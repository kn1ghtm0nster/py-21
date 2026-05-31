from rich.console import Console
from rich.panel import Panel
from rich.text import Text


console = Console()

def print_welcome():
    title = Text("WELCOME TO BLACKJACK", style="bold magenta")
    panel = Panel(title, expand=False)
    console.print(panel)

def print_message(msg: str, style: str = ""):
    console.print(msg, style=style)