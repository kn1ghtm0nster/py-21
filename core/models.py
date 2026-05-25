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

    def __init__(self, cards: List[Card] = []):
        self.cards = cards
        self.deck = Deck()

    def calculate_score(self) -> int:
        score = 0
        ace_count = 0

        for card in self.cards:
            if card.rank in ['JACK', 'QUEEN', 'KING', 'J', 'Q', 'K']:
                score += 10
            elif card.rank == 'ACE':
                score += 11
                ace_count += 1
            else:
                score += int(card.rank)

        # Adjust for Aces if score is over 21
        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1

        return score

    def draw_card(self, count: int = 1) -> None:
        new_cards = self.deck.draw_card(count)
        self.cards.extend(new_cards)

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