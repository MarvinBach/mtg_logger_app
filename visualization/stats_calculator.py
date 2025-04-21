from typing import Dict, List, Optional
import pandas as pd
from .data_provider import DataProvider
from datetime import datetime

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

    def calculate_player_matchups(self, player_name: str, start_date=None, end_date=None, edition_filter="All"):
        """Calculate win rates against other players with filters"""
        games = self.data_provider.get_games()
        players = self.data_provider.get_players()

        if not games or not players:
            return pd.DataFrame()

        # Get player ID
        player = next((p for p in players if p["name"] == player_name), None)
        if not player:
            return pd.DataFrame()

        # Filter games by date range and edition
        filtered_games = []
        for game in games:
            # Check if game involves the player
            if game["winner_id"] != player["id"] and game["loser_id"] != player["id"]:
                continue

            # Apply date filter if specified
            if start_date or end_date:
                game_date = datetime.fromisoformat(game["played_at"]).date()
                if start_date and game_date < start_date:
                    continue
                if end_date and game_date > end_date:
                    continue

            # Apply edition filter if specified
            if edition_filter != "All" and game.get("edition") != edition_filter:
                continue

            filtered_games.append(game)

        # Calculate matchup statistics
        matchups = {}
        for game in filtered_games:
            opponent_id = game["loser_id"] if game["winner_id"] == player["id"] else game["winner_id"]
            opponent = next(p for p in players if p["id"] == opponent_id)

            if opponent["name"] not in matchups:
                matchups[opponent["name"]] = {"wins": 0, "total": 0}

            matchups[opponent["name"]]["total"] += 1
            if game["winner_id"] == player["id"]:
                matchups[opponent["name"]]["wins"] += 1

        # Convert to DataFrame
        stats = []
        for opponent, data in matchups.items():
            stats.append({
                "Opponent": opponent,
                "Win Rate": data["wins"] / data["total"],
                "Total Games": data["total"]
            })

        return pd.DataFrame(stats).sort_values("Win Rate", ascending=False)

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

    def calculate_player_color_stats(self, player_name: str, start_date=None, end_date=None, edition_filter="All"):
        """Calculate win rates by color combination with filters"""
        games = self.data_provider.get_games()
        players = self.data_provider.get_players()

        if not games or not players:
            return pd.DataFrame()

        # Get player ID
        player = next((p for p in players if p["name"] == player_name), None)
        if not player:
            return pd.DataFrame()

        # Filter games and collect color statistics
        color_stats = {}
        for game in games:
            # Check if game involves the player
            is_winner = game["winner_id"] == player["id"]
            is_loser = game["loser_id"] == player["id"]
            if not (is_winner or is_loser):
                continue

            # Apply date filter if specified
            if start_date or end_date:
                game_date = datetime.fromisoformat(game["played_at"]).date()
                if start_date and game_date < start_date:
                    continue
                if end_date and game_date > end_date:
                    continue

            # Apply edition filter if specified
            if edition_filter != "All" and game.get("edition") != edition_filter:
                continue

            # Get player's colors for this game
            colors = game["winner_colors"] if is_winner else game["loser_colors"]
            color_key = ", ".join(sorted(colors)) if colors else "Colorless"

            if color_key not in color_stats:
                color_stats[color_key] = {"wins": 0, "total": 0}

            color_stats[color_key]["total"] += 1
            if is_winner:
                color_stats[color_key]["wins"] += 1

        # Convert to DataFrame
        stats = []
        for colors, data in color_stats.items():
            if data["total"] > 0:
                stats.append({
                    "Colors": colors,
                    "Win Rate": data["wins"] / data["total"],
                    "Total Games": data["total"]
                })

        return pd.DataFrame(stats).sort_values("Win Rate", ascending=False)
