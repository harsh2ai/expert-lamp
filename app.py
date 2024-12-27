import streamlit as st
import pandas as pd
from config import PAGE_TITLE, PAGE_ICON, AGENT_TYPES
from database.connector import init_db
from agents.orchestrator import OrchestratorAgent
from utils.query_classifier import QueryClassifier

# Page Configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide"
)

def display_query_and_results(sql_query: str, df: pd.DataFrame):
    """Display SQL query and results in a formatted way"""
    # Display SQL Query in an expander
    with st.expander("View SQL Query"):
        st.code(sql_query, language='sql')
    
    # Display results in a table with formatting
    st.dataframe(
        df.style.format({
            col: '{:.2f}' for col in df.select_dtypes(include=['float64']).columns
        }),
        use_container_width=True,
        hide_index=True
    )

    # If the data might be interesting as a chart, offer visualization options
    if len(df) > 0 and df.select_dtypes(include=['float64', 'int64']).columns.any():
        with st.expander("View Visualization"):
            # Determine suitable visualization based on data
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            if 'month' in df.columns.str.lower() and len(numeric_cols) > 0:
                # Time series plot
                st.line_chart(df.set_index('MONTH')[numeric_cols])
            elif len(df) <= 10:  # For small datasets
                st.bar_chart(df.set_index(df.columns[0])[numeric_cols])

def init_session_state():
    """Initialize session state variables"""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = None

def display_metrics_dashboard():
    """Display key metrics in the sidebar"""
    with st.sidebar:
        st.subheader("Key Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Queries", len(st.session_state.conversation_history) // 2)
        with col2:
            if st.session_state.current_agent:
                st.metric("Active Agent", st.session_state.current_agent)

def main():
    # Initialize
    init_session_state()
    init_db()

    # Page Header with styling
    st.title(f"{PAGE_ICON} {PAGE_TITLE}")
    
    # Sidebar
    with st.sidebar:
        st.header("System Controls")
        # Display metrics
        display_metrics_dashboard()
        
        # Clear conversation button
        if st.button("Clear Conversation", type="primary"):
            st.session_state.conversation_history = []
            st.session_state.current_agent = None
            st.rerun()
        
        # Help section
        with st.expander("Help & Tips"):
            st.markdown("""
            **Example Queries:**
            - Track order: "Where is AWB00000004?"
            - Analytics: "Show RTO rate month over month"
            - Performance: "What's our delivery success rate?"
            """)

    # Main Chat Interface
    st.subheader("Chat Interface")
    
    # Display conversation history
    for message in st.session_state.conversation_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            # If message contains SQL and results, display them
            if "sql_query" in message and "results" in message:
                display_query_and_results(
                    message["sql_query"],
                    pd.DataFrame(message["results"])
                )

    # Chat input
    if prompt := st.chat_input("Ask about your shipments..."):
        # Add user message to history
        st.session_state.conversation_history.append({
            "role": "user",
            "content": prompt
        })

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Processing your query..."):
                try:
                    orchestrator = OrchestratorAgent()
                    response, sql_query, results = orchestrator.process_query(prompt)
                    
                    # Add assistant response to history
                    message = {
                        "role": "assistant",
                        "content": response
                    }
                    
                    # If we have SQL and results, add them
                    if sql_query and results is not None:
                        message["sql_query"] = sql_query
                        message["results"] = results
                        
                    st.session_state.conversation_history.append(message)
                    
                    # Display response
                    st.write(response)
                    if sql_query and results is not None:
                        display_query_and_results(sql_query, pd.DataFrame(results))
                        
                except Exception as e:
                    error_msg = f"Error processing query: {str(e)}"
                    st.error(error_msg)
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": error_msg
                    })

if __name__ == "__main__":
    main()