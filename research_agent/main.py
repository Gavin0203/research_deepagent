from langchain.messages import HumanMessage
from agent import agent
import dotenv

dotenv.load_dotenv()

if __name__ == "__main__":
    response = agent.invoke(
        {
            "messages" : [HumanMessage(
                                content="What are the latest advancements in quantum computing? Give a short summary."
                            )
                        ]
        }
    )
    for message in response.get("messages",[]):
        if hasattr(message,"content") and message.content:
            print(message.content)