import pytest

from core import (
    Card,
    Hand,
    Deck,
    DeckAPIClient,
    BlackJackRule,
)

@pytest.fixture
def mock_api():
    return DeckAPIClient()

@pytest.fixture
def mock_deck():
    return Deck()

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


class TestCard:

    def test_card_initialization(self):
        card = Card(suit = "HEARTS", rank = "10", image = "https://deckofcardsapi.com/static/img/0H.png")

        assert card.suit == "HEARTS"
        assert card.rank == "10"
        assert card.image == "https://deckofcardsapi.com/static/img/0H.png"

    def test_display_image(self):
        card = Card(suit = "HEARTS", rank = "10", image = "https://deckofcardsapi.com/static/img/0H.png")

        assert card.display_image() == "https://deckofcardsapi.com/static/img/0H.png"


class TestDeck:

    def test_deck_instance(self):
        deck = Deck()
        assert isinstance(deck, Deck)

    def test_get_new_deck(self, mock_api, mock_new_deck_response, monkeypatch):
        # Mock the API response
        monkeypatch.setattr("core.api_client.DeckAPIClient.get_new_deck", lambda self, deck_count=1: mock_new_deck_response)

        deck = Deck()
        response = deck.get_new_deck()

        assert response['success'] is True
        assert deck.deck_id == "3p40paa87x90"
        assert deck.remaining == 52
        assert deck.shuffled is True

    def test_shuffle_deck(self, mock_api, mock_new_deck_response, mock_shuffle_deck_response, monkeypatch):
        monkeypatch.setattr("core.api_client.DeckAPIClient.get_new_deck", lambda self, deck_count=1: mock_new_deck_response)
        monkeypatch.setattr("core.api_client.DeckAPIClient.shuffle_deck", lambda self, deck_id: mock_shuffle_deck_response)

        deck = Deck()
        deck.get_new_deck()
        deck.shuffle_deck()

        assert deck.shuffled is True
        assert deck.remaining == 40

    def test_shuffle_deck_raises(self):
        deck = Deck()
        with pytest.raises(ValueError, match="Deck ID is not set. Please get a new deck first."):
            deck.shuffle_deck()

    def test_draw_card(self, mock_api, mock_new_deck_response, mock_draw_card_response, monkeypatch):
        monkeypatch.setattr("core.api_client.DeckAPIClient.get_new_deck", lambda self, deck_count=1: mock_new_deck_response)
        monkeypatch.setattr("core.api_client.DeckAPIClient.draw_card", lambda self, deck_id, count=1: mock_draw_card_response)

        deck = Deck()
        deck.get_new_deck()
        cards = deck.draw_card()

        assert len(cards) == 1
        assert cards[0].suit == "SPADES"
        assert cards[0].rank == "ACE"
        assert cards[0].image == "https://deckofcardsapi.com/static/img/AS.png"
        assert deck.remaining == 51

    def test_draw_card_raises(self):
        deck = Deck()
        with pytest.raises(ValueError, match="Deck ID is not set. Please get a new deck first."):
            deck.draw_card()


class TestHand:

    def test_hand_initialization(self):
        deck = Deck()
        hand = Hand(deck=deck)
        assert isinstance(hand, Hand)

        assert hand.cards == []
        assert hand.deck == deck

    def test_calculate_score(self):
        deck = Deck()
        cards = [
            Card(suit="HEARTS", rank="10", image="https://deckofcardsapi.com/static/img/0H.png"),
            Card(suit="SPADES", rank="ACE", image="https://deckofcardsapi.com/static/img/AS.png")
        ]
        hand = Hand(deck=deck, cards=cards)
        result = hand.calculate_score()

        assert result == 21

    def test_calculate_score_no_face_cards(self):
        deck = Deck()
        cards = [
            Card(suit="HEARTS", rank="2", image="https://deckofcardsapi.com/static/img/2H.png"),
            Card(suit="SPADES", rank="3", image="https://deckofcardsapi.com/static/img/3S.png")
        ]
        hand = Hand(deck=deck, cards=cards)
        result = hand.calculate_score()

        assert result == 5

    def test_calculate_score_multiple_aces(self):
        deck = Deck()
        cards = [
            Card(suit="HEARTS", rank="ACE", image="https://deckofcardsapi.com/static/img/AH.png"),
            Card(suit="SPADES", rank="ACE", image="https://deckofcardsapi.com/static/img/AS.png"),
            Card(suit="DIAMONDS", rank="9", image="https://deckofcardsapi.com/static/img/9D.png")
        ]
        hand = Hand(deck=deck, cards=cards)
        result = hand.calculate_score()

        assert result == 21

    def test_draw_card(self, mock_api, mock_new_deck_response, mock_draw_card_response, monkeypatch):
        monkeypatch.setattr("core.api_client.DeckAPIClient.get_new_deck", lambda self, deck_count=1: mock_new_deck_response)
        monkeypatch.setattr("core.api_client.DeckAPIClient.draw_card", lambda self, deck_id, count=1: mock_draw_card_response)

        deck = Deck()
        deck.get_new_deck()
        hand = Hand(deck=deck)
        cards = hand.deck.draw_card()

        assert len(cards) == 1
        assert hand.deck.remaining == 51


class TestBlackJackRule:

    def test_blackjack_rule_initialization(self, mock_deck):
        rule = BlackJackRule(deck=mock_deck)

        assert isinstance(rule, BlackJackRule)
        assert isinstance(rule.deck, Deck)
        assert isinstance(rule.player_hand, Hand)
        assert isinstance(rule.dealer_hand, Hand)

    def test_determine_winner(self, mock_deck):
        rule = BlackJackRule(deck=mock_deck)

        rule.player_hand.cards = [
            Card(suit="HEARTS", rank="10", image="https://deckofcardsapi.com/static/img/0H.png"),
            Card(suit="SPADES", rank="ACE", image="https://deckofcardsapi.com/static/img/AS.png")
        ]
        rule.dealer_hand.cards = [
            Card(suit="DIAMONDS", rank="9", image="https://deckofcardsapi.com/static/img/9D.png"),
            Card(suit="CLUBS", rank="7", image="https://deckofcardsapi.com/static/img/7C.png")
        ]

        result = rule.determine_winner()
        assert result == "Player wins!"

    def test_determine_winner_tie(self, mock_deck):
        rule = BlackJackRule(deck=mock_deck)

        rule.player_hand.cards = [
            Card(suit="HEARTS", rank="10", image="https://deckofcardsapi.com/static/img/0H.png"),
            Card(suit="SPADES", rank="ACE", image="https://deckofcardsapi.com/static/img/AS.png")
        ]
        rule.dealer_hand.cards = [
            Card(suit="DIAMONDS", rank="10", image="https://deckofcardsapi.com/static/img/0D.png"),
            Card(suit="CLUBS", rank="ACE", image="https://deckofcardsapi.com/static/img/AC.png")
        ]

        result = rule.determine_winner()
        assert result == "It's a tie!"

    def test_determine_winner_dealer_wins(self, mock_deck):
        rule = BlackJackRule(deck=mock_deck)

        rule.player_hand.cards = [
            Card(suit="HEARTS", rank="10", image="https://deckofcardsapi.com/static/img/0H.png"),
            Card(suit="SPADES", rank="9", image="https://deckofcardsapi.com/static/img/9S.png")
        ]
        rule.dealer_hand.cards = [
            Card(suit="DIAMONDS", rank="10", image="https://deckofcardsapi.com/static/img/0D.png"),
            Card(suit="CLUBS", rank="ACE", image="https://deckofcardsapi.com/static/img/AC.png")
        ]

        result = rule.determine_winner()
        assert result == "Dealer wins!"

    def test_determine_winner_player_busts(self, mock_deck):
        rule = BlackJackRule(deck=mock_deck)

        rule.player_hand.cards = [
            Card(suit="HEARTS", rank="10", image="https://deckofcardsapi.com/static/img/0H.png"),
            Card(suit="SPADES", rank="9", image="https://deckofcardsapi.com/static/img/9S.png"),
            Card(suit="DIAMONDS", rank="5", image="https://deckofcardsapi.com/static/img/5D.png")
        ]
        rule.dealer_hand.cards = [
            Card(suit="DIAMONDS", rank="10", image="https://deckofcardsapi.com/static/img/0D.png"),
            Card(suit="CLUBS", rank="ACE", image="https://deckofcardsapi.com/static/img/AC.png")
        ]

        result = rule.determine_winner()
        assert result == "Dealer wins!"

    def test_determine_winner_dealer_busts(self, mock_deck):
        rule = BlackJackRule(deck=mock_deck)

        rule.player_hand.cards = [
            Card(suit="HEARTS", rank="10", image="https://deckofcardsapi.com/static/img/0H.png"),
            Card(suit="SPADES", rank="9", image="https://deckofcardsapi.com/static/img/9S.png")
        ]
        rule.dealer_hand.cards = [
            Card(suit="DIAMONDS", rank="10", image="https://deckofcardsapi.com/static/img/0D.png"),
            Card(suit="CLUBS", rank="9", image="https://deckofcardsapi.com/static/img/9C.png"),
            Card(suit="HEARTS", rank="5", image="https://deckofcardsapi.com/static/img/5H.png")
        ]

        result = rule.determine_winner()
        assert result == "Player wins!"

    def test_dealer_attempts_win(self, mock_deck):
        rule = BlackJackRule(deck=mock_deck)
        # NOTE: I'm letting the get_new_deck method here make an actual API call to set the deck_id, 
        # since the dealer_attempts_win method relies on the draw_card method which also makes an API 
        # call. Mocking both methods would be more complex.
        rule.deck.get_new_deck()

        rule.dealer_hand.cards = [
            Card(suit="DIAMONDS", rank="10", image="https://deckofcardsapi.com/static/img/0D.png"),
            Card(suit="CLUBS", rank="6", image="https://deckofcardsapi.com/static/img/6C.png")
        ]
        assert rule.dealer_hand.calculate_score() == 16

        rule.dealer_attempts_win()
        assert rule.dealer_hand.calculate_score() >= 17