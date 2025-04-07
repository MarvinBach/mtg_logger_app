import streamlit as st
from db_new import add_player, get_players, add_game, get_recent_games, get_player_by_id

st.title("Magic The Gathering Game Logger")

st.header("Add new player")
new_player = st.text_input("Player name")
if st.button("Add Player"):
    try:
        add_player(new_player)
        st.success(f"Player {new_player} added successfully!")
    except Exception as e:
        st.error(f"Failed to add player: {e}")

st.header("Add game result")
players = get_players()
player_map = {p["name"]: p["id"] for p in players}
player_names = list(player_map.keys())

if not player_names:
    st.warning("Add some players first!")
else:
    winner = st.selectbox("Winner", player_names, key="winner")
    loser = st.selectbox("Loser", player_names, key="loser")
    game_format = st.selectbox("Format", ["Draft", "Cube", "Commander"])
    winner_colors = st.text_input("Winner's colors (comma-separated)", key="winner_colors")
    loser_colors = st.text_input("Loser's colors (comma-separated)", key="loser_colors")

    if st.button("Add Game Result"):
        if winner == loser:
            st.error("Winner and loser cannot be the same player.")
        else:
            add_game(
                winner_id=player_map[winner],
                loser_id=player_map[loser],
                game_format=game_format,
                winner_colors=winner_colors,
                loser_colors=loser_colors
            )
            st.success(f"Game result added: {winner} defeated {loser} in {game_format} format!")

st.header("Game History")
games = get_recent_games()
for g in games:
    winner_name = get_player_by_id(g["winner_id"])
    loser_name = get_player_by_id(g["loser_id"])
    st.write(f"{winner_name} defeated {loser_name} in {g['format']} format on {g['played_at']}")
