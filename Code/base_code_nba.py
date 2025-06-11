from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Time, ForeignKey, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship



# Create a base class for declarative class definitions
Base = declarative_base()

class Game(Base):
    __tablename__ = 'game'
    game_id = Column(Integer, primary_key=True)
    home_team_id = Column(Integer, ForeignKey('teams.team_id', ondelete='CASCADE'))
    away_team_id = Column(Integer, ForeignKey('teams.team_id', ondelete='CASCADE'))
    game_time = Column(Time)
    game_date = Column(Date)
    streaming_platform = Column(String)
    is_active = Column(Boolean)
    game_period = Column(String)
    time_remaining = Column(Time)
    winning_team_id = Column(Integer, ForeignKey('teams.team_id', ondelete='CASCADE'))

    active_lineups = relationship("ActiveLineup", back_populates="game", cascade="all, delete-orphan", passive_deletes=True)


class Team(Base):
    __tablename__ = 'teams'
    team_id = Column(Integer, primary_key=True)
    team_name = Column(String)
    conf_name = Column(String)
    division_name = Column(String)
    win_count = Column(Integer)
    loss_count = Column(Integer)
    win_percentage = Column(Double)
    game_balance = Column(Integer)

    players = relationship("Player", back_populates="team", cascade="all, delete-orphan", passive_deletes=True)
    arenas = relationship("Arena", back_populates="team", cascade="all, delete-orphan", passive_deletes=True)
    active_lineups = relationship("ActiveLineup", back_populates="team", cascade="all, delete-orphan", passive_deletes=True)


class Player(Base):
    __tablename__ = 'players'
    player_id = Column(Integer, primary_key=True)
    player_name = Column(String)
    team_id = Column(Integer, ForeignKey('teams.team_id', ondelete='CASCADE'))
    position = Column(String)
    player_status = Column(String)

    team = relationship("Team", back_populates="players", passive_deletes=True)
    active_lineups = relationship("ActiveLineup", back_populates="player", cascade="all, delete-orphan", passive_deletes=True)
    offensive_stats = relationship("OffensiveStats", back_populates="player", cascade="all, delete-orphan", passive_deletes=True)
    defensive_stats = relationship("DefensiveStats", back_populates="player", cascade="all, delete-orphan", passive_deletes=True)


class ActiveLineup(Base):
    __tablename__ = 'active_lineup'
    team_id = Column(Integer, ForeignKey('teams.team_id', ondelete='CASCADE'), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id', ondelete='CASCADE'), primary_key=True)
    game_id = Column(Integer, ForeignKey('game.game_id', ondelete='CASCADE'), primary_key=True)
    is_starter = Column(Boolean)
    on_court = Column(Boolean)

    player = relationship("Player", back_populates="active_lineups", passive_deletes=True)
    team = relationship("Team", back_populates="active_lineups", passive_deletes=True)
    game = relationship("Game", back_populates="active_lineups", passive_deletes=True)


class Arena(Base):
    __tablename__ = 'arena'
    arena_id = Column(Integer, primary_key=True)
    arena_name = Column(String)
    team_id = Column(Integer, ForeignKey('teams.team_id', ondelete='CASCADE'))
    location = Column(String)

    team = relationship("Team", back_populates="arenas", passive_deletes=True)


class OffensiveStats(Base):
    __tablename__ = 'offensive_player_stats_in_game'
    player_id = Column(Integer, ForeignKey('players.player_id', ondelete='CASCADE'), primary_key=True)
    game_id = Column(Integer, ForeignKey('game.game_id', ondelete='CASCADE'), primary_key=True)
    minutes = Column(Integer)
    points = Column(Integer)
    o_rebound = Column(Integer)
    assist = Column(Integer)
    made_shots = Column(Integer)
    made_3 = Column(Integer)
    made_free_throw = Column(Integer)
    turnover = Column(Integer)
    total_shots_attempt = Column(Integer)
    total_3_attempt = Column(Integer)
    total_free_throw = Column(Integer)

    player = relationship("Player", back_populates="offensive_stats", passive_deletes=True)


class DefensiveStats(Base):
    __tablename__ = 'defensive_player_stats_in_game'
    player_id = Column(Integer, ForeignKey('players.player_id', ondelete='CASCADE'), primary_key=True)
    game_id = Column(Integer, ForeignKey('game.game_id', ondelete='CASCADE'), primary_key=True)
    minutes = Column(Integer)
    steal = Column(Integer)
    d_rebound = Column(Integer)
    block = Column(Integer)
    personal_foul = Column(Integer)

    player = relationship("Player", back_populates="defensive_stats", passive_deletes=True)


if __name__ == "__main__":
    from sqlalchemy import create_engine
engine = create_engine('sqlite:///NBA_BoxScore.db')
Base.metadata.create_all(engine)