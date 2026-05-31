from typing import List, Dict, Any
from abc import ABC, abstractmethod

from .api_client import DeckAPIClient
from utils import BlackJackWinner


class Card:

    def __init__(self, suit: str, rank: str, image: str):
        self.suit = suit
        self.rank = rank
        self.image = image

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def display_image(self) -> str:
        return self.image


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


class Hand:

    def __init__(self, deck: Deck, cards: List[Card] | None = None):
        self.cards = cards or []
        self.deck = deck

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


class Rule(ABC):

    @abstractmethod
    def determine_winner(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")


class BlackJackRule(Rule):

    def __init__(self, deck: Deck):
        self.deck = deck
        self.player_hand = Hand(deck=self.deck)
        self.dealer_hand = Hand(deck=self.deck)

    def determine_winner(self) -> str:
        player_score = self.player_hand.calculate_score()
        dealer_score = self.dealer_hand.calculate_score()

        if player_score > 21:
            return BlackJackWinner.DEALER.value
        elif dealer_score > 21:
            return BlackJackWinner.PLAYER.value
        elif player_score > dealer_score:
            return BlackJackWinner.PLAYER.value
        elif dealer_score > player_score:
            return BlackJackWinner.DEALER.value
        else:
            return BlackJackWinner.TIE.value

    def dealer_attempts_win(self) -> None:
        dealer_score = self.dealer_hand.calculate_score()

        while dealer_score < 17:
            self.dealer_hand.draw_card()
            dealer_score = self.dealer_hand.calculate_score()