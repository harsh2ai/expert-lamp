from typing import Dict, List, Any
from datetime import datetime

class ContextManager:
    def __init__(self):
        self.context = {
            'conversation_history': [],
            'active_entities': set(),
            'current_metrics': {},
            'last_query_time': None
        }
        
    def update_context(self, query: str, response: str, 
                      entities: List[str] = None, 
                      metrics: Dict[str, Any] = None) -> None:
        """Update conversation context"""
        # Update conversation history
        self.context['conversation_history'].append({
            'query': query,
            'response': response,
            'timestamp': datetime.now()
        })
        
        # Update active entities
        if entities:
            self.context['active_entities'].update(entities)
        
        # Update metrics
        if metrics:
            self.context['current_metrics'].update(metrics)
        
        self.context['last_query_time'] = datetime.now()

    def get_relevant_context(self, query: str) -> Dict[str, Any]:
        """Get context relevant to current query"""
        relevant_context = {
            'recent_history': self.context['conversation_history'][-3:],
            'active_entities': list(self.context['active_entities']),
            'current_metrics': self.context['current_metrics']
        }
        return relevant_context

    def clear_context(self) -> None:
        """Clear context data"""
        self.context = {
            'conversation_history': [],
            'active_entities': set(),
            'current_metrics': {},
            'last_query_time': None
        }

    def should_refresh_context(self) -> bool:
        """Check if context needs refreshing"""
        if not self.context['last_query_time']:
            return True
            
        time_difference = datetime.now() - self.context['last_query_time']
        return time_difference.total_seconds() > 1800  # 30 minutes