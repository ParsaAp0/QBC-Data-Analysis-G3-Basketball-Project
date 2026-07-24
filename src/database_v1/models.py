from sqlalchemy import and_, Column, Integer, String, Float, Boolean
from sqlalchemy.dialects.sqlite import DATE
from sqlalchemy.orm import relationship

from db_connection import base


class Nationality(base):
    __tablename__ = "nationalities"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String)

    players = relationship("Player", back_populates='nationality')


class Position(base):
    __tablename__ = "positions"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    short_title = Column(String)
    title = Column(String)

    player_positions = relationship(
        "PlayerPosition", back_populates="position")
    player_seasons = relationship("PlayerSeason", back_populates='position')


class College(base):
    __tablename__ = "colleges"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String)

    players = relationship("Player", back_populates='college')


class Conference(base):
    __tablename__ = "conferences"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String)

    teams = relationship("Team", back_populates='conference')


class Division(base):
    __tablename__ = "divisions"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String)

    teams = relationship("Team", back_populates='division')


class Season(base):
    __tablename__ = "seasons"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String)

    team_seasons = relationship("TeamSeason", back_populates='season')


class Arena(base):
    __tablename__ = "arenas"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String)

    team_seasons = relationship("TeamSeason", back_populates='arena')


class PlayoffResult(base):
    __tablename__ = "playoff_results"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String)

    team_seasons = relationship("TeamSeason", back_populates='playoff_result')


class Player(base):
    __tablename__ = "players"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    _from = Column(String)
    to = Column(String)
    height = Column(Integer)
    weight = Column(Integer)
    birth_date = Column(DATE)
    experience = Column(Integer)
    shoots = Column(Boolean)

    nationality = relationship("Nationality", back_populates="players")
    player_positions = relationship("PlayerPosition", back_populates="player")
    college = relationship("College", back_populates="players")
    draft = relationship("Draft", back_populates="player", uselist=False)
    player_seasons = relationship("PlayerSeason", back_populates="player")


class Team(base):
    __tablename__ = "teams"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short_name = Column(String)
    franchise = Column(String)
    _from = Column(String)
    to = Column(String)
    playoff_appearances = Column(Integer)
    championships = Column(Integer)

    conference = relationship("Conference", back_populates="teams")
    division = relationship("Division", back_populates="teams")
    team_seasons = relationship("TeamSeason", back_populates='team')
    drafts = relationship("Draft", back_populates="team")


class Award(base):
    __tablename__ = "awards"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    short_name = Column(String)
    trophy_name = Column(String)
    description = Column(String)

    player_season_awards = relationship(
        "PlayerSeasonAward", back_populates="award")


class Draft(base):
    __tablename__ = "drafts"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    year = Column(String)
    round = Column(Integer)
    pick = Column(Integer)

    player = relationship("Player", back_populates="draft")
    team = relationship("Team", back_populates="drafts")


class PlayerPosition(base):
    __tablename__ = "player_positions"
    __table_args__ = {'keep_existing': True}

    player = relationship("Player", back_populates="player_positions")
    position = relationship("Position", back_populates="player_positions")


class TeamSeason(base):
    __tablename__ = "team_seasons"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    games = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    minutes_played = Column(Integer)
    pace_factor = Column(Float)
    relative_pace = Column(Float)
    offensive_rating = Column(Float)
    relative_offensive_rating = Column(Float)
    defensive_rating = Column(Float)
    relative_defensive_rating = Column(Float)
    points = Column(Integer)
    opponent_points_per_game = Column(Float)
    three_point_field_goals_made = Column(Integer)
    three_point_field_goals_attempts = Column(Integer)
    two_point_field_goals_made = Column(Integer)
    two_point_field_goals_attempts = Column(Integer)
    free_throws_made = Column(Integer)
    free_throws_attempts = Column(Integer)
    ft_per_fga = Column(Float)
    offensive_rebounds = Column(Float)
    offensive_rebound_percentage = Column(Float)
    defensive_rebounds = Column(Float)
    defensive_rebound_percentage = Column(Float)
    total_rebounds = Column(Float)
    total_rebound_percentage = Column(Float)
    assists = Column(Integer)
    assist_percentage = Column(Float)
    steals = Column(Integer)
    steal_percentage = Column(Float)
    blocks = Column(Integer)
    block_percentage = Column(Float)
    turnovers = Column(Integer)
    turnover_percentage = Column(Float)
    personal_fouls = Column(Integer)
    standing = Column(Integer)
    conference_standing = Column(Integer)
    conference_champion = Column(Boolean)
    champion = Column(Boolean)

    team = relationship("Team", back_populates="team_seasons")
    season = relationship("Season", back_populates="team_seasons")
    arena = relationship("Arena", back_populates="team_seasons")
    playoff_result = relationship(
        "PlayoffResult", back_populates="team_seasons")
    player_seasons = relationship("PlayerSeason", back_populates="team_season")


class PlayerSeason(base):
    __tablename__ = "player_seasons"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    games_played = Column(Integer)
    games_started = Column(Integer)
    minutes_played = Column(Integer)
    three_point_field_goals_made = Column(Float)
    three_point_field_goals_attempts = Column(Float)
    two_point_field_goals_made = Column(Float)
    two_point_field_goals_attempts = Column(Float)
    effective_field_goals_percentage = Column(Float)
    free_throws_made = Column(Float)
    free_throws_attempts = Column(Float)
    offensive_rebounds = Column(Float)
    offensive_rebound_percentage = Column(Float)
    defensive_rebounds = Column(Float)
    defensive_rebound_percentage = Column(Float)
    total_rebounds = Column(Float)
    total_rebound_percentage = Column(Float)
    assists = Column(Float)
    assist_percentage = Column(Float)
    steals = Column(Float)
    steal_percentage = Column(Float)
    blocks = Column(Float)
    block_percentage = Column(Float)
    turnovers = Column(Float)
    turnover_percentage = Column(Float)
    personal_fouls = Column(Float)
    points = Column(Float)
    player_efficiency_rating = Column(Float)

    player = relationship("Player", back_populates="player_seasons")
    team_season = relationship("TeamSeason", back_populates="player_seasons")
    position = relationship("Position", back_populates="player_seasons")
    player_season_awards = relationship(
        "PlayerSeasonAward", back_populates="player_season")


class PlayerSeasonAward(base):
    __tablename__ = "player_season_awards"
    __table_args__ = {'keep_existing': True}

    award = relationship("Award", back_populates="player_season_awards")
    player_season = relationship(
        "PlayerSeason", back_populates="player_season_awards")
