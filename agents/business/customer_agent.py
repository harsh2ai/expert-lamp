from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from utils.metrics import MetricsCalculator

class CustomerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.metrics_calculator = MetricsCalculator()

    def process_query(self, query: str, context: Dict[str, Any] = None) -> str:
        # Get customer metrics
        customer_data = self._get_customer_metrics(context)
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a customer service agent for a shipping company. 
            Help customers track their orders and answer shipping-related questions."""),
            ("human", "{query}")
        ])
        
        # Create chain using the new pipe syntax
        chain = prompt | self.llm
        
        try:
            # Use invoke instead of run
            response = chain.invoke({
                "query": query
            })
            return str(response.content)
        except Exception as e:
            return "I need more information to help track your order. Could you please provide your order ID or AWB number?"

    def _get_customer_metrics(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Calculate customer-related metrics"""
        try:
            metrics = {}
            if context and context.get("order_id"):
                # Add metrics calculation logic here
                pass
            return metrics
        except Exception as e:
            return {}