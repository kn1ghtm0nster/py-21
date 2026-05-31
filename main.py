from typing import List, Any

from core import (
    Card,
)
from games import BlackJackGame
from utils import (
    get_player_action,
    PlayerAction,
    print_welcome,
    print_message,
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
    print_welcome()
    print_message("Fetching a new deck of cards please wait...", style="bold cyan")

    play = True
    while play:
        game = BlackJackGame()
        game.start_game()

        print_message("\n--- Game Started ---", style="bold green")

        # player's turn
        while not game.player_stands:
            display_hand(game.player_hand.cards, "Your Hand:")
            player_score = game.player_hand.calculate_score()
            print_message(f"Your current score: {player_score}", style="bold yellow")

            action = get_player_action()
            match action:
                case PlayerAction.HIT.value:
                    game.player_hit()
                    if game.player_hand.calculate_score() > 21:
                        print_message("\n🎯 BUST! Better luck next time!", style="bold red")
                        break
                case PlayerAction.STAND.value:
                    game.player_stands = True
                case PlayerAction.DOUBLE.value:
                    game.player_doubles_down()
                    if game.player_hand.calculate_score() > 21:
                        print_message("\n🎯 BUST! Better luck next time!", style="bold red")
                        break

        player_score = game.player_hand.calculate_score()
        # it is now the dealer's turn IF the player hasn't already busted
        if player_score <= 21:
            print_message("\n--- Dealer's Turn ---", style="bold cyan")
            game.rule.dealer_attempts_win()
            display_hand(game.dealer_hand.cards, "Dealer's Hand:")
            print_message(f"Dealer's score: {game.dealer_hand.calculate_score()}", style="bold yellow")

        # now we determine the winner
        winner = game.rule.determine_winner()
        print_message(f"\n🏆 Winner: {winner} 🏆", style="bold magenta")

        again = input("\nPlay again? (Y/N): ").strip().upper()
        play = again == "Y"

    # user decides to quit
    print_message("\nThanks for playing! Goodbye!", style="bold cyan")

if __name__ == "__main__":
    main()