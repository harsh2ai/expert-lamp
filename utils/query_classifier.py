from typing import Dict, List
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import AGENT_MODEL, TEMPERATURE
import json

class QueryClassifier:
    def __init__(self):
        self.model = ChatOpenAI(
            model_name=AGENT_MODEL,
            temperature=TEMPERATURE
        )
        
        # Patterns for different types of queries
        self.patterns = {
            'analytical': [
                'rate', 'trend', 'analysis', 'compare', 'performance',
                'distribution', 'breakdown', 'month', 'percentage',
                'average', 'avg', 'total', 'count', 'rto', 'ndr', 'fasr'
            ],
            'tracking': [
                'track', 'where', 'status', 'awb', 'delivery status',
                'shipment status', 'order status'
            ],
            'metric_terms': {
                'rto': ['rto', 'return', 'returned'],
                'ndr': ['ndr', 'non delivery', 'not delivered'],
                'fasr': ['fasr', 'first attempt', 'success rate'],
                'tat': ['tat', 'turnaround', 'delivery time']
            }
        }

    def classify(self, query: str) -> Dict:
        """Classify the query and determine appropriate agent(s)"""
        query_lower = query.lower()
        
        # Extract metrics and entities
        metrics = self.extract_key_metrics(query_lower)
        tracking_numbers = self._extract_tracking_numbers(query)
        
        # Check if query is analytical
        if any(term in query_lower for term in self.patterns['analytical']):
            return {
                "primary_agent": "operations",
                "secondary_agents": [],
                "metrics": metrics,
                "entities": self._extract_entities(query_lower),
                "confidence_score": 0.9,
                "query_type": "analytical"
            }
        
        # Check if query is about tracking
        if tracking_numbers or any(term in query_lower for term in self.patterns['tracking']):
            return {
                "primary_agent": "delivery",
                "secondary_agents": [],
                "metrics": metrics,
                "entities": tracking_numbers,
                "confidence_score": 0.9,
                "query_type": "tracking"
            }
        
        # Default to customer service
        return {
            "primary_agent": "customer",
            "secondary_agents": [],
            "metrics": metrics,
            "entities": [],
            "confidence_score": 0.7,
            "query_type": "general"
        }

    def extract_key_metrics(self, query: str) -> List[str]:
        """Extract mentioned metrics/KPIs from query"""
        found_metrics = []
        for metric, terms in self.patterns['metric_terms'].items():
            if any(term in query for term in terms):
                found_metrics.append(metric)
        return found_metrics

    def _extract_tracking_numbers(self, text: str) -> List[str]:
        """Extract AWB numbers from text"""
        # Pattern for AWB numbers (adjust based on your actual AWB format)
        awb_pattern = r'AWB\d{8}'
        return re.findall(awb_pattern, text, re.IGNORECASE)

    def _extract_entities(self, text: str) -> List[str]:
        """Extract other relevant entities from query"""
        entities = []
        
        # Zone patterns
        zone_pattern = r'zone[_\s]?[a-e]2?'
        zones = re.findall(zone_pattern, text, re.IGNORECASE)
        entities.extend(zones)
        
        # City tier patterns
        tier_pattern = r'tier[_\s]?[123]|metro'
        tiers = re.findall(tier_pattern, text, re.IGNORECASE)
        entities.extend(tiers)
        
        # Payment mode patterns
        if 'cod' in text.lower():
            entities.append('COD')
        if 'prepaid' in text.lower():
            entities.append('PREPAID')
        
        return entities

    def _preprocess_query(self, query: str) -> str:
        """Clean and standardize query text"""
        query = query.lower().strip()
        query = re.sub(r'\s+', ' ', query)
        return query