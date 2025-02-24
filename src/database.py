import snowflake.connector
from contextlib import contextmanager
from .config import get_settings
import logging

logger = logging.getLogger(__name__)

class DatabasePool:
    _pool = None
    _settings = get_settings()

    @classmethod
    def get_pool(cls):
        try:
            if cls._pool is None or not cls._pool.is_alive():
                logger.info("Creating new Snowflake connection")
                cls._pool = snowflake.connector.connect(
                    account=cls._settings.SNOWFLAKE_ACCOUNT,
                    user=cls._settings.SNOWFLAKE_USER,
                    password=cls._settings.SNOWFLAKE_PASSWORD,
                    database=cls._settings.SNOWFLAKE_DATABASE,
                    schema=cls._settings.SNOWFLAKE_SCHEMA,
                    warehouse=cls._settings.SNOWFLAKE_WAREHOUSE,
                    # Connection pooling settings
                    client_session_keep_alive=True,
                    client_prefetch_threads=cls._settings.DB_POOL_MIN_CONNECTIONS,
                    max_connection_pool=cls._settings.DB_POOL_MAX_CONNECTIONS
                )
            return cls._pool
        except Exception as e:
            logger.error(f"Error connecting to Snowflake: {str(e)}")
            raise

    @classmethod
    @contextmanager
    def get_connection(cls):
        conn = None
        try:
            conn = cls.get_pool()
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        finally:
            if conn and not conn.is_closed():
                try:
                    conn.cursor().close()
                except:
                    pass 