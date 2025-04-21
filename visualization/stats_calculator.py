from typing import Dict, List, Optional
import pandas as pd
from .data_provider import DataProvider

class StatsCalculator:
    """Calculates statistics from game data"""
    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
        self.games = self.data_provider.get_recent_games()
        self.players = self.data_provider.get_players()

    def calculate_player_win_rates(self) -> pd.DataFrame:
        """Calculate win rates for all players"""
        win_counts: Dict[int, int] = {}
        loss_counts: Dict[int, int] = {}

        for game in self.games:
            winner_id = game["winner_id"]
            loser_id = game["loser_id"]
            win_counts[winner_id] = win_counts.get(winner_id, 0) + 1
            loss_counts[loser_id] = loss_counts.get(loser_id, 0) + 1

        stats = []
        for player_id in set(win_counts) | set(loss_counts):
            name = self.data_provider.get_player_by_id(player_id)
            wins = win_counts.get(player_id, 0)
            losses = loss_counts.get(player_id, 0)
            total = wins + losses
            win_rate = round((wins / total) * 100, 2) if total > 0 else 0
            stats.append({
                "Player": name,
                "Wins": wins,
                "Losses": losses,
                "Total Games": total,
                "Win Rate (%)": win_rate,
            })

        return pd.DataFrame(stats).sort_values(by="Win Rate (%)", ascending=False)

    def calculate_color_win_rates(
        self,
        player_name: str,
        game_format: str = "All",
        edition: str = "All"
    ) -> Optional[pd.DataFrame]:
        """Calculate win rates by color for a specific player"""
        player_map = {p["name"]: p["id"] for p in self.players}
        player_id = player_map.get(player_name)

        if not player_id:
            return None

        filtered_games = [
            g for g in self.games
            if (g["winner_id"] == player_id or g["loser_id"] == player_id)
            and isinstance(g.get("winner_colors"), list)
            and isinstance(g.get("loser_colors"), list)
            and (game_format == "All" or g.get("format") == game_format)
            and (edition == "All" or g.get("edition") == edition)
        ]

        win_counts: Dict[str, int] = {}
        loss_counts: Dict[str, int] = {}

        for game in filtered_games:
            if game["winner_id"] == player_id:
                for color in game["winner_colors"]:
                    win_counts[color] = win_counts.get(color, 0) + 1
            else:
                for color in game["loser_colors"]:
                    loss_counts[color] = loss_counts.get(color, 0) + 1

        all_colors = sorted(set(win_counts) | set(loss_counts))
        if not all_colors:
            return None

        stats = []
        for color in all_colors:
            wins = win_counts.get(color, 0)
            losses = loss_counts.get(color, 0)
            total = wins + losses
            win_rate = round((wins / total) * 100, 2) if total > 0 else 0
            stats.append({
                "Color": color,
                "Wins": wins,
                "Losses": losses,
                "Total Games": total,
                "Win Rate (%)": win_rate,
            })

        return pd.DataFrame(stats)
