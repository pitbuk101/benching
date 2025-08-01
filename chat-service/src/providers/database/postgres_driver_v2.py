from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from src.env import PGUSER, PGPASSWORD, PGHOST, PGPORT, PGDATABASE
from src.utils.logs import get_custom_logger

logger = get_custom_logger(__name__)

class PostgresConnection:
    def __init__(self, conn_params):
        self.conn_params = conn_params
        self.engine: Engine = create_engine(self._build_conninfo(conn_params), pool_size=50, max_overflow=100, pool_timeout=60)

    def _build_conninfo(self, params):
        if PGHOST in ("localhost", "postgres"):
            logger.critical("Using Local Postgres")
            connection_url = (
                f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
            )
        else:
            logger.critical("Using SSL Mode AWS")
            connection_url = (
                f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
                f"?sslmode=require"
            )
        return connection_url

    def execute(self, query: str, *args):
        """
        Executes a query. For SELECT, returns rows and columns.
        For others (INSERT/UPDATE/DELETE), returns status.
        """
        try:
            with self.engine.connect() as conn:
                if query.strip().lower().startswith("select"):
                    result = conn.execute(text(query), args)
                    rows = result.fetchall()
                    columns = result.keys()
                    return {"columns": columns, "data": rows}
                else:
                    result = conn.execute(text(query), args)
                    conn.commit()
                    return result.rowcount  # or result.cursor.statusmessage if needed
        except Exception as e:
            logger.exception(f"Error executing query: {e}")

    def connect(self):
        # No-op for compatibility
        pass

    def close(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None


postgres_client = PostgresConnection({
    "user": PGUSER,
    "password": PGPASSWORD,
    "host": PGHOST,
    "port": PGPORT,
    "database": PGDATABASE
})
