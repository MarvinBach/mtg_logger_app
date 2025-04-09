from models import Player


def add_player(name: str) -> str:
    """Adds a new player to the database"""
    name = name.strip()
    if not name:
        raise ValueError("Player name cannot be empty.")

    player = Player(name=name)
    response = player.add()

    if response.status_code != 201:
        raise Exception(f"Supabase error: {response}")

    return f"Player {name} added successfully!"
