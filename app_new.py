import streamlit as st
from db_new import add_player, get_players, add_game, get_recent_games, get_player_by_id
from plot import plot_player_win_rates
import matplotlib.pyplot as plt
import pandas as pd

EDITION_OPTIONS = [
    "",
    "Tarkir Dragonstorm", "Innistrad Remastered", "Foundations", "Outlaws of Thunder Junction"
]

COLOR_OPTIONS = ["Blue", "Green", "Red", "White", "Black"]

def to_pg_array(py_list):
    return f"{{{','.join([f'\"{item}\"' for item in py_list])}}}"

st.title("Magic The Gathering Game Logger")

st.header("Add game result")
players = get_players()
player_map = {p["name"]: p["id"] for p in players}
player_names = list(player_map.keys())

if not player_names:
    st.warning("Add some players first!")
else:
    winner = st.selectbox("Winner", player_names, key="winner")
    loser = st.selectbox("Loser", player_names, key="loser")
    game_format = st.selectbox("Format", ["Draft", "Sealed", "Cube Draft", "Constructed", "Commander"])
    selected_edition = st.selectbox(
        "Edition",
        options=EDITION_OPTIONS,
        index=0
    )
    winner_colors = st.multiselect("Winner's Colors", options=COLOR_OPTIONS, default=[])
    loser_colors = st.multiselect("Loser's Colors", options=COLOR_OPTIONS, default=[])

    if st.button("Add Game Result"):
        if winner == loser:
            st.error("Winner and loser cannot be the same player.")
        else:
            add_game(
                winner_id=player_map[winner],
                loser_id=player_map[loser],
                game_format=game_format,
                selected_edition=selected_edition,
                winner_colors=to_pg_array(winner_colors),
                loser_colors=to_pg_array(loser_colors)
            )
            st.success(f"Game result added: {winner} defeated {loser} in {game_format} format!")

st.header("Game History")
games = get_recent_games(limit=5)
for g in games:
    winner_name = get_player_by_id(g["winner_id"])
    loser_name = get_player_by_id(g["loser_id"])
    st.write(f"{winner_name} defeated {loser_name} in {g['format']} format on {g['played_at']}")


st.header("Player Win Rates")
plot_player_win_rates()

st.header("Player Win Rate by Color")

# Step 1: Get the list of players
players = get_players()  # Fetch all players
player_map = {p["name"]: p["id"] for p in players}  # Map names to player IDs

# Step 2: Player selection
selected_player_name = st.selectbox("Select Player", list(player_map.keys()))

# Step 3: Fetch games for the selected player
player_id = player_map[selected_player_name]

# Query games where the selected player is the winner or loser
games = get_recent_games()  # Fetch all recent games (can be optimized if needed)

# Filter games involving the selected player
player_games = [
    g for g in games 
    if (g["winner_id"] == player_id or g["loser_id"] == player_id) and
       g.get("winner_colors") is not None and
       g.get("loser_colors") is not None
]

# Step 4: Calculate wins and losses by color for the selected player
win_counts = {}
loss_counts = {}

for g in player_games:
    winner_id = g["winner_id"]
    loser_id = g["loser_id"]

    if winner_id == player_id:
        winner_colors = g["winner_colors"]
        for color in winner_colors:
            win_counts[color] = win_counts.get(color, 0) + 1
    elif loser_id == player_id:
        loser_colors = g["loser_colors"]
        for color in loser_colors:
            loss_counts[color] = loss_counts.get(color, 0) + 1

# Step 5: Prepare Data for Plotting
all_colors = set(win_counts.keys()) | set(loss_counts.keys())
stats = []

for color in all_colors:
    wins = win_counts.get(color, 0)
    losses = loss_counts.get(color, 0)
    total = wins + losses
    win_rate = round((wins / total) * 100, 2) if total > 0 else 0
    stats.append({
        "Color": color,
        "Wins": wins,
        "Losses": losses,
        "Total Games": total,
        "Win Rate (%)": win_rate
    })

df = pd.DataFrame(stats).sort_values(by="Win Rate (%)", ascending=False)

# Step 6: Display Table
st.subheader(f"Win Rates for {selected_player_name} by Color")
st.dataframe(df)

# Step 7: Display Bar Chart
fig, ax = plt.subplots()
ax.bar(df["Color"], df["Win Rate (%)"], color="skyblue")
ax.set_title(f"Win Rate per Color for {selected_player_name}")
ax.set_ylabel("Win Rate (%)")
ax.set_ylim(0, 100)
ax.set_xticklabels(df["Color"], rotation=45, ha="right")

st.pyplot(fig)



st.header("Add new player")
new_player = st.text_input("Player name")
if st.button("Add Player"):
    try:
        add_player(new_player)
        st.success(f"Player {new_player} added successfully!")
    except Exception as e:
        st.error(f"Failed to add player: {e}")