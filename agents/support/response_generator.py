from typing import Dict, List, Any
from datetime import datetime
import json

class ResponseGenerator:
    def __init__(self):
        self.response_templates = {
            'metrics': """
Based on the analysis:
- {metric_details}
- {insights}
- {recommendations}
            """.strip(),
            
            'error': """
Unable to process query due to: {error_message}
Suggestion: {suggestion}
            """.strip(),
            
            'clarification': """
To better assist you, could you please clarify:
{clarification_points}
            """.strip()
        }

    def generate_response(self, 
                         data: Dict[str, Any],
                         response_type: str = 'metrics') -> str:
        """Generate formatted response"""
        if response_type not in self.response_templates:
            return "Invalid response type"
            
        template = self.response_templates[response_type]
        
        try:
            return template.format(**data)
        except KeyError as e:
            return f"Error generating response: Missing key {str(e)}"

    def format_metrics(self, metrics: Dict[str, float]) -> str:
        """Format metrics for response"""
        formatted_metrics = []
        for metric, value in metrics.items():
            if isinstance(value, float):
                formatted_metrics.append(f"{metric}: {value:.2f}%")
            else:
                formatted_metrics.append(f"{metric}: {value}")
                
        return "\n".join(formatted_metrics)

    def add_confidence_score(self, response: str, 
                           confidence: float) -> str:
        """Add confidence score to response"""
        if confidence < 0.7:
            return f"{response}\n\nNote: This analysis is based on limited data and may need further verification."
        return response

    def format_error_response(self, error: Exception) -> str:
        """Format error response"""
        return self.generate_response({
            'error_message': str(error),
            'suggestion': 'Please try refining your query or contact support.'
        }, response_type='error')