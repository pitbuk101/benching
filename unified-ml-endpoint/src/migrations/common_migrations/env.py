# type: ignore
import os
import sys
from logging.config import fileConfig
from dotenv import load_dotenv
from alembic import context
from constants import DB_HOST, DB_NAME, DB_PORT, DB_SECRET, DB_USER
from sqlalchemy import engine_from_config, pool, text


load_dotenv()
# flake8: noqa: E402
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from schema_user_creator import create_schema, create_user

from ada.utils.config.config_loader import read_config

conf = read_config("azml_deployment.yaml")


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None


def get_connection_params():
    """
    Fetching the connection params from the environment variables. The variables are set by the db_migrate file whihc was a component in azure
    and triggerred by the pipeline
    Returns:
        db_user: string
        db_pass: string
        db_host: string
        db_port: string
        db_name: string
    """
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_SECRET')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    return db_user, db_pass, db_host, db_port, db_name


db_user, db_pass, db_host, db_port, db_name = get_connection_params()
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}",
)


def grant_permission_to_public(connection, common_schema_name: str):
    connection.execute(
        text(
            f"""
                GRANT USAGE ON SCHEMA {common_schema_name} TO PUBLIC;
                ALTER DEFAULT PRIVILEGES IN SCHEMA {common_schema_name} GRANT ALL ON TABLES TO PUBLIC;
                """,
        ),
    )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        common_schema_name = "common"
        common_user_name = "common-db-user"
        connection.execute(text("CREATE extension IF NOT EXISTS vector with schema public;"))

        create_user(connection, db_user, common_schema_name, common_user_name)

        create_schema(connection, common_schema_name, common_user_name)

        grant_permission_to_public(connection, common_schema_name)

        execute_migrations_against_schema(connection, common_schema_name)


def execute_migrations_against_schema(connection, common_schema_name):
    print("Running for the tenant TenantId: ", common_schema_name)
    connection.execute(text(f'set search_path to "{common_schema_name}", public'))
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
