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

def delete_player(player_id: int):
    response = supabase.table("players").delete().eq("id", player_id).execute()
    return response

def add_game(winner_id, loser_id, game_format, selected_edition, winner_colors, loser_colors):
    data = {
        "winner_id": winner_id,
        "loser_id": loser_id,
        "format": game_format,
        "edition": selected_edition,
        "winner_colors": winner_colors,
        "loser_colors": loser_colors
    }
    response = supabase.table("games").insert(data).execute()
    return response

def get_recent_games(limit=None):
    query = supabase.table("games").select("*").order("played_at", desc=True)
    if limit is not None:
        query = query.limit(limit)
    return query.execute().data

def get_player_by_id(player_id):
    response = supabase.table("players").select("name").eq("id", player_id).limit(1).execute()
    if response.data:
        return response.data[0]["name"]
    return "Unknown"