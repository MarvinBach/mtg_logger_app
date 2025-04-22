import streamlit as st
from .stats_calculator import StatsCalculator

class DataVisualizer:
    """Visualizes statistics using Streamlit"""
    def __init__(self, stats_calculator: StatsCalculator):
        self.stats_calculator = stats_calculator

    def plot_player_win_rates(self) -> None:
        """Display win rates for all players"""
        win_rates = self.stats_calculator.calculate_player_win_rates()
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
            st.write("No games found for the selected filters.")
            return

        # Format win rates as percentages
        df["Win Rate"] = df["Win Rate"].apply(lambda x: f"{x*100:.1f}%")

        # Display the dataframe
        st.dataframe(
            df,
            column_config={
                "Opponent": st.column_config.TextColumn("Opponent"),
                "Win Rate": st.column_config.TextColumn("Win Rate"),
                "Total Games": st.column_config.NumberColumn("Total Games", format="%d")
            },
            hide_index=True
        )

    def plot_player_win_rates_by_color(self, player_name: str, start_date=None, end_date=None, edition_filter="All", format_filter="All") -> None:
        """Display win rates by color for a selected player"""
        st.subheader(f"Win Rates by Color - {player_name}")

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
