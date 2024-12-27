from typing import Dict, Any, List, Tuple, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from database.connector import get_db_connection
import pandas as pd

class OperationsAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.conn = get_db_connection()
        
        # Schema information for the LLM
        self.table_schema = """
        Table: VIEW_TITANIUM_PLATINUM_REPORT
        Columns:
        - ZONE: Geographical delivery zone (z_a, z_b, z_c, z_d, z_e, z_e2)
        - CITY_TIER: Tier of delivery city (Tier1, Tier2, Tier3, Metro, Others)
        - ASSIGNED_DATE_TIME: Timestamp when shipment was assigned
        - AWB_CODE: Unique AWB code
        - IS_DELIVERYBOOST: Indicates if delivery boost (0/1)
        - PARENT_COURIER: Primary courier partner name
        - SHIPMENT_STATUS: Current status code
        - RTO_SHIPMENTS: Whether shipment was returned (0/1)
        - FASR_SHIPMENT: First delivery attempt success (0/1)
        - NDR_RAISED_SHIPMENTS: Whether NDR was raised (0/1)
        - MODE_OF_SHIPMENT: PREPAID or COD
        - AWB_DELIVERED_DATE: Delivery date
        """
        
        self.nl2sql_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in converting natural language queries to SQL. 
            Given the following schema and a question, generate a SQLite-compatible SQL query.
            
            {schema}
            
            Rules:
            1. Use substr(ASSIGNED_DATE_TIME, 1, 7) for monthly grouping
            2. Use julianday() for date differences
            3. Always include proper error handling
            4. Round percentages to 2 decimal places using ROUND()
            5. Order results meaningfully (usually by date DESC)
            6. Always alias columns with clear names
            7. For month-over-month analysis, use substr(ASSIGNED_DATE_TIME, 1, 7) as MONTH
            
            Generate only the SQL query, no explanations."""),
            ("human", "{question}")
        ])

    def process_query(self, query: str, context: Dict[str, Any] = None) -> Tuple[str, str, List[Dict]]:
        try:
            # Generate SQL from natural language
            chain = self.nl2sql_prompt | self.llm
            sql_response = chain.invoke({
                "schema": self.table_schema,
                "question": query
            })
            
            sql_query = sql_response.content
            
            # Execute the generated query
            df = pd.read_sql_query(sql_query, self.conn)
            
            # Format natural language response
            response = self._format_results_text(df, query)
            
            return response, sql_query, df.to_dict('records')
            
        except Exception as e:
            raise Exception(f"Failed to process query: {str(e)}")

    def _format_results_text(self, df: pd.DataFrame, query: str) -> str:
        """Format results into natural language response"""
        if df.empty:
            return "No data found for your query."
        
        query_lower = query.lower()
        
        # Format based on query type
        if any(word in query_lower for word in ['rto', 'return']):
            return self._format_rto_response(df)
        elif any(word in query_lower for word in ['time', 'tat', 'duration']):
            return self._format_time_response(df)
        elif 'distribution' in query_lower or 'breakdown' in query_lower:
            return self._format_distribution_response(df)
        else:
            # Generic formatting
            return f"Here are the results:\n\n{df.to_string(index=False)}"

    def _format_rto_response(self, df: pd.DataFrame) -> str:
        """Format RTO analysis results"""
        response = "RTO Analysis:\n\n"
        for _, row in df.iterrows():
            response += f"Period: {row.get('MONTH', 'N/A')}\n"
            for col in row.index:
                if col != 'MONTH':
                    value = row[col]
                    if isinstance(value, float):
                        response += f"{col}: {value:.2f}%\n"
                    else:
                        response += f"{col}: {value}\n"
            response += "\n"
        return response

    def _format_time_response(self, df: pd.DataFrame) -> str:
        """Format time-based results"""
        response = "Delivery Time Analysis:\n\n"
        for _, row in df.iterrows():
            response += f"Period: {row.get('MONTH', row.get('ZONE', 'N/A'))}\n"
            for col in row.index:
                if 'TIME' in col.upper() or 'DURATION' in col.upper():
                    value = row[col]
                    if isinstance(value, float):
                        response += f"{col}: {value:.1f} hours\n"
                    else:
                        response += f"{col}: {value}\n"
            response += "\n"
        return response

    def _format_distribution_response(self, df: pd.DataFrame) -> str:
        """Format distribution analysis results"""
        response = "Distribution Analysis:\n\n"
        for _, row in df.iterrows():
            category = row.get(df.columns[0], 'N/A')
            response += f"Category: {category}\n"
            for col in df.columns[1:]:
                value = row[col]
                if isinstance(value, float):
                    response += f"{col}: {value:.2f}%\n"
                else:
                    response += f"{col}: {value}\n"
            response += "\n"
        return response