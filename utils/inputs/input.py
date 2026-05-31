from utils import PlayerAction

def get_player_action() -> str:
    while True:
        choice = input("> ").strip().upper()
        match choice:
            case "H":
                return PlayerAction.HIT.value
            case "S":
                return PlayerAction.STAND.value
            case "D":
                return PlayerAction.DOUBLE.value
            case _:
                print("Unknown action. Please enter H, S, or D.")