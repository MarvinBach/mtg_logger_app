import streamlit as st
from models import Player


def add_new_player() -> None:
    new_player = st.text_input("Player name")
    if st.button("Add Player"):
        if not new_player.strip():
            st.error("Player name cannot be empty.")
        else:
            try:
                Player.add(name=new_player)
                st.success(f"Player {new_player} added successfully!")
            except Exception as e:
                st.error(f"Failed to add player: {e}")
