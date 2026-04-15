# Deep Research Agent

A sophisticated AI-powered research agent built with LangGraph and LangChain that conducts deep, comprehensive research on any topic using hierarchical multi-agent orchestration.

## Overview

The Deep Research Agent is an autonomous system that breaks down complex research tasks into smaller, focused subtasks and delegates them to specialized research sub-agents. It uses Claude Sonnet as the language model and Tavily Search for information gathering, providing comprehensive research reports with proper citations.

### Key Features

- **Hierarchical Multi-Agent Architecture**: Main orchestrator agent delegates research tasks to specialized sub-agents
- **Parallel Research**: Concurrent research units for faster information gathering
- **Comprehensive Analysis**: Deep research with multiple iterations and thorough fact-checking
- **Structured Reports**: Generates well-organized final reports with citations
- **Interactive UI**: Streamlit-based web interface for easy interaction
- **Workflow Management**: Intelligent task planning and synthesis of findings

## Project Structure

```
.
├── research_agent/
│   ├── agent.py              # Main agent configuration and setup
│   ├── main.py               # CLI entry point for running the agent
│   ├── streamlit_app.py      # Web UI interface
│   ├── run_streamlit.sh      # Shell script to run Streamlit
│   ├── run_streamlit.bat     # Batch script to run Streamlit (Windows)
│   └── utils/
│       ├── __init__.py
│       ├── prompt.py         # System prompts and instructions
│       ├── tools.py          # Tool definitions (Tavily search)
│       └── state.py          # Agent state management
├── langgraph.json            # LangGraph configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Prerequisites

- Python 3.11 or higher
- Virtual environment (venv recommended)
- API Keys:
  - Claude API key (Anthropic)
  - Tavily Search API key

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd Deep-Research
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv-research
   venv-research\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv-research
   source venv-research/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with:
   ```
   ANTHROPIC_API_KEY=your_claude_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

## Usage

### Option 1: CLI Interface

Run the agent from the command line:

```bash
cd research_agent
python main.py
```

This will prompt you to enter a research query and return the findings in the console.

### Option 2: Web UI (Streamlit)

Launch the interactive web interface:

**Windows:**
```bash
cd research_agent
run_streamlit.bat
```

**macOS/Linux:**
```bash
cd research_agent
bash run_streamlit.sh
```

Or manually:
```bash
cd research_agent
streamlit run streamlit_app.py
```

The web interface will open at `http://localhost:8501`

## How It Works

### Research Workflow

1. **Planning**: The main agent creates a task breakdown for the research query
2. **Request Saving**: The research question is saved for reference
3. **Delegation**: Research tasks are delegated to specialized sub-agents working in parallel
4. **Synthesis**: Findings are consolidated with unified citations
5. **Report Generation**: A comprehensive report is written with proper structure and citations
6. **Verification**: The system verifies all aspects of the query have been addressed

### Agent Configuration

- **Main Agent**: 
  - Model: Claude Sonnet 4.6
  - Temperature: 0.0 (deterministic responses)
  - Tool: Tavily Search

- **Research Sub-Agent**:
  - Specializes in focused topic research
  - Handles one topic at a time
  - Maximum concurrent research units: 3
  - Maximum research iterations: 3

## Dependencies

Key libraries and frameworks:

- **LangChain**: Chain orchestration and model integration
- **LangGraph**: Stateful agent orchestration
- **DeepAgents**: Hierarchical multi-agent system
- **Claude (Anthropic)**: Primary language model
- **Tavily**: Web search tool for information gathering
- **Streamlit**: Web UI framework
- **BeautifulSoup4**: HTML parsing for search results

See `requirements.txt` for complete list of dependencies.

## Configuration

### Agent Parameters

Edit `research_agent/agent.py` to customize:

```python
max_concurrent_research_units = 3      # Number of parallel researchers
max_research_iterations = 3             # Maximum research depth per topic
```

### Model Configuration

Model, temperature, and other settings can be adjusted in `agent.py`:

```python
model = init_chat_model(model="claude-sonnet-4-6", temperature=0.0, streaming=False)
```

## Output

The agent generates:

- **Console Output**: Direct results in the terminal
- **final_report.md**: Comprehensive research report with:
  - Structured sections
  - Key findings
  - Consolidated citations
  - Evidence-based conclusions

- **research_request.md**: Saved copy of the research query

## Troubleshooting

### API Key Errors
Ensure your `.env` file is properly configured and in the root directory. The agent loads variables from:
- Environment variables
- `.env` file (via `python-dotenv`)

### No Results
- Check your Tavily API key is valid
- Verify internet connection
- Ensure your search query is specific enough

### Slow Performance
- Reduce `max_concurrent_research_units` for lower resource usage
- Reduce `max_research_iterations` for faster completion
- Ensure your API rate limits aren't exceeded

## Architecture Notes

The system uses a hierarchical agent architecture:

```
┌─────────────────────────────────┐
│    Main Orchestrator Agent      │
│  (Planning & Synthesis)         │
└──────────────┬──────────────────┘
               │
      ┌────────┼────────┐
      │        │        │
    ┌─▼─┐  ┌─▼─┐  ┌─▼─┐
    │ R1│  │ R2│  │ R3│  Research Sub-Agents
    └─┬─┘  └─┬─┘  └─┬─┘  (Parallel Research)
      │     │      │
      └─────┴──────┘
          │
      Tavily Search API
```

## Development

To extend the agent:

1. **Add new tools**: Modify `research_agent/utils/tools.py`
2. **Adjust prompts**: Edit `research_agent/utils/prompt.py`
3. **Customize state**: Modify `research_agent/utils/state.py`
4. **Extend agent logic**: Update `research_agent/agent.py`

## Support

For issues or questions, please refer to:
- LangChain Documentation: https://python.langchain.com/
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- Anthropic Claude Documentation: https://docs.anthropic.com/
- Tavily API Documentation: https://docs.tavily.com/
