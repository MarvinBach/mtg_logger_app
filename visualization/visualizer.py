import streamlit as st
from .stats_calculator import StatsCalculator
import plotly.express as px

class DataVisualizer:
    """Visualizes statistics using Streamlit"""
    def __init__(self, stats_calculator: StatsCalculator):
        self.stats_calculator = stats_calculator

    def plot_player_win_rates(self) -> None:
        """Plot overall win rates for all players"""
        win_rates = self.stats_calculator.calculate_win_rates()
        if win_rates.empty:
            st.info("No games recorded yet.")
            return

        st.subheader("Overall Win Rates")
        fig = px.bar(
            win_rates,
            x="Player",
            y="Win Rate",
            text=win_rates["Win Rate"].apply(lambda x: f"{x:.1%}"),
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    def plot_player_matchups(self, player_name: str, start_date=None, end_date=None, edition_filter="All") -> None:
        """Plot win rates against other players for a specific player with filters"""
        st.subheader(f"Win Rates Against Other Players - {player_name}")

        # Get matchup data with filters
        matchups = self.stats_calculator.calculate_player_matchups(
            player_name,
            start_date=start_date,
            end_date=end_date,
            edition_filter=edition_filter
        )

        if matchups.empty:
            st.info(f"No games found for {player_name} with the current filters.")
            return

        # Create bar chart
        fig = px.bar(
            matchups,
            x="Opponent",
            y="Win Rate",
            text=matchups["Win Rate"].apply(lambda x: f"{x:.1%}"),
            hover_data=["Total Games"]
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

        # Show detailed statistics
        with st.expander("Detailed Statistics"):
            st.dataframe(
                matchups.style.format({
                    "Win Rate": "{:.1%}",
                    "Total Games": "{:}"
                })
            )

    def plot_player_win_rates_by_color(self, player_name: str, start_date=None, end_date=None, edition_filter="All") -> None:
        """Plot win rates by color for a specific player with filters"""
        st.subheader(f"Win Rates by Color - {player_name}")

        # Get color stats with filters
        color_stats = self.stats_calculator.calculate_player_color_stats(
            player_name,
            start_date=start_date,
            end_date=end_date,
            edition_filter=edition_filter
        )

        if color_stats.empty:
            st.info(f"No games found for {player_name} with the current filters.")
            return

        # Create bar chart
        fig = px.bar(
            color_stats,
            x="Colors",
            y="Win Rate",
            text=color_stats["Win Rate"].apply(lambda x: f"{x:.1%}"),
            hover_data=["Total Games"]
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

        # Show detailed statistics
        with st.expander("Detailed Statistics"):
            st.dataframe(
                color_stats.style.format({
                    "Win Rate": "{:.1%}",
                    "Total Games": "{:}"
                })
            )
