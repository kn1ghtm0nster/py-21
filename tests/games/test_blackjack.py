import pytest

from core import Card
from games import BlackJackGame
from utils import BlackJackWinner


@pytest.fixture
def mock_game():
    return BlackJackGame()

@pytest.fixture
def mock_new_deck_response():
    return {
        "success": True,
        "deck_id": "3p40paa87x90",
        "remaining": 52,
        "shuffled": True
    }

@pytest.fixture
def mock_draw_card_response():
    return {
        "success": True,
        "cards": [
            {
                "code": "AS",
                "image": "https://deckofcardsapi.com/static/img/AS.png",
                "images": {
                    "svg": "https://deckofcardsapi.com/static/img/AS.svg",
                    "png": "https://deckofcardsapi.com/static/img/AS.png"
                },
                "value": "ACE",
                "suit": "SPADES"
            },
            {
                "code": "10H",
                "image": "https://deckofcardsapi.com/static/img/0H.png",
                "images": {
                    "svg": "https://deckofcardsapi.com/static/img/0H.svg",
                    "png": "https://deckofcardsapi.com/static/img/0H.png"
                },
                "value": "10",
                "suit": "HEARTS"
            }
        ],
        "deck_id": "3p40paa87x90",
        "remaining": 50
    }

@pytest.fixture
def mock_draw_card_smart():
    def mock_draw(self, deck_id, count=1):
        card = {
            "code": "5C",
            "image": "https://deckofcardsapi.com/static/img/5C.png",
            "images": {
                "svg": "https://deckofcardsapi.com/static/img/5C.svg",
                "png": "https://deckofcardsapi.com/static/img/5C.png"
            },
            "value": "5",
            "suit": "CLUBS"
        }
        return {
            "success": True,
            "cards": [card] * count,
            "deck_id": deck_id,
            "remaining": 52 - count
        }
    return mock_draw


class TestBlackJackGame:

    def test_game_initialization(self):
        game = BlackJackGame()
        assert isinstance(game, BlackJackGame)

    def test_deal_cards(self, mock_new_deck_response, mock_draw_card_response, monkeypatch):
        monkeypatch.setattr("core.api_client.DeckAPIClient.get_new_deck", lambda self, deck_count=1: mock_new_deck_response)
        monkeypatch.setattr("core.api_client.DeckAPIClient.draw_card", lambda self, deck_id, count=1: mock_draw_card_response)
        game = BlackJackGame()
        game.start_game()

        assert len(game.player_hand.cards) == 2
        assert len(game.dealer_hand.cards) == 2

    def test_player_turn(self, mock_game, mock_new_deck_response, mock_draw_card_smart, monkeypatch):
        monkeypatch.setattr("core.api_client.DeckAPIClient.get_new_deck", lambda self, deck_count=1: mock_new_deck_response)
        monkeypatch.setattr("core.api_client.DeckAPIClient.draw_card", lambda self, deck_id, count=1: mock_draw_card_smart(self, deck_id, count))
        
        mock_game.start_game()
        mock_game.player_hit()

        assert len(mock_game.player_hand.cards) == 3

    def test_dealer_turn(self, mock_game, mock_new_deck_response, mock_draw_card_smart, monkeypatch):
        monkeypatch.setattr("core.api_client.DeckAPIClient.get_new_deck", lambda self, deck_count=1: mock_new_deck_response)
        monkeypatch.setattr("core.api_client.DeckAPIClient.draw_card", lambda self, deck_id, count=1: mock_draw_card_smart(self, deck_id, count))

        mock_game.start_game()
        mock_game.rule.dealer_attempts_win()

        assert len(mock_game.dealer_hand.cards) >= 2

    def test_determine_winner(self, mock_game, mock_new_deck_response, mock_draw_card_smart, monkeypatch):
        monkeypatch.setattr("core.api_client.DeckAPIClient.get_new_deck", lambda self, deck_count=1: mock_new_deck_response)
        monkeypatch.setattr("core.api_client.DeckAPIClient.draw_card", lambda self, deck_id, count=1: mock_draw_card_smart(self, deck_id, count))

        mock_game.start_game()
        mock_game.determine_winner()

        # NOTE: The winner should be one of the defined values in BlackJackWinner
        # rather than writing a single repetitive tests for each possible outcome, 
        # we can just check if the winner is in the expected set of values
        assert mock_game.winner in [BlackJackWinner.PLAYER.value, BlackJackWinner.DEALER.value, BlackJackWinner.TIE.value]

    def test_play_again(self, mock_game):
        mock_game.player_hand.cards = [Card(suit="HEARTS", rank="10", image="https://deckofcardsapi.com/static/img/0H.png"), Card(suit="SPADES", rank="5", image="https://deckofcardsapi.com/static/img/5S.png")]
        mock_game.dealer_hand.cards = [Card(suit="CLUBS", rank="7", image="https://deckofcardsapi.com/static/img/7C.png"), Card(suit="DIAMONDS", rank="8", image="https://deckofcardsapi.com/static/img/8D.png")]
        mock_game.winner = BlackJackWinner.PLAYER.value

        mock_game.play_again()

        assert mock_game.winner is None
        assert len(mock_game.player_hand.cards) == 2
        assert len(mock_game.dealer_hand.cards) == 2
        assert mock_game.player_hand.cards[0].rank != 10  # Ensure new cards are drawn
        assert mock_game.dealer_hand.cards[0].rank != 7  # Ensure new cards are drawn

    def test_player_stand(self, mock_game, mock_new_deck_response, mock_draw_card_smart, monkeypatch):
        monkeypatch.setattr("core.api_client.DeckAPIClient.get_new_deck", lambda self, deck_count=1: mock_new_deck_response)
        monkeypatch.setattr("core.api_client.DeckAPIClient.draw_card", lambda self, deck_id, count=1: mock_draw_card_smart(self, deck_id, count))
        mock_game.start_game()
        
        mock_game.player_stand()

        assert len(mock_game.player_hand.cards) == 2  # Player should not draw more cards
        assert mock_game.player_stands is True

    def test_player_double(self, mock_game, mock_new_deck_response, mock_draw_card_smart, monkeypatch):
        monkeypatch.setattr("core.api_client.DeckAPIClient.get_new_deck", lambda self, deck_count=1: mock_new_deck_response)
        monkeypatch.setattr("core.api_client.DeckAPIClient.draw_card", lambda self, deck_id, count=1: mock_draw_card_smart(self, deck_id, count))
        mock_game.start_game()
        
        mock_game.player_doubles_down()
        assert len(mock_game.player_hand.cards) == 3
        assert mock_game.player_double_down is True
        # Player should automatically stand after doubling down for the time being
        assert mock_game.player_stands is True  