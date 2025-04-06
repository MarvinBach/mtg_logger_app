from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime


Base = declarative_base()

class Player(Base): 
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique = True, nullable=False)

    def __repr__(self):
        return f"Player(id={self.id}, name='{self.name}')"
    
class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    winner_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    loser_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    format = Column(String, nullable=False)
    winner_colors = Column(String, nullable=True)
    loser_colors = Column(String, nullable=True)
    played_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return (f"Game(id={self.id}, winner_id={self.winner_id}, loser_id={self.loser_id}, "
                f"format='{self.format}', winner_colors='{self.winner_colors}', "
                f"loser_colors='{self.loser_colors}', played_at='{self.played_at}')")