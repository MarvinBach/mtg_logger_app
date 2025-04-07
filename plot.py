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

def plot_player_win_rates_by_color():
    players = get_players()
    player_map = {p["name"]: p["id"] for p in players}

    selected_player_name = st.selectbox("Select Player", list(player_map.keys()))
    player_id = player_map[selected_player_name]

    games = get_recent_games()

    # Filter games with valid color data and where the player participated
    player_games = [
        g for g in games
        if (g["winner_id"] == player_id or g["loser_id"] == player_id)
        and isinstance(g.get("winner_colors"), list)
        and isinstance(g.get("loser_colors"), list)
    ]

    win_counts = {}
    loss_counts = {}

    for g in player_games:
        if g["winner_id"] == player_id:
            for color in g["winner_colors"]:
                win_counts[color] = win_counts.get(color, 0) + 1
        elif g["loser_id"] == player_id:
            for color in g["loser_colors"]:
                loss_counts[color] = loss_counts.get(color, 0) + 1

    all_colors = sorted(set(win_counts.keys()) | set(loss_counts.keys()))
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

    df = pd.DataFrame(stats)

    st.subheader(f"Win Rates for {selected_player_name} by Color")
    st.dataframe(df)

    if not df.empty:
        fig, ax = plt.subplots()
        ax.bar(df["Color"], df["Win Rate (%)"], color="skyblue")
        ax.set_title(f"Win Rate per Color for {selected_player_name}")
        ax.set_ylabel("Win Rate (%)")
        ax.set_ylim(0, 100)
        ax.set_xticks(range(len(df["Color"])))
        ax.set_xticklabels(df["Color"], rotation=45, ha="right")
        st.pyplot(fig)
    else:
        st.info("No game data available for selected player with valid color info.")

