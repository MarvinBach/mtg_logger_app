from models import Player


def add_player(name: str) -> str:
    """Adds a new player to the database."""
    name = name.strip()
    if not name:
        raise ValueError("Player name cannot be empty.")

    Player.add(name=name)
    return f"Player {name} added successfully!"
