import random

from langchain_core.tools import tool

MAJOR_ARCANA = [
    "The Fool (0)",
    "The Magician (I)",
    "The High Priestess (II)",
    "The Empress (III)",
    "The Emperor (IV)",
    "The Hierophant (V)",
    "The Lovers (VI)",
    "The Chariot (VII)",
    "Strength (VIII)",
    "The Hermit (IX)",
    "The Wheel of Fortune (X)",
    "Justice (XI)",
    "The Hanged Man (XII)",
    "Death (XIII)",
    "Temperance (XIV)",
    "The Devil (XV)",
    "The Tower (XVI)",
    "The Star (XVII)",
    "The Moon (XVIII)",
    "The Sun (XIX)",
    "Judgment (XX)",
    "The World (XXI)",
]

SUIT_OF_WANDS = [
    "Ace of Wands",
    "2 of Wands",
    "3 of Wands",
    "4 of Wands",
    "5 of Wands",
    "6 of Wands",
    "7 of Wands",
    "8 of Wands",
    "9 of Wands",
    "10 of Wands",
    "Page of Wands",
    "Knight of Wands",
    "Queen of Wands",
    "King of Wands",
]

SUIT_OF_PENTACLES = [
    "Ace of Pentacles",
    "2 of Pentacles",
    "3 of Pentacles",
    "4 of Pentacles",
    "5 of Pentacles",
    "6 of Pentacles",
    "7 of Pentacles",
    "8 of Pentacles",
    "9 of Pentacles",
    "10 of Pentacles",
    "Page of Pentacles",
    "Knight of Pentacles",
    "Queen of Pentacles",
    "King of Pentacles",
]


SUIT_OF_SWORDS = [
    "Ace of Swords",
    "2 of Swords",
    "3 of Swords",
    "4 of Swords",
    "5 of Swords",
    "6 of Swords",
    "7 of Swords",
    "8 of Swords",
    "9 of Swords",
    "10 of Swords",
    "Page of Swords",
    "Knight of Swords",
    "Queen of Swords",
    "King of Swords",
]


SUIT_OF_CUPS = [
    "Ace of Cups",
    "2 of Cups ",
    "3 of Cups",
    "4 of Cups",
    "5 of Cups",
    "6 of Cups",
    "7 of Cups",
    "8 of Cups",
    "9 of Cups",
    "10 of Cups",
    "Page of Cups",
    "Knight of Cups",
    "Queen of Cups",
    "King of Cups",
]


@tool
def random_pick_tarot_cards(number_of_cards: int = 3, with_replacement=False, reversed_allowed=False) -> list[str]:
    """
    Randomly pick tarot cards from the deck.
    Args:
        number_of_cards (int): Number of cards to pick. Defaults to 3.
        with_replacement (bool): Whether to sample with replacement. Defaults to False.
        reversed_allowed (bool): Whether to allow reversed cards. Defaults to False.
    Returns:
        list[str]: List of tarot cards.
    """
    cards = MAJOR_ARCANA + SUIT_OF_WANDS + SUIT_OF_PENTACLES + SUIT_OF_SWORDS + SUIT_OF_CUPS
    if with_replacement:
        cards = random.choices(cards, k=number_of_cards)
    else:
        cards = random.sample(cards, number_of_cards)
    if reversed_allowed:
        cards = [card + " (reversed)" if random.random() < 0.5 else card for card in cards]
    return cards
