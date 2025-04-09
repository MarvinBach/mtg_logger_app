from models import Player


def add_player(name: str) -> str:
    """Adds a new player to the database"""
    name = name.strip()
    if not name:
        raise ValueError("Player name cannot be empty.")

    player = Player(name=name)
    response = player.add()

    if not response or not getattr(response, "data", None):
        raise Exception("Failed to add player.")

    return f"Player {name} added successfully!"
