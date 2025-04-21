from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from .enums import GameFormat, Color, Edition

@dataclass
class Player:
    """Player model with validation"""
    name: str
    id: Optional[int] = None

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Player name cannot be empty")
        if len(self.name) > 50:
            raise ValueError("Player name too long (max 50 characters)")

@dataclass
class Game:
    """Game model with validation"""
    winner_id: int
    loser_id: int
    game_format: GameFormat
    winner_colors: List[Color]
    loser_colors: List[Color]
    edition: Optional[Edition] = None
    played_at: Optional[datetime] = None
    id: Optional[int] = None

    def validate(self) -> None:
        if self.winner_id == self.loser_id:
            raise ValueError("Winner and loser cannot be the same player")
        if not self.winner_colors and not self.loser_colors:
            raise ValueError("At least one player must have colors")

    def to_dict(self) -> dict:
        """Convert game to dictionary for database storage"""
        return {
            "winner_id": self.winner_id,
            "loser_id": self.loser_id,
            "format": self.game_format.value,
            "winner_colors": [color.value for color in self.winner_colors],
            "loser_colors": [color.value for color in self.loser_colors],
            "edition": self.edition.value if self.edition else None,
            "played_at": self.played_at.isoformat() if self.played_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Game':
        """Create game instance from dictionary"""
        return cls(
            winner_id=data["winner_id"],
            loser_id=data["loser_id"],
            game_format=GameFormat(data["format"]),
            winner_colors=[Color(c) for c in data["winner_colors"]],
            loser_colors=[Color(c) for c in data["loser_colors"]],
            edition=Edition(data["edition"]) if data.get("edition") else None,
            played_at=datetime.fromisoformat(data["played_at"]) if data.get("played_at") else None,
            id=data.get("id")
        )
