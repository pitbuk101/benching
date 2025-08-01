import os
import sys
from logging.config import fileConfig
from dotenv import load_dotenv
from alembic import context
from constants import DB_HOST, DB_NAME, DB_PORT, DB_SECRET, DB_USER, TENANT_LIST
from schema_user_creator import (
    create_schema,
    create_user,
    grant_permissions_to_materialized_views,
)
from sqlalchemy import engine_from_config, pool, text

load_dotenv()

# flake8: noqa: E402
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

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
        schema_names = str(os.getenv(TENANT_LIST)).split(",")
        print("List of available tenants : ", schema_names)

        for schema_name in schema_names:
            create_user(connection, db_user, schema_name, schema_name)
            create_schema(connection, schema_name, schema_name)
            print("Running for the tenant TenantId: ", schema_name)
            connection.execute(text('set search_path to "%s", public' % schema_name))
            with context.begin_transaction():
                context.run_migrations()
                grant_permissions_to_materialized_views(connection, schema_name, schema_name)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
