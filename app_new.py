import streamlit as st
from db import SessionLocal, init_db
from models import Player, Game
from sqlalchemy.exc import IntegrityError

# Initialize the database (create tables if not exist)
init_db()

st.title("Magic The Gathering Game Logger")
session = SessionLocal()

# Add new player
st.header("Add new player")
new_player = st.text_input("Player name")
if st.button("Add Player"):
    try:
        player = Player(name=new_player)
        session.add(player)
        session.commit()
        st.success(f"Player {new_player} added successfully!")
    except IntegrityError:
        session.rollback()
        st.error(f"Player {new_player} already exists!")

# Add game result
st.header("Add game result") 
players = session.query(Player).all()
player_names = [p.name for p in players]

winner = st.selectbox("Winner", player_names, key="winner")
loser = st.selectbox("Loser", player_names, key="loser")
game_format = st.selectbox("Format", ["Draft", "Cube", "Commander"])
winner_colors = st.text_input("Winner's colors (comma-separated)", key="winner_colors")
loser_colors = st.text_input("Loser's colors (comma-separated)", key="loser_colors")

if st.button("Add Game Result"):
    winner_id = [p.id for p in players if p.name == winner][0]
    loser_id = [p.id for p in players if p.name == loser][0]
    game = Game(winner_id=winner_id, loser_id=loser_id, format=game_format,
                winner_colors=winner_colors, loser_colors=loser_colors)
    session.add(game)
    session.commit()
    st.success(f"Game result added: {winner} defeated {loser} in {game_format} format!")

# Show game history
st.header("Game History")
games = session.query(Game).order_by(Game.played_at.desc()).limit(10).all()
for g in games: 
    winner_name = session.query(Player).get(g.winner_id).name
    loser_name = session.query(Player).get(g.loser_id).name
    st.write(f"{winner_name} defeated {loser_name} in {g.format} format on {g.played_at}.")
