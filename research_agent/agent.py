from datetime import datetime
import dotenv
import os 

from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

from utils.prompt import RESEARCHER_INSTRUCTIONS, RESEARCH_WORKFLOW_INSTRUCTIONS, SUBAGENT_DELEGATION_INSTRUCTIONS
from utils.tools import tavily_search

max_concurrent_research_units = 3
max_research_iterations = 3

dotenv.load_dotenv()

current_date = datetime.now().strftime("%Y-%m-%d")

model = init_chat_model(model="claude-sonnet-4-6",temperature=0.0,streaming=False)

INSTRUCTIONS = (
    RESEARCH_WORKFLOW_INSTRUCTIONS + "\n\n" + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
        max_concurrent_research_units=max_concurrent_research_units,
        max_researcher_iterations=max_research_iterations
    )
)

research_sub_agent = {
    "name" : "research-agent",
    "description" : "Delegate research to the sub-agent.Handles only one topic at a time.",
    "system_prompt" : RESEARCHER_INSTRUCTIONS.format(date=current_date),
    "tools" : [tavily_search]
}

agent = create_deep_agent(
    model=model,
    tools=[tavily_search],
    system_prompt=INSTRUCTIONS,
    subagents=[research_sub_agent]
)