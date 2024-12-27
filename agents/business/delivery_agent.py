from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from utils.metrics import MetricsCalculator
from database.connector import get_db_connection
import pandas as pd

class DeliveryAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.metrics_calculator = MetricsCalculator()
        self.conn = get_db_connection()

    def process_query(self, query: str, context: Dict[str, Any] = None) -> str:
        # Extract tracking numbers from context or query
        tracking_numbers = context.get('entities', []) if context else []
        if not tracking_numbers:
            tracking_numbers = self._extract_tracking_numbers(query)
        
        try:
            if tracking_numbers:
                # Get tracking info for the first AWB
                return self._get_tracking_info(tracking_numbers[0])
            else:
                return "Please provide a valid tracking number (AWB) to check your delivery status."
                
        except Exception as e:
            return f"I encountered an error while retrieving the tracking information: {str(e)}"

    def _extract_tracking_numbers(self, text: str) -> List[str]:
        """Extract AWB numbers from text"""
        import re
        awb_pattern = r'AWB\d{8}'
        return re.findall(awb_pattern, text, re.IGNORECASE)

    def _get_tracking_info(self, awb: str) -> str:
        """Get tracking information for an AWB"""
        query = """
            SELECT 
                AWB_CODE,
                SHIPMENT_STATUS,
                ASSIGNED_DATE_TIME,
                FIRST_ATTEMPT_DATE,
                AWB_DELIVERED_DATE,
                NO_OF_ATTEMPTS,
                NDR_RAISED_SHIPMENTS,
                PARENT_COURIER,
                ZONE,
                CITY_TIER
            FROM DEV_REPORTS_COPILOT_REPORT
            WHERE AWB_CODE = ?
            """
        
        try:
            df = pd.read_sql_query(query, self.conn, params=[awb])
            
            if df.empty:
                return f"No tracking information found for AWB: {awb}"
            
            row = df.iloc[0]
            
            response = f"Tracking Information for {awb}:\n\n"
            response += f"Status: {row['SHIPMENT_STATUS']}\n"
            response += f"Courier: {row['PARENT_COURIER']}\n"
            response += f"Zone: {row['ZONE']}\n"
            response += f"City Tier: {row['CITY_TIER']}\n\n"
            
            try:
                response += f"Assigned Date: {pd.to_datetime(row['ASSIGNED_DATE_TIME']).strftime('%Y-%m-%d %H:%M')}\n"
                
                if pd.notna(row['FIRST_ATTEMPT_DATE']):
                    response += f"First Attempt: {pd.to_datetime(row['FIRST_ATTEMPT_DATE']).strftime('%Y-%m-%d %H:%M')}\n"
                
                if pd.notna(row['AWB_DELIVERED_DATE']):
                    response += f"Delivered Date: {pd.to_datetime(row['AWB_DELIVERED_DATE']).strftime('%Y-%m-%d %H:%M')}\n"
            except:
                pass
            
            response += f"\nDelivery Attempts: {row['NO_OF_ATTEMPTS']}\n"
            
            if row['NDR_RAISED_SHIPMENTS']:
                response += "Note: Non-Delivery Report (NDR) has been raised for this shipment\n"
            
            return response
        except Exception as e:
            return f"Error retrieving tracking info: {str(e)}"