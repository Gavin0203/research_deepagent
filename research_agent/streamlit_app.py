import streamlit as st
import os
import dotenv
from datetime import datetime
from langchain.messages import HumanMessage
from agent import agent

# Configure page
st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
dotenv.load_dotenv()

# Custom CSS
st.markdown("""
<style>
    .research-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5em;
    }
    .status-box {
        padding: 1em;
        border-radius: 0.5em;
        margin: 0.5em 0;
    }
    .status-pending {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .status-processing {
        background-color: #cfe2ff;
        border-left: 4px solid #0d6efd;
    }
    .status-complete {
        background-color: #d1e7dd;
        border-left: 4px solid #198754;
    }
    .source-link {
        text-decoration: none;
        color: #0d6efd;
    }
    .source-link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")
    
    st.subheader("Model Configuration")
    model_info = st.info(f"🤖 **Model:** Claude Sonnet 4.6\n\n🌡️ **Temperature:** 0.0\n\n📅 **Current Date:** {datetime.now().strftime('%Y-%m-%d')}")
    
    st.markdown("---")
    st.subheader("Research Parameters")
    
    max_concurrent = st.slider(
        "Max Concurrent Research Units",
        min_value=1,
        max_value=5,
        value=3,
        help="Number of research tasks to run in parallel"
    )
    
    max_iterations = st.slider(
        "Max Research Iterations",
        min_value=1,
        max_value=10,
        value=3,
        help="Maximum number of research iterations per sub-agent"
    )
    st.markdown("---")
    st.caption("💡 Tip: Use fewer concurrent units and iterations for faster results")

# Main content
st.markdown('<div class="research-header">🔍 Deep Research Agent</div>', unsafe_allow_html=True)
st.markdown("Power your research with AI-driven insights and comprehensive web searches")
st.markdown("---")

# Research input
col1, col2 = st.columns([4, 1])
with col1:
    user_query = st.text_input(
        "Enter your research question:",
        placeholder="e.g., What are the latest advancements in quantum computing?",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button("🚀 Research", use_container_width=True)

st.markdown("---")

# Initialize session state
if "research_state" not in st.session_state:
    st.session_state.research_state = {
        "status": None,
        "messages": [],
        "report": None,
        "error": None,
        "query": None
    }

# Handle research
if search_button:
    if not user_query.strip():
        st.error("❌ Please enter a research question")
    else:
        st.session_state.research_state["query"] = user_query
        
        # Create placeholders for real-time updates
        status_placeholder = st.empty()
        output_placeholder = st.empty()
        
        try:
            with status_placeholder.container():
                st.markdown('<div class="status-box status-processing">⏳ Research in progress...</div>', unsafe_allow_html=True)
            
            # Run the agent
            response = agent.invoke(
                {
                    "messages": [HumanMessage(content=user_query)]
                }
            )
            
            # Extract and store messages
            st.session_state.research_state["messages"] = response.get("messages", [])
            st.session_state.research_state["status"] = "complete"
            
            with status_placeholder.container():
                st.markdown('<div class="status-box status-complete">✅ Research complete!</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.session_state.research_state["status"] = "error"
            st.session_state.research_state["error"] = str(e)
            with status_placeholder.container():
                st.error(f"❌ Error during research: {str(e)}")

# Display results
if st.session_state.research_state["status"]:
    if st.session_state.research_state["status"] == "complete" and st.session_state.research_state["messages"]:
        st.markdown("---")
        st.subheader("📊 Research Results")
        
        # Separate tabs for different views
        tab1, tab2, tab3 = st.tabs(["📄 Full Report", "💬 Messages", "🔗 Sources"])
        
        with tab1:
            # Display full content
            st.markdown("### Research Findings")
            for message in st.session_state.research_state["messages"]:
                if hasattr(message, "content") and message.content:
                    # Check if message contains report-like content
                    content = message.content
                    try:
                        if content.strip():
                            st.markdown(content)

                            # Add copy button for full content
                            col1, col2 = st.columns([3, 1])
                            with col2:
                                st.button(
                                    "📋 Copy",
                                    key=f"copy_{id(message)}",
                                    help="Copy this content to clipboard"
                                )
                    except Exception as e:
                        st.markdown(content)
                        # Add copy button for full content
                        col1, col2 = st.columns([3, 1])
                        with col2:
                            st.button(
                                "📋 Copy",
                                key=f"copy_{id(message)}",
                                help="Copy this content to clipboard"
                            )
        with tab2:
            st.markdown("### Agent Messages")
            for i, message in enumerate(st.session_state.research_state["messages"], 1):
                if hasattr(message, "content") and message.content:
                    with st.expander(f"Message {i}", expanded=(i == 1)):
                        st.text_area(
                            "Content:",
                            value=message.content,
                            height=150,
                            disabled=True,
                            label_visibility="collapsed"
                        )
        
        with tab3:
            st.markdown("### Sources & Citations")
            # Extract and display sources from the content
            sources_found = False
            for message in st.session_state.research_state["messages"]:
                if hasattr(message, "content") and "Sources" in message.content:
                    # Extract sources section
                    content = message.content
                    if "### Sources" in content:
                        sources_section = content.split("### Sources")[1]
                        st.markdown("#### Referenced Sources")
                        st.markdown(sources_section)
                        sources_found = True
            
            if not sources_found:
                st.info("📌 Sources will appear here if the research includes citations")
        
        # Research metadata
        st.markdown("---")
        st.markdown("### 📋 Research Metadata")
        metadata_col1, metadata_col2, metadata_col3 = st.columns(3)
        
        with metadata_col1:
            st.metric("Query", st.session_state.research_state["query"][:50] + "..." if len(st.session_state.research_state["query"]) > 50 else st.session_state.research_state["query"])
        
        with metadata_col2:
            st.metric("Status", "✅ Complete")
        
        with metadata_col3:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.metric("Timestamp", timestamp)
        
        # Export options
        st.markdown("---")
        st.subheader("💾 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            full_content = "\n\n".join([
                msg.content for msg in st.session_state.research_state["messages"]
                if hasattr(msg, "content") and msg.content
            ])
            st.download_button(
                label="📥 Download as Markdown",
                data=full_content,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
        
        with col2:
            st.download_button(
                label="📥 Download as Text",
                data=full_content,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        with col3:
            if st.button("🔄 New Research", use_container_width=True):
                st.session_state.research_state = {
                    "status": None,
                    "messages": [],
                    "report": None,
                    "error": None,
                    "query": None
                }
                st.rerun()

# Information section
with st.expander("ℹ️ How This Works"):
    st.markdown("""
    ### Deep Research Agent Features
    
    - **Multi-Agent Research**: Delegates complex queries to specialized sub-agents
    - **Web Search Integration**: Uses Tavily API for up-to-date web searches
    - **Parallel Processing**: Executes multiple research tasks concurrently
    - **Citation Tracking**: Maintains source attribution throughout research
    - **Comprehensive Reporting**: Generates well-structured research reports
    
    ### Best Practices
    
    1. **Be Specific**: More detailed queries lead to better research results
    2. **Ask Questions**: Frame your query as a question for optimal results
    3. **Avoid Too Complex Queries**: Break down very complex topics into simpler questions
    4. **Review Sources**: Always check the provided sources for accuracy
    
    ### Troubleshooting
    
    - **API Errors**: Ensure TAVILY_API_KEY and ANTHROPIC_API_KEY are set
    - **Slow Results**: Reduce concurrent research units for faster processing
    - **Low Quality Results**: Try rephrasing your question more specifically
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
    <small>🚀 Powered by LangGraph | 🤖 Claude Sonnet 4.6 | 🔍 Tavily Search</small>
    </div>
    """,
    unsafe_allow_html=True
)
