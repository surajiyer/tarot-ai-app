from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

load_dotenv()
model = AzureChatOpenAI()


def is_text_about_subject(text: str, subject: str) -> bool:
    result = model.invoke(
        [
            HumanMessage(text),
            SystemMessage("Is this about " + subject + "? Just return one word, true or false in lowercase."),
        ]
    )
    return "true" in result.content


def complete_chat(messages: list[dict[str, str]] = None) -> dict[str, str]:
    messages = list(
        map(
            lambda m: (
                HumanMessage(m["content"])
                if m["role"] == "human"
                else AIMessage(m["content"])
                if m["role"] == "assistant"
                else SystemMessage(m["content"])
            ),
            messages,
        )
    )
    result = model.invoke(messages)
    return {"role": "assistant", "content": result.content}
