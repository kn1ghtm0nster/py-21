import pytest

from core import Card
from main import display_cards_horizontal, display_hand


def test_display_cards_horizontal():
    cards = [
        Card(suit="SPADES", rank="ACE", image="https://example.com/ace_of_spades.png"),
        Card(suit="HEARTS", rank="10", image="https://example.com/10_of_hearts.png"),
    ]
    result = display_cards_horizontal(cards)
    assert "A" in result
    assert "10" in result
    assert "♠" in result
    assert "♥" in result
    assert "┌─────────┐" in result
    assert len(result.split('\n')) == 7

def test_display_hand(capsys):
    cards = [
        Card(suit="SPADES", rank="ACE", image="https://example.com/ace_of_spades.png"),
        Card(suit="HEARTS", rank="10", image="https://example.com/10_of_hearts.png"),
    ]
    display_hand(cards, "Test Hand:")
    result = capsys.readouterr()
    assert "Test Hand:" in result.out
    assert "A" in result.out
    assert "10" in result.out
    assert "♠" in result.out
    assert "♥" in result.out
    assert "┌─────────┐" in result.out
    assert len(result.out.split('\n')) == 10  # 10 lines of cards