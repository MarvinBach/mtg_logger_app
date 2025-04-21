import streamlit as st
from datetime import datetime, timedelta
from data.repositories import GameRepository, PlayerRepository
from core.enums import Edition
from .edit_game_form import edit_game_modal
from typing import List, Dict, Any

@st.cache_data(ttl=60)  # Cache player data for 1 minute
def get_cached_players() -> List[Dict[str, Any]]:
    """Get cached list of players"""
    try:
        return PlayerRepository.get_all()
    except Exception as e:
        st.error(f"Failed to fetch players: {str(e)}")
        return []

def get_game_date(game):
    """Extract date from game's played_at field"""
    try:
        if not game.get("played_at"):
            return None

        played_at = game["played_at"]
        return datetime.fromisoformat(played_at).date() if isinstance(played_at, str) else played_at.date()
    except (ValueError, AttributeError) as e:
        st.error(f"Error parsing date for game {game}: {str(e)}")
        return None

def render_game_history() -> None:
    """Render game history"""
    st.header("Game History")

    # Get cached player data
    players = get_cached_players()
    player_map = {p["name"]: p["id"] for p in players}

    # Filter and display options
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 0.7])

    with col1:
        default_start = datetime.now().date() - timedelta(days=30)  # Last 30 days by default
        start_date = st.date_input(
            "From Date",
            value=default_start,
            key="history_start_date",
            help="Start date (inclusive)"
        )

    with col2:
        end_date = st.date_input(
            "To Date",
            value=datetime.now().date(),  # Today by default
            key="history_end_date",
            help="End date (inclusive)"
        )

    with col3:
        edition_filter = st.selectbox(
            "Edition",
            ["All"] + Edition.list()[1:],
            key="history_edition_filter"
        )

    with col4:
        player_filter = st.selectbox(
            "Player",
            ["All"] + list(player_map.keys()),
            key="history_player_filter"
        )

    # Then let user choose how many games to display
    with col5:
        display_limit = st.number_input(
            "Show games",
            min_value=1,
            max_value=100,  # Reasonable maximum
            value=5,  # Default to 5 games
            step=5,
            key="history_limit"
        )

    # Get filtered games directly from database
    player_id = player_map[player_filter] if player_filter != "All" else None
    filtered_games = GameRepository.get_filtered_games(
        start_date=start_date,
        end_date=end_date,
        edition_filter=edition_filter,
        player_id=player_id,
        limit=display_limit
    )

    if not filtered_games:
        st.info("No games found matching the selected filters.")
        return

    # Display games
    st.caption(f"Showing {len(filtered_games)} games")

    for game in filtered_games:
        # Create columns for game info and edit button
        col1, col2 = st.columns([0.85, 0.15])

        with col1:
            winner_name = PlayerRepository.get_by_id(game["winner_id"])
            loser_name = PlayerRepository.get_by_id(game["loser_id"])

            # Handle date display
            played_at_str = ""
            if game.get("played_at"):
                try:
                    if isinstance(game["played_at"], str):
                        played_at = datetime.fromisoformat(game["played_at"])
                    else:
                        played_at = game["played_at"]
                    played_at_str = f" on {played_at.strftime('%Y-%m-%d %H:%M')}"
                except (ValueError, AttributeError) as e:
                    st.error(f"Error parsing date: {e}")

            # Display game info with colors
            winner_colors = ", ".join(game.get("winner_colors", []))
            loser_colors = ", ".join(game.get("loser_colors", []))

            game_info = (
                f"{winner_name} ({winner_colors}) defeated "
                f"{loser_name} ({loser_colors}) in {game['format']} format{played_at_str}"
            )

            st.write(game_info)

        with col2:
            edit_game_modal(game)
