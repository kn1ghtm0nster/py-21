from enum import StrEnum


class BlackJackWinner(StrEnum):
    PLAYER = "Player wins!"
    DEALER = "Dealer wins!"
    TIE = "It's a tie!"