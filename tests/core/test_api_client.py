import pytest

from core import DeckAPIClient


@pytest.fixture
def api_client():
    return DeckAPIClient()

@pytest.fixture
def mock_new_deck_response():
    return {
        "success": True,
        "deck_id": "3p40paa87x90",
        "remaining": 52,
        "shuffled": True
    }

@pytest.fixture
def mock_shuffle_deck_response():
    return {
        "success": True,
        "deck_id": "3p40paa87x90",
        "remaining": 40,
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
            }
        ],
        "deck_id": "3p40paa87x90",
        "remaining": 51
    }

class TestDeckAPIClient:
    # NOTE: These tests are designed to test the API client methods in isolation, 
    # without making actual API calls. We use fixtures to mock the responses from the API.

    def test_instance_creation(self, api_client):
        assert isinstance(api_client, DeckAPIClient)

    def test_get_new_deck(self, api_client, mock_new_deck_response, monkeypatch):
        # Mock the API response
        monkeypatch.setattr(api_client, "get_new_deck", lambda deck_count=1: mock_new_deck_response)

        response = api_client.get_new_deck()
        assert response['success'] is True
        assert 'deck_id' in response
        assert 'remaining' in response
        assert 'shuffled' in response

    def test_shuffle_deck(self, api_client, mock_shuffle_deck_response, monkeypatch):
        # Mock the API response
        monkeypatch.setattr(api_client, "shuffle_deck", lambda deck_id: mock_shuffle_deck_response)

        response = api_client.shuffle_deck(deck_id="3p40paa87x90")
        assert response['success'] is True
        assert 'deck_id' in response
        assert 'remaining' in response
        assert 'shuffled' in response

    def test_draw_card(self, api_client, mock_draw_card_response, monkeypatch):
        # Mock the API response
        monkeypatch.setattr(api_client, "draw_card", lambda deck_id, count=1: mock_draw_card_response)

        response = api_client.draw_card(deck_id="3p40paa87x90")
        assert response['success'] is True
        assert 'cards' in response
        assert 'deck_id' in response
        assert 'remaining' in response