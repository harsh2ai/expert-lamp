from typing import Dict

DELIVERY_BASE_PROMPT = """You are a Delivery Performance Analysis Agent specializing in shipment tracking metrics.
Focus on: RTO rates, NDR patterns, FASR, and delivery success metrics.

Current Query: {query}
Context: {context}

Analyze the query and provide insights focusing on delivery performance.
Include relevant metrics and their interpretation."""

DELIVERY_ANALYSIS_PROMPT = """Analyze the following delivery metrics:
- RTO Rate: {rto_rate}%
- NDR Rate: {ndr_rate}%
- FASR: {fasr}%
- Delivery Success Rate: {delivery_rate}%

Provide business insights and recommendations based on these metrics.
Consider historical patterns and industry benchmarks."""

DELIVERY_ALERT_PROMPT = """Review the following metrics for potential issues:
Metrics: {metrics}
Thresholds: {thresholds}

Identify any metrics that require immediate attention and explain why."""