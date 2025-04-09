import streamlit as st
import pandas as pd
from db import get_player_by_id, get_players, get_recent_games


class WinRatePlotter:
    def __init__(self, games=None):
        self.games = games or get_recent_games()
        self.players = get_players()

    def get_player_win_rates(self):
        """Calculate win rates for all players."""
        win_counts = {}
        loss_counts = {}

        for g in self.games:
            winner_id = g["winner_id"]
            loser_id = g["loser_id"]
            win_counts[winner_id] = win_counts.get(winner_id, 0) + 1
            loss_counts[loser_id] = loss_counts.get(loser_id, 0) + 1

        player_ids = set(win_counts) | set(loss_counts)
        stats = []

        for player_id in player_ids:
            name = get_player_by_id(player_id)
            wins = win_counts.get(player_id, 0)
            losses = loss_counts.get(player_id, 0)
            total = wins + losses
            win_rate = round((wins / total) * 100, 2) if total > 0 else 0
            stats.append(
                {
                    "Player": name,
                    "Wins": wins,
                    "Losses": losses,
                    "Total Games": total,
                    "Win Rate (%)": win_rate,
                }
            )

        df = pd.DataFrame(stats).sort_values(by="Win Rate (%)", ascending=False)
        return df

    def plot_player_win_rates(self):
        """Plot win rates for all players."""
        df = self.get_player_win_rates()
        st.dataframe(df)

    def plot_player_win_rates_by_color(
        self,
        selected_player_name: str,
        selected_format: str = "All",
        selected_edition: str = "All",
    ):
        """Plot win rates by color for a selected player, with optional format and edition filtering."""
        player_map = {p["name"]: p["id"] for p in self.players}
        player_id = player_map.get(selected_player_name)

        if not player_id:
            st.error("Player not found.")
            return

        filtered_games = [
            g
            for g in self.games
            if (g["winner_id"] == player_id or g["loser_id"] == player_id)
            and isinstance(g.get("winner_colors"), list)
            and isinstance(g.get("loser_colors"), list)
            and (selected_format == "All" or g.get("format") == selected_format)
            and (selected_edition == "All" or g.get("edition") == selected_edition)
        ]

        win_counts = {}
        loss_counts = {}

        for g in filtered_games:
            if g["winner_id"] == player_id:
                for color in g["winner_colors"]:
                    win_counts[color] = win_counts.get(color, 0) + 1
            elif g["loser_id"] == player_id:
                for color in g["loser_colors"]:
                    loss_counts[color] = loss_counts.get(color, 0) + 1

        all_colors = sorted(set(win_counts.keys()) | set(loss_counts.keys()))
        stats = []

        for color in all_colors:
            wins = win_counts.get(color, 0)
            losses = loss_counts.get(color, 0)
            total = wins + losses
            win_rate = round((wins / total) * 100, 2) if total > 0 else 0
            stats.append(
                {
                    "Color": color,
                    "Wins": wins,
                    "Losses": losses,
                    "Total Games": total,
                    "Win Rate (%)": win_rate,
                }
            )

        if stats:
            df = pd.DataFrame(stats)
            st.subheader(f"Win Rates for {selected_player_name} by Color")
            st.dataframe(df)
        else:
            st.write("No head-to-head data available.")
