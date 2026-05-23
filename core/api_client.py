from typing import Dict, Any
import requests

class DeckAPIClient:
    BASE_URL = "https://deckofcardsapi.com/api"

    def get_new_deck(self, deck_count: int = 1) -> Dict[str, Any]:
        response = requests.get(f"{self.BASE_URL}/deck/new/shuffle/?deck_count={deck_count}")
        return response.json()

    def shuffle_deck(self, deck_id: str) -> Dict[str, Any]:
        # Code to shuffle the deck using the API
        response = requests.get(f"{self.BASE_URL}/deck/{deck_id}/shuffle/?remaining=true")
        return response.json()

    def draw_card(self, deck_id: str, count: int = 1) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/deck/{deck_id}/draw/?count={count}"
        response = requests.get(url)
        return response.json()