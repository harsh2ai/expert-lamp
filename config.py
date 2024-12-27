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