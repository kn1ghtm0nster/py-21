from typing import List, Dict, Any

from core import DeckAPIClient

class Card:

    def __init__(self, suit: str, rank: str, image: str):
        self.suit = suit
        self.rank = rank
        self.image = image

    def display_image(self) -> str:
        return self.image

class Hand:
    pass

class Deck:

    def __init__(self):
        self.deck_id = None
        self.remaining = None
        self.shuffled = False
        self.api_client = DeckAPIClient()

    def get_new_deck(self, deck_count: int = 1) -> Dict[str, Any]:
        response = self.api_client.get_new_deck(deck_count)
        self.deck_id = response['deck_id']
        self.remaining = response['remaining']
        self.shuffled = response['shuffled']
        return response

    def shuffle_deck(self) -> None:
        if self.deck_id:
            response = self.api_client.shuffle_deck(self.deck_id)
            self.shuffled = response['shuffled']
            self.remaining = response['remaining']
        else:
            raise ValueError("Deck ID is not set. Please get a new deck first.")

    def draw_card(self, count: int = 1) -> List[Card]:
        if self.deck_id:
            response = self.api_client.draw_card(self.deck_id, count)
            self.remaining = response['remaining']
            cards = []
            for card_info in response['cards']:
                card = Card(suit=card_info['suit'], rank=card_info['value'], image=card_info['image'])
                cards.append(card)
            return cards
        else:
            raise ValueError("Deck ID is not set. Please get a new deck first.")

class Rule:
    pass