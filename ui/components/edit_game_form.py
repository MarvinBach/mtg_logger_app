import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime
from core.enums import GameFormat, Color, Edition
from core.models import Game
from data.repositories import GameRepository, PlayerRepository

def render_edit_game_form(game_data: Dict[str, Any]) -> None:
    """Render form for editing an existing game"""

    # Get players for dropdowns
    players = PlayerRepository.get_all()
    player_map = {p["name"]: p["id"] for p in players}
    player_names = list(player_map.keys())

    # Get current values
    current_winner = next(name for name, id in player_map.items()
                        if id == game_data["winner_id"])
    current_loser = next(name for name, id in player_map.items()
                        if id == game_data["loser_id"])

    # Form inputs
    winner = st.selectbox(
        "Winner",
        player_names,
        index=player_names.index(current_winner),
        key=f"edit_winner_{game_data['id']}"
    )

    loser = st.selectbox(
        "Loser",
        player_names,
        index=player_names.index(current_loser),
        key=f"edit_loser_{game_data['id']}"
    )

    game_format = st.selectbox(
        "Format",
        GameFormat.list(),
        index=GameFormat.list().index(game_data["format"]),
        key=f"edit_format_{game_data['id']}"
    )

    # Handle edition selection
    editions = ["None"] + Edition.list()[1:]  # All editions except NONE
    current_edition = game_data.get("edition", "None")
    if current_edition is None:
        current_edition = "None"

    selected_edition = st.selectbox(
        "Edition (optional)",
        options=editions,
        index=editions.index(current_edition),
        key=f"edit_edition_{game_data['id']}"
    )

    current_winner_colors = game_data.get("winner_colors", [])
    winner_colors = st.multiselect(
        "Winner's Colors",
        options=Color.list(),
        default=current_winner_colors,
        key=f"edit_winner_colors_{game_data['id']}"
    )

    current_loser_colors = game_data.get("loser_colors", [])
    loser_colors = st.multiselect(
        "Loser's Colors",
        options=Color.list(),
        default=current_loser_colors,
        key=f"edit_loser_colors_{game_data['id']}"
    )

    # Replace the 3-column button layout with 2 columns for main actions
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        save_button = st.button("Save Changes", key=f"save_{game_data['id']}")
    with col2:
        cancel_button = st.button("Cancel", key=f"cancel_{game_data['id']}")

    # Add delete button in a separate section below with warning coloring
    st.markdown("---")  # Visual separator
    delete_button = st.button("🗑️ Delete Game", key=f"delete_{game_data['id']}", type="secondary", help="Permanently delete this game")

    if cancel_button:
        del st.session_state[f"editing_game_{game_data['id']}"]
        st.rerun()

    if delete_button:
        if st.session_state.get(f"confirm_delete_{game_data['id']}", False):
            try:
                GameRepository.delete(game_data["id"])
                st.success("Game deleted successfully!")
                del st.session_state[f"editing_game_{game_data['id']}"]
                del st.session_state[f"confirm_delete_{game_data['id']}"]
                st.rerun()
            except Exception as e:
                st.error(f"Failed to delete game: {e}")
        else:
            st.session_state[f"confirm_delete_{game_data['id']}"] = True
            st.warning("Are you sure you want to delete this game? Click Delete again to confirm.")
            return

    if save_button:
        if winner == loser:
            st.error("Winner and loser cannot be the same player.")
            return

        try:
            # Create updated game object
            game = Game(
                winner_id=player_map[winner],
                loser_id=player_map[loser],
                game_format=GameFormat(game_format),
                winner_colors=[Color(c) for c in winner_colors],
                loser_colors=[Color(c) for c in loser_colors],
                edition=Edition(selected_edition) if selected_edition != "None" else None,
                played_at=datetime.fromisoformat(game_data["played_at"]) if game_data.get("played_at") else None,
                id=game_data["id"]
            )

            # Update in database
            GameRepository.update(game_data["id"], game)
            st.success("Game updated successfully!")
            del st.session_state[f"editing_game_{game_data['id']}"]
            st.rerun()  # Refresh the page to show updated data

        except Exception as e:
            st.error(f"Failed to update game: {e}")

def edit_game_modal(game_data: Dict[str, Any]) -> None:
    """Show edit game modal"""
    col1, col2 = st.columns([0.85, 0.15])
    with col2:
        if st.button("Edit", key=f"edit_button_{game_data['id']}"):
            st.session_state[f"editing_game_{game_data['id']}"] = True

    if st.session_state.get(f"editing_game_{game_data['id']}", False):
        with st.expander("Edit Game", expanded=True):
            render_edit_game_form(game_data)
