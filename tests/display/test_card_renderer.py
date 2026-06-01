import pytest

from display import render_card
from core import Card

def test_render_card_spades_ace():
    card = Card(suit="SPADES", rank="ACE", image="https://example.com/ace_of_spades.png")
    result = render_card(card)
    assert "A" in result
    assert "♠" in result
    assert "┌─────────┐" in result

def test_render_card_diamond_ace():
    card = Card(suit="DIAMONDS", rank="ACE", image="https://example.com/ace_of_diamonds.png")
    result = render_card(card)
    assert "A" in result
    assert "♦" in result
    assert "┌─────────┐" in result

def test_render_card_club_ace():
    card = Card(suit="CLUBS", rank="ACE", image="https://example.com/ace_of_clubs.png")
    result = render_card(card)
    assert "A" in result
    assert "♣" in result
    assert "┌─────────┐" in result

def test_render_card_heart_ace():
    card = Card(suit="HEARTS", rank="ACE", image="https://example.com/ace_of_hearts.png")
    result = render_card(card)
    assert "A" in result
    assert "♥" in result
    assert "┌─────────┐" in result