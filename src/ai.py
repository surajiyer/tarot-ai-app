from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI

from tarot import random_pick_tarot_cards

load_dotenv()
llm = AzureChatOpenAI()


@tool
def tool_draw_tarot_cards(number_of_cards: int = 3, with_replacement=False, reversed_allowed=False):
    """
    Randomly pick tarot cards from the deck.
    Args:
        number_of_cards (int): Number of cards to pick. Defaults to 3.
        with_replacement (bool): Whether to sample with replacement. Defaults to False.
        reversed_allowed (bool): Whether to allow reversed cards. Defaults to False.
    Returns:
        list[str]: List of tarot cards.
    """
    return str(random_pick_tarot_cards(number_of_cards, with_replacement, reversed_allowed))


tools = [tool_draw_tarot_cards]
llm_with_tools = llm.bind_tools(tools)


def is_conversation_about_subject(messages: list[dict[str, str]]) -> bool:
    """
    Check if the entire conversation is about tarot-related topics.

    Args:
        messages: List of message dictionaries with 'role' and 'content' keys

    Returns:
        bool: True if the conversation is on topic, False otherwise
    """
    # Extract only user messages for analysis
    user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]

    if not user_messages:
        return True  # No user messages yet

    # Join the recent messages (using last 10 or all if fewer) to check context
    recent_messages = user_messages[-10:] if len(user_messages) > 3 else user_messages
    conversation_text = "\n".join(recent_messages)

    tarot_topics = [
        "tarot cards",
        "tarot readings",
        "divination",
        "card meanings",
        "spreads",
        "major arcana",
        "minor arcana",
        "card interpretations",
        "spiritual guidance",
        "fortune telling",
        "tarot spreads",
        "card symbolism",
    ]

    # Add examples for better context assessment
    result = llm.invoke(
        [
            SystemMessage(
                f"You are a strict content filter for a tarot reading application. "
                f"Determine if the conversation is related to any of these topics: {', '.join(tarot_topics)}. "
                f"Users should only discuss tarot readings, interpretations, spiritual guidance, or related topics. "
                f"Conversations about other topics like general life advice, coding help, weather, news, etc. "
                f"should be rejected unless they're specifically in the context of tarot readings. "
                f"Return ONLY 'true' if the conversation is about tarot or related topics, or 'false' otherwise."
            ),
            HumanMessage("Here is the conversation so far:\n" + conversation_text),
        ]
    )
    return "true" in result.content.lower()


def complete_chat(messages: list[dict[str, str]] = None) -> dict[str, str]:
    messages = list(
        map(
            lambda m: (
                HumanMessage(m["content"])
                if m["role"] == "user"
                else AIMessage(m["content"])
                if m["role"] == "assistant"
                else SystemMessage(m["content"])
            ),
            messages,
        )
    )
    messages.insert(
        0,
        SystemMessage(
            "You are a knowledgeable and insightful tarot reader. Your goal is to provide meaningful and accurate tarot "
            "readings, interpretations, and spiritual guidance to users. Use your expertise to help users understand the "
            "symbolism and meanings of the tarot cards they draw. Offer thoughtful, compassionate yet firm and truthful "
            "advice based on the cards and their positions in the spread. Remember to be respectful and considerate in "
            "your responses, and ensure that your guidance is always related to tarot readings. You will speak mystical "
            "and draw cards when necessary. Otherwise, you will extend your reading of existing cards to provide more "
            "context to your answers."
        ),
    )
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    for tool_call in ai_msg.tool_calls:
        selected_tool = {"tool_draw_tarot_cards": tool_draw_tarot_cards}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)
    final_result = llm_with_tools.invoke(messages)
    return {"role": "assistant", "content": final_result.content}
