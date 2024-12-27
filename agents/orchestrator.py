from typing import Dict, List, Tuple, Any, TypedDict, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from operator import itemgetter
from langgraph.graph import Graph, StateGraph,END
#rom langgraph.prebuilt import END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import ORCHESTRATOR_MODEL, AGENT_MODEL
from utils.query_classifier import QueryClassifier
from typing import Dict, List, Any, TypedDict, Optional, Tuple  # Added Tuple here

class GraphState(TypedDict):
    messages: List[BaseMessage]
    current_agent: str
    context: Dict[str, Any]
    next_step: str
    query_type: str
    entities: List[str]
    metrics: List[str]
    sql_query: Optional[str]
    results: Optional[List[Dict]]

def get_business_agent(agent_type: str):
    """Get specific business agent based on type"""
    if agent_type == "delivery":
        from agents.business.delivery_agent import DeliveryAgent
        return DeliveryAgent()
    elif agent_type == "operations":
        from agents.business.operations_agent import OperationsAgent
        return OperationsAgent()
    elif agent_type == "customer":
        from agents.business.customer_agent import CustomerAgent
        return CustomerAgent()
    elif agent_type == "courier":
        from agents.business.courier_agent import CourierAgent
        return CourierAgent()
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

def classify_query(state: GraphState) -> GraphState:
    """Classify incoming query and update state"""
    classifier = QueryClassifier()
    messages = state["messages"]
    latest_message = messages[-1].content
    
    classification = classifier.classify(latest_message)
    
    return {
        **state,
        "query_type": classification["primary_agent"],
        "entities": classification["entities"],
        "metrics": classification["metrics"],
        "next_step": "route_to_agent"
    }

def route_to_agent(state: GraphState) -> GraphState:
    """Route query to appropriate agent"""
    agent_type = state["query_type"]
    agent = get_business_agent(agent_type)
    
    try:
        if agent_type == "operations":
            response, sql_query, results = agent.process_query(
                query=state["messages"][-1].content,
                context={
                    "entities": state["entities"],
                    "metrics": state["metrics"]
                }
            )
            state["sql_query"] = sql_query
            state["results"] = results
        else:
            response = agent.process_query(
                query=state["messages"][-1].content,
                context={
                    "entities": state["entities"],
                    "metrics": state["metrics"]
                }
            )
            
        state["messages"].append(AIMessage(content=response))
        state["current_agent"] = agent_type
        state["next_step"] = "check_followup"
        
        return state
    except Exception as e:
        error_msg = f"Error in agent processing: {str(e)}"
        state["messages"].append(AIMessage(content=error_msg))
        return state

def check_followup(state: GraphState) -> str:
    """Determine if query needs followup"""
    context = state.get("context", {})
    
    if context.get("need_clarification"):
        return "need_clarification"
    elif context.get("need_additional_data"):
        return "need_data"
    elif context.get("need_cross_agent"):
        return "cross_agent"
    else:
        return "end"

def handle_clarification(state: GraphState) -> GraphState:
    """Handle cases needing clarification"""
    llm = ChatOpenAI(model=AGENT_MODEL)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate a clarifying question based on this user query."),
        ("human", "{query}")
    ])
    
    chain = prompt | llm
    clarification = chain.invoke({"query": state["messages"][-1].content})
    state["messages"].append(AIMessage(content=str(clarification)))
    state["next_step"] = "await_user"
    return state

def create_graph() -> Graph:
    """Create the workflow graph"""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("classify", classify_query)
    workflow.add_node("route", route_to_agent)
    workflow.add_node("clarify", handle_clarification)
    
    # Add edges with conditions
    workflow.add_edge("classify", "route")
    workflow.add_conditional_edges(
        "route",
        check_followup,
        {
            "need_clarification": "clarify",
            "need_data": "route",
            "end": END
        }
    )
    workflow.add_edge("clarify", "classify")
    
    workflow.set_entry_point("classify")
    return workflow.compile()

class OrchestratorAgent:
    def __init__(self):
        self.graph = create_graph()
        self.classifier = QueryClassifier()
    
    def process_query(self, query: str) -> Tuple[str, Optional[str], Optional[List[Dict]]]:
        """Process query through the graph and return response, SQL query, and results"""
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "current_agent": None,
            "context": {},
            "next_step": "classify",
            "query_type": None,
            "entities": [],
            "metrics": [],
            "sql_query": None,
            "results": None
        }
        
        try:
            final_state = self.graph.invoke(initial_state)
            return (
                final_state["messages"][-1].content,
                final_state.get("sql_query"),
                final_state.get("results")
            )
        except Exception as e:
            return f"Error processing query: {str(e)}", None, None

    def reset(self):
        """Reset the orchestrator state"""
        self.graph = create_graph()