import streamlit as st
from .stats_calculator import StatsCalculator

class DataVisualizer:
    """Visualizes statistics using Streamlit"""
    def __init__(self, stats_calculator: StatsCalculator):
        self.stats_calculator = stats_calculator

    def plot_player_win_rates(self, start_date=None, end_date=None, edition_filter="All", format_filter="All") -> None:
        """Display win rates for all players"""
        win_rates = self.stats_calculator.calculate_player_win_rates(start_date=start_date, end_date=end_date, edition_filter=edition_filter, format_filter=format_filter)
        if win_rates.empty:
            st.info("No games recorded yet.")
            return

        st.subheader("Overall Win Rates")
        st.dataframe(
            win_rates.style.format({
                "Win Rate (%)": "{:.1f}%",
                "Total Games": "{:}"
            }),
            use_container_width=True
        )

    def plot_player_matchups(self, player_name: str, start_date=None, end_date=None, edition_filter="All", format_filter="All"):
        """Display player matchup statistics"""
        st.subheader(f"Matchup Statistics - {player_name}")

        df = self.stats_calculator.calculate_player_matchups(
            player_name, start_date, end_date, edition_filter, format_filter
        )

        if df.empty:
            st.info(f"No games found for {player_name} with the current filters.")
            return

        # Display the dataframe with consistent formatting
        st.dataframe(
            df.style.format({
                "Win Rate (%)": "{:.1f}%",
                "Total Games": "{:}"
            }),
            use_container_width=True
        )

    def plot_player_win_rates_by_color(self, player_name: str, start_date=None, end_date=None, edition_filter="All", format_filter="All") -> None:
        """Display win rates by color combination for a selected player"""
        st.subheader(f"Win Rates by Color Combination - {player_name}")
        st.caption("Shows statistics for each unique combination of colors played")

        color_stats = self.stats_calculator.calculate_player_color_stats(
            player_name,
            start_date=start_date,
            end_date=end_date,
            edition_filter=edition_filter,
            format_filter=format_filter
        )

        if color_stats.empty:
            st.info(f"No games found for {player_name} with the current filters.")
            return

        st.dataframe(
            color_stats.style.format({
                "Win Rate (%)": "{:.1f}%",
                "Total Games": "{:}"
            }),
            use_container_width=True
        )

    def plot_player_individual_color_stats(self, player_name: str, start_date=None, end_date=None, edition_filter="All", format_filter="All") -> None:
        """Display win rates by individual colors for a selected player"""
        st.subheader(f"Win Rates by Individual Color - {player_name}")
        st.caption("Each color is counted separately when playing multi-color decks")

        color_stats = self.stats_calculator.calculate_player_individual_color_stats(
            player_name,
            start_date=start_date,
            end_date=end_date,
            edition_filter=edition_filter,
            format_filter=format_filter
        )

        if color_stats.empty:
            st.info(f"No games found for {player_name} with the current filters.")
            return

        st.dataframe(
            color_stats.style.format({
                "Win Rate (%)": "{:.1f}%",
                "Total Games": "{:}"
            }),
            use_container_width=True
        )
