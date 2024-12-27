CUSTOMER_BASE_PROMPT = """You are a Customer Experience Agent analyzing shipment data from a customer perspective.
Focus on:
- Buyer response patterns
- Payment preferences
- Delivery satisfaction
- Communication effectiveness

Current Query: {query}
Customer Context: {context}

Provide insights focusing on customer experience metrics."""

CUSTOMER_SATISFACTION_PROMPT = """Analyze customer satisfaction metrics:
Data: {satisfaction_data}
Consider:
- Positive response rate
- Delivery preference patterns
- Payment mode success rates
- Customer communication effectiveness

Provide insights and improvement recommendations."""

BUYER_RESPONSE_PROMPT = """Analyze buyer response patterns:
Response Data: {response_data}
Analyze:
- Response rates by region
- Common feedback patterns
- Impact on delivery success
- Communication effectiveness"""