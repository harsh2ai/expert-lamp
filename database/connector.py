import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
from config import SNOWFLAKE_CONFIG
from contextlib import contextmanager

def init_db():
    """Initialize database connection and verify connectivity"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test the connection
        cursor.execute(f"SELECT 1 FROM {SNOWFLAKE_CONFIG['schema']}.VIEW_TITANIUM_PLATINUM_REPORT LIMIT 1")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        raise Exception(f"Failed to initialize database connection: {str(e)}")

def get_db_connection():
    """Create Snowflake connection"""
    return snowflake.connector.connect(
        user=SNOWFLAKE_CONFIG['user'],
        password=SNOWFLAKE_CONFIG['password'],
        account=SNOWFLAKE_CONFIG['account'],
        warehouse=SNOWFLAKE_CONFIG['warehouse'],
        database=SNOWFLAKE_CONFIG['database'],
        schema=SNOWFLAKE_CONFIG['schema'],
        role=SNOWFLAKE_CONFIG['role']
    )

@contextmanager
def get_db_session():
    """Get database session"""
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query: str, params: dict = None):
    """Execute SQL query"""
    with get_db_session() as conn:
        cur = conn.cursor()
        try:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            return cur.fetchall()
        finally:
            cur.close()

def execute_query_df(query: str) -> pd.DataFrame:
    """Execute query and return DataFrame"""
    with get_db_session() as conn:
        return pd.read_sql_query(query, conn)