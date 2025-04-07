import streamlit as st
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

def add_player(name: str):
    return supabase.table("players").insert({"name": name}).execute()

def get_players():
    return supabase.table("players").select("*").execute().data

def add_game(winner_id, loser_id, game_format, winner_colors, loser_colors):
    return supabase.table("games").insert({
        "winner_id": winner_id,
        "loser_id": loser_id,
        "format": game_format,
        "winner_colors": winner_colors,
        "loser_colors": loser_colors
    }).execute()

def get_recent_games(limit=10):
    return supabase.table("games").select("*").order("played_at", desc=True).limit(limit).execute().data

def get_player_by_id(player_id):
    response = supabase.table("players").select("name").eq("id", player_id).limit(1).execute()
    if response.data:
        return response.data[0]["name"]
    return "Unknown"