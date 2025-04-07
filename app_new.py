import streamlit as st
from db_new import add_player, get_players, add_game, get_recent_games, get_player_by_id

EDITION_OPTIONS = [
    "",
    "Tarkir Dragonstorm", "Innistrad Remastered", "Foundations", "Outlaws of Thunder Junction"
]

COLOR_OPTIONS = ["Blue", "Green", "Red", "White", "Black"]

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
    game_format = st.selectbox("Format", ["Draft", "Sealed", "Cube Draft", "Commander"])
    selected_edition = st.selectbox(
        "Edition",
        options=EDITION_OPTIONS,
        index=0
    )
    winner_colors = st.multiselect(
    "Winner's Colors",
    options=COLOR_OPTIONS,
    default=[]
)
    loser_colors = st.multiselect(
    "Loser's Colors",
    options=COLOR_OPTIONS,
    default=[]
)

    if st.button("Add Game Result"):
        if winner == loser:
            st.error("Winner and loser cannot be the same player.")
        else:
            add_game(
                winner_id=player_map[winner],
                loser_id=player_map[loser],
                game_format=game_format,
                selected_edition=selected_edition,
                winner_colors=winner_colors,
                loser_colors=loser_colors
            )
            st.success(f"Game result added: {winner} defeated {loser} in {game_format} format!")

st.header("Game History")
games = get_recent_games(limit=10)
for g in games:
    winner_name = get_player_by_id(g["winner_id"])
    loser_name = get_player_by_id(g["loser_id"])
    st.write(f"{winner_name} defeated {loser_name} in {g['format']} format on {g['played_at']}")


import pandas as pd
import matplotlib.pyplot as plt

st.header("Player Win Rates")

# Step 1: Load recent games
games = get_recent_games()

# Step 2: Count wins and losses
win_counts = {}
loss_counts = {}

for g in games:
    winner_id = g["winner_id"]
    loser_id = g["loser_id"]
    
    win_counts[winner_id] = win_counts.get(winner_id, 0) + 1
    loss_counts[loser_id] = loss_counts.get(loser_id, 0) + 1

# Step 3: Combine into a DataFrame
player_ids = set(win_counts) | set(loss_counts)
stats = []

for player_id in player_ids:
    name = get_player_by_id(player_id)
    wins = win_counts.get(player_id, 0)
    losses = loss_counts.get(player_id, 0)
    total = wins + losses
    win_rate = round((wins / total) * 100, 2) if total > 0 else 0
    stats.append({
        "Player": name,
        "Wins": wins,
        "Losses": losses,
        "Total Games": total,
        "Win Rate (%)": win_rate
    })

df = pd.DataFrame(stats).sort_values(by="Win Rate (%)", ascending=False)

# Step 4: Show table
st.dataframe(df)

# Step 5: Show bar chart of win rate
fig, ax = plt.subplots()
ax.bar(df["Player"], df["Win Rate (%)"], color="skyblue")
ax.set_title("Win Rate per Player")
ax.set_ylabel("Win Rate (%)")
ax.set_ylim(0, 100)
ax.set_xticklabels(df["Player"], rotation=45, ha="right")

st.pyplot(fig)
