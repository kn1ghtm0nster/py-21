# Blackjack in Python!

For the days when you're bored and want something to do in your terminal to pretend you're working.

This project was written exclusively in Python with as few dependencies as possible. All you need to do is follow the install guide and you're set!

## Requirements

- Python 3.10+
- `pip` (Python package manager)

## Install Guide

1. Clone the repository:

```bash
git clone https://github.com/yourusername/py-21.git
cd py-21
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Play

Start the game:

```bash
python main.py
```

**Game Rules:**

- Get a hand value closer to 21 than the dealer without going over
- Hit: Take another card
- Stand: Keep your current hand
- Double: Double your bet and take one final card (for MVP, no actual betting)
- Bust: Go over 21 and lose instantly

## Project Structure

```
py-21/
├── core/              # Game models (Card, Deck, Hand, Rules)
├── games/             # Game logic (BlackjackGame orchestrator)
├── display/           # Terminal rendering (ASCII cards)
├── utils/             # Helper utilities (input handling, enums, messages)
├── tests/             # Unit tests for all modules
├── main.py            # Entry point
└── requirements.txt   # Python dependencies
```

## Running Tests

Run all tests:

```bash
python -m pytest
```

Run specific test file:

```bash
python -m pytest tests/core/test_models.py
```

Run with verbose output:

```bash
python -m pytest -v
```

## Future Enhancements

This project was meant to be more than just blackjack but for the time being, I have limited this project to one game. Future additions include:

- Betting system with player balance
- Additional card games (Poker, War, etc.)
- Multiplayer support
- Scoring/leaderboard system
- Better AI for dealer decisions

## Contributing

Feel free to fork the repository and add more features or games to this project! All I ask is that you:

1. Open an issue describing your enhancement
2. Follow the existing code structure
3. Write tests for new functionality
4. Submit a PR with a clear description

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
