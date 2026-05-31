from typing import List, Any

from core import (
    Card,
)
from games import BlackJackGame
from utils import (
    get_player_action,
    PlayerAction
)
from display import render_card

def display_cards_horizontal(cards: List[Card]) -> str:
    """
    Displays cards horizontally as ASCII art.
    """
    
    card_arts = [render_card(card).strip().split('\n') for card in cards]
    # Strip each line to remove leading spaces
    # avoids weird spacing when cards are displayed horizontally
    card_arts = [[line.strip() for line in card] for card in card_arts]
    
    lines = []
    for line_idx in range(len(card_arts[0])):
        line = "  ".join(card_arts[i][line_idx] for i in range(len(cards)))
        lines.append(line)
    return "\n".join(lines)

def display_hand(cards:List[Card], title: str) -> None:
    """Displays cards in a hand as readable strings."""
    print(f"\n{title}")
    print(display_cards_horizontal(cards))


def main():
    print("Welcome to Blackjack!")
    print("Fetching a new deck of cards please wait...")

    play = True
    while play:
        game = BlackJackGame()
        game.start_game()

        print("\n--- Game Started ---")

        # player's turn
        while not game.player_stands:
            display_hand(game.player_hand.cards, "Your Hand:")
            player_score = game.player_hand.calculate_score()
            print(f"Your current score: {player_score}")

            action = get_player_action()
            match action:
                case PlayerAction.HIT.value:
                    game.player_hit()
                    if game.player_hand.calculate_score() > 21:
                        print("\n🎯 BUST! Better luck next time!")
                        break
                case PlayerAction.STAND.value:
                    game.player_stands = True
                case PlayerAction.DOUBLE.value:
                    game.player_doubles_down()
                    if game.player_hand.calculate_score() > 21:
                        print("\n🎯 BUST! Better luck next time!")
                        break

        player_score = game.player_hand.calculate_score()
        # it is now the dealer's turn IF the player hasn't already busted
        if player_score <= 21:
            print("\n--- Dealer's Turn ---")
            game.rule.dealer_attempts_win()
            display_hand(game.dealer_hand.cards, "Dealer's Hand:")
            print(f"Dealer's score: {game.dealer_hand.calculate_score()}")

        # now we determine the winner
        winner = game.rule.determine_winner()
        print(f"\n🏆 Winner: {winner} 🏆")

        again = input("\nPlay again? (Y/N): ").strip().upper()
        play = again == "Y"

    # user decides to quit
    print("\nThanks for playing! Goodbye!")

if __name__ == "__main__":
    main()