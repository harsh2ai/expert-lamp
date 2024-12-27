import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database
DB_PATH = os.getenv("DB_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model Configs
ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL")
AGENT_MODEL = os.getenv("AGENT_MODEL")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))

# Streamlit
PAGE_TITLE = os.getenv("PAGE_TITLE", "Shipment Tracking RAG System")
PAGE_ICON = os.getenv("PAGE_ICON", "🚚")

# Agent Configs
AGENT_TYPES = {
    "delivery": "Delivery Performance Agent",
    "courier": "Courier Management Agent",
    "customer": "Customer Experience Agent",
    "operations": "Operations Agent"
}

# Query Classification Thresholds
CONFIDENCE_THRESHOLD = 0.7
MAX_CONTEXT_LENGTH = 5
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Snowflake Configuration
SNOWFLAKE_CONFIG = {
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'role': os.getenv('SNOWFLAKE_ROLE'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': os.getenv('SNOWFLAKE_DATABASE'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA')
}

# Table Configuration
TABLE_NAME = "VIEW_TITANIUM_PLATINUM_REPORT"
SCHEMA_NAME = SNOWFLAKE_CONFIG['schema']

# Other configurations remain the same...