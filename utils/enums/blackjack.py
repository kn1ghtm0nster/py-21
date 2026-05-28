from enum import StrEnum


class BlackJackWinner(StrEnum):
    PLAYER = "Player wins! Play again? (Y/N)"
    DEALER = "Dealer wins! Play again? (Y/N)"
    TIE = "It's a tie! Play again? (Y/N)"