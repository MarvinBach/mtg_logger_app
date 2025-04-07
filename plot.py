import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from db_new import get_player_by_id, get_players, get_recent_games

def plot_player_win_rates() -> None: 
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
    #fig, ax = plt.subplots()
    #ax.bar(df["Player"], df["Win Rate (%)"], color="skyblue")
    #ax.set_title("Win Rate per Player")
    #ax.set_ylabel("Win Rate (%)")
    #ax.set_ylim(0, 100)
    #ax.set_xticklabels(df["Player"], rotation=45, ha="right")

    #st.pyplot(fig)


def plot_player_win_rates_by_color() -> None:
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
