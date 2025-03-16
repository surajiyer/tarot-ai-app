from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

load_dotenv()
model = AzureChatOpenAI()


def complete_chat(messages: list[dict[str, str]] = None) -> str:
    messages = list(
        map(
            lambda m: (
                HumanMessage(m["message"])
                if m["user"] == "human"
                else AIMessage(m["message"])
                if m["user"] == "assistant"
                else SystemMessage(m["message"])
            ),
            messages,
        )
    )
    print(messages)
    result = model.invoke(messages)
    return result.content
