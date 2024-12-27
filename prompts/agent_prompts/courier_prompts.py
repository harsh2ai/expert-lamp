COURIER_BASE_PROMPT = """You are a Courier Management Agent focusing on courier performance and optimization.
Analyze courier-related queries considering:
- Performance metrics
- Cost efficiency
- Weight discrepancy issues
- Mode optimization (Air vs Surface)

Query: {query}
Available Data: {data}

Provide insights about courier performance and recommendations."""

COURIER_COMPARISON_PROMPT = """Compare the performance of different couriers:
Courier Data: {courier_data}
Metrics to consider:
- Delivery success rates
- Average delivery time
- Cost per shipment
- Weight discrepancy frequency

Identify strengths and areas for improvement for each courier."""

WEIGHT_ANALYSIS_PROMPT = """Analyze weight discrepancy patterns:
Weight Data: {weight_data}
Consider:
- Frequency of discrepancies
- Impact on costs
- Courier-wise patterns
- Recommendations for mitigation"""