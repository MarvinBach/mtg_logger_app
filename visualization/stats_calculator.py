from typing import Dict, List, Optional
import pandas as pd
from .data_provider import DataProvider
from datetime import datetime

class StatsCalculator:
    """Calculates statistics from game data"""
    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
        self.players = self.data_provider.get_players()

    def calculate_player_win_rates(self) -> pd.DataFrame:
        """Calculate win rates for all players using all games in database"""
        games = self.data_provider.get_games()  # Get ALL games
        win_counts: Dict[int, int] = {}
        loss_counts: Dict[int, int] = {}

        for game in games:
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

    def calculate_player_matchups(self, player_name: str, start_date=None, end_date=None, edition_filter="All", format_filter="All"):
        """Calculate win rates against other players"""
        # Get all games for the player
        all_games = self.data_provider.get_games()  # Get ALL games instead of just recent ones
        player_games = [
            game for game in all_games
            if player_name in [
                self.data_provider.get_player_by_id(game["winner_id"]),
                self.data_provider.get_player_by_id(game["loser_id"])
            ]
        ]

        if not player_games:
            return pd.DataFrame(columns=["Opponent", "Win Rate", "Total Games"])

        # Apply date filter if specified
        if start_date:
            player_games = [g for g in player_games if datetime.fromisoformat(g["played_at"]).date() >= start_date]
        if end_date:
            player_games = [g for g in player_games if datetime.fromisoformat(g["played_at"]).date() <= end_date]

        # Apply edition filter if specified
        if edition_filter != "All":
            player_games = [g for g in player_games if g["edition"] == edition_filter]

        # Apply format filter if specified
        if format_filter != "All":
            player_games = [g for g in player_games if g["format"] == format_filter]

        # Calculate matchup statistics
        matchups = {}
        for game in player_games:
            winner = self.data_provider.get_player_by_id(game["winner_id"])
            loser = self.data_provider.get_player_by_id(game["loser_id"])
            opponent = loser if winner == player_name else winner

            if opponent not in matchups:
                matchups[opponent] = {"wins": 0, "total": 0}
            matchups[opponent]["total"] += 1
            if winner == player_name:
                matchups[opponent]["wins"] += 1

        # Convert to DataFrame
        if not matchups:
            return pd.DataFrame(columns=["Opponent", "Win Rate", "Total Games"])

        df = pd.DataFrame([
            {
                "Opponent": opp,
                "Win Rate": stats["wins"] / stats["total"],
                "Total Games": stats["total"]
            }
            for opp, stats in matchups.items()
        ])

        return df.sort_values("Win Rate", ascending=False) if not df.empty else df

    def calculate_player_color_stats(self, player_name: str, start_date=None, end_date=None, edition_filter="All", format_filter="All"):
        """Calculate win rates by color combination with filters"""
        games = self.data_provider.get_games()  # Get ALL games
        players = self.data_provider.get_players()

        if not games or not players:
            return pd.DataFrame(columns=["Colors", "Win Rate (%)", "Total Games"])

        # Get player ID
        player = next((p for p in players if p["name"] == player_name), None)
        if not player:
            return pd.DataFrame(columns=["Colors", "Win Rate (%)", "Total Games"])

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

            # Apply format filter if specified
            if format_filter != "All" and game.get("format") != format_filter:
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
            total = data["total"]
            wins = data["wins"]
            win_rate = round((wins / total) * 100, 2) if total > 0 else 0
            stats.append({
                "Colors": colors,
                "Wins": wins,
                "Losses": total - wins,
                "Total Games": total,
                "Win Rate (%)": win_rate,
            })

        df = pd.DataFrame(stats)
        return df.sort_values("Win Rate (%)", ascending=False) if not df.empty else df
