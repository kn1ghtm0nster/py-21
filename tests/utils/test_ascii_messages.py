import pytest

from utils import print_welcome, print_message

def test_print_welcome(capsys):
    print_welcome()
    result = capsys.readouterr()
    assert "WELCOME TO BLACKJACK" in result.out

def test_print_message(capsys):
    print_message("Test message", style="bold red")
    result = capsys.readouterr()
    assert "Test message" in result.out