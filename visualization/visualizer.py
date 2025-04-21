import streamlit as st
from .stats_calculator import StatsCalculator

class DataVisualizer:
    """Visualizes statistics using Streamlit"""
    def __init__(self, stats_calculator: StatsCalculator):
        self.stats_calculator = stats_calculator

    def plot_player_win_rates(self) -> None:
        """Display win rates for all players"""
        df = self.stats_calculator.calculate_player_win_rates()
        st.dataframe(df, use_container_width=True)

    def plot_player_matchups(self, player_name: str) -> None:
        """Display win rates against other players"""
        df = self.stats_calculator.calculate_player_matchups(player_name)
        if df is not None:
            st.subheader(f"Win Rates against Other Players")
            st.dataframe(df, use_container_width=True)
        else:
            st.write("No matchup data available.")

    def plot_player_win_rates_by_color(
        self,
        player_name: str,
        game_format: str = "All",
        edition: str = "All"
    ) -> None:
        """Display win rates by color for a selected player"""
        df = self.stats_calculator.calculate_color_win_rates(
            player_name, game_format, edition
        )
        if df is not None:
            st.dataframe(df, use_container_width=True)
        else:
            st.write("No win rates by color data available.")
