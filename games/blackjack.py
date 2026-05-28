from core import (
    BlackJackRule,
    Deck
)


class BlackJackGame:

    def __init__(self):
        self.deck = Deck()
        self.rule = BlackJackRule(self.deck)
        self.player_hand = self.rule.player_hand
        self.dealer_hand = self.rule.dealer_hand
        self.winner = None
        self.player_stands = False
        self.player_double_down = False

    def start_game(self) -> None:
        self.deck.get_new_deck()
        self.deal_cards()

    def deal_cards(self) -> None:
        self.player_hand.draw_card(2)
        self.dealer_hand.draw_card(2)

    def player_hit(self) -> None:
        self.player_hand.draw_card(1)

    def determine_winner(self) -> None:
        self.winner = self.rule.determine_winner()

    def play_again(self) -> None:
        self.player_hand.cards = []
        self.dealer_hand.cards = []
        self.winner = None
        self.start_game()

    def player_stand(self) -> None:
        self.player_stands = True
        self.rule.dealer_attempts_win()
        self.determine_winner()

    def player_doubles_down(self) -> None:
        self.player_double_down = True
        self.player_hand.draw_card(1)
        self.player_stands = True