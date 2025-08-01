import os
import secrets
from dotenv import load_dotenv
from sqlalchemy import text
from ada.components.azureml.workspace import get_workspace
from ada.utils.config.config_loader import read_config

load_dotenv()

first_row = first_column = 0


conf = read_config("azml_deployment.yaml")


def set_user_secret(user_name: str) -> str:
    """
    Sets a user secret in Azure Key Vault.

    Args:
        user_name (str): The name of the user for whom the secret is being set.

    Returns:
        str: The secret value for the user.
    """
    if os.getenv("LOCAL_DB_MODE") == "1":
        return "postgres"

    user_key_name = "psql-" + user_name
    workspace = get_workspace(conf)
    key_vault = workspace.get_default_keyvault()
    try:
        tenant_password = key_vault.get_secret(user_key_name)
        print(f"Key {user_key_name} already exist in keyvault")
        return tenant_password
    except Exception:
        # Generate a random key value
        key_value = secrets.token_urlsafe(32)

        # Add the key to Key Vault
        key_vault.set_secret(name=user_key_name, value=key_value)

        print(f"Key '{user_key_name}' with a random value added to Key Vault.")
        return key_value


def create_user(connection, admin_user: str, schema_name: str, user_name: str):
    """
    Creates a database user with the specified schema and grants access.

    Args:
        connection: The database connection object.
        admin_user (str): The name of the administrative user.
        schema_name (str): The name of the schema to associate with the user.
        user_name (str): The name of the user to be created.

    Returns:
        None
    """

    is_user_exist = f"""
                    SELECT COUNT(1) FROM pg_catalog.pg_roles WHERE  rolname = '{user_name}';
                """
    user_exist_cursor = connection.execute(text(is_user_exist))
    user_exists = user_exist_cursor.fetchall()

    if user_exists[first_row][first_column] == 0:
        print(f"Creating {schema_name} user: {user_name}")
        user_password = set_user_secret(user_name)
        connection.execute(
            text(
                f"""
                CREATE USER "{user_name}" WITH PASSWORD '{user_password}';
                GRANT "{user_name}" TO "{admin_user}";
                """,
            ),
        )


def grant_permissions_to_materialized_views(connection, schema_name: str, user_name: str):
    """
    Grants permissions to the user on all materialized views in the schema.
    """
    material_views = connection.execute(
        text(
            f"""
                SELECT matviewname
                FROM pg_matviews
                WHERE schemaname='{schema_name}'
            """,
        ),
    ).cursor.fetchall()

    for mat_view in material_views:
        alter_ownership_query = f"""
                ALTER MATERIALIZED VIEW "{schema_name}".{mat_view[0]} OWNER TO "{user_name}";
            """
        connection.execute(text(alter_ownership_query))


def create_schema(connection, schema_name: str, user_name: str):
    """
    Creates a schema if it does not exist and assigns it to the user.

    Args:
        connection: The database connection object.
        schema_name (str): The name of the schema to create.
        user_name (str): The name of the user to assign ownership of the schema.

    Returns:
        None
    """

    print(f"Creating schema if not exists: {schema_name}")
    connection.execute(
        text(
            f"""
            CREATE SCHEMA IF NOT EXISTS "{schema_name}";
            ALTER SCHEMA "{schema_name}" OWNER TO "{user_name}";
            GRANT ALL ON ALL TABLES IN SCHEMA "{schema_name}" TO "{user_name}";
            GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO "{user_name}";
            GRANT ALL ON ALL SEQUENCES IN SCHEMA "{schema_name}" TO "{user_name}"
            """,
        ),
    )
