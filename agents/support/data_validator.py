from typing import Dict, List, Any
from datetime import datetime
import pandas as pd
from database.connector import get_db_session

class DataValidator:
    def __init__(self):
        self.required_columns = [
            'AWB_CODE', 'ZONE', 'CITY_TIER', 'SHIPMENT_STATUS',
            'DELIVERED_SHIPMENTS', 'RTO_SHIPMENTS'
        ]
        
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate incoming data"""
        validation_results = {
            'is_valid': True,
            'missing_fields': [],
            'invalid_values': [],
            'warnings': []
        }
        
        # Check required fields
        for field in self.required_columns:
            if field not in data:
                validation_results['missing_fields'].append(field)
                validation_results['is_valid'] = False
        
        # Validate field values
        if 'ZONE' in data:
            if data['ZONE'] not in ['z_a', 'z_b', 'z_c', 'z_d', 'z_e', 'z_e2']:
                validation_results['invalid_values'].append(('ZONE', data['ZONE']))
        
        if 'CITY_TIER' in data:
            if data['CITY_TIER'] not in ['Tier1', 'Tier2', 'Tier3', 'Metro', 'Others']:
                validation_results['invalid_values'].append(('CITY_TIER', data['CITY_TIER']))
        
        return validation_results

    def clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and standardize data"""
        cleaned_data = data.copy()
        
        # Standardize dates
        date_fields = ['ASSIGNED_DATE_TIME', 'PICKED_DATE', 'AWB_DELIVERED_DATE']
        for field in date_fields:
            if field in cleaned_data and cleaned_data[field]:
                try:
                    cleaned_data[field] = pd.to_datetime(cleaned_data[field])
                except:
                    cleaned_data[field] = None
        
        # Standardize boolean fields
        bool_fields = ['RTO_SHIPMENTS', 'DELIVERED_SHIPMENTS', 'NDR_RAISED_SHIPMENTS']
        for field in bool_fields:
            if field in cleaned_data:
                cleaned_data[field] = bool(cleaned_data[field])
        
        return cleaned_data

    def validate_metrics(self, metrics: Dict[str, float]) -> bool:
        """Validate calculated metrics"""
        valid = True
        
        # Check metric ranges
        for metric, value in metrics.items():
            if isinstance(value, (int, float)):
                if value < 0 or value > 100:
                    valid = False
                    break
        
        return valid