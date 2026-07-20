from sqlalchemy import create_engine, Table, Column, Integer, Float, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.sqlite import DATE
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

from typing import Any, Type

import re
import os
from dotenv import load_dotenv

load_dotenv()

base = declarative_base()


class Database:
    """
    A thin wrapper around SQLAlchemy engine and session.
    """

    def __init__(self) -> None:
        connection_string = os.getenv(
            "CONNECTION_STRING", "sqlite:///basketball_reference.db")

        self.engine = create_engine(connection_string)
        self.session = Session(self.engine)
        base.metadata.create_all(self.engine)

    # ------------------------------------------------------------------
    # Migrations
    # ------------------------------------------------------------------

    nationalities = Table(
        "nationalities",
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("title", String),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    positions = Table(
        "positions",
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("short_title", String(2)),
        Column("title", String),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    colleges = Table(
        "colleges",
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("title", String),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    conferences = Table(
        "conferences",
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("title", String),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    divisions = Table(
        "divisions",
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("title", String),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    seasons = Table(
        "seasons",
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("title", String),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    arenas = Table(
        "arenas",
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("title", String),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    playoff_results = Table(
        "playoff_results",
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("title", String),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    players = Table(
        "players",
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String),
        Column("_from", String),
        Column("to", String),
        Column("height", Integer),
        Column("weight", Integer),
        Column("birth_date", DATE),
        Column("experience", Integer),
        Column("shoots", Boolean),
        Column("nationality_id", ForeignKey("nationalities.id")),
        Column("college_id", ForeignKey("colleges.id")),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    teams = Table(
        "teams",
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String),
        Column("short_name", String),
        Column("franchise", String),
        Column("_from", String),
        Column("to", String),
        Column("playoff_appearances", Integer),
        Column("championships", Integer),
        Column("conference_id", ForeignKey("conferences.id")),
        Column("division_id", ForeignKey("divisions.id")),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    awards = Table(
        "awards",
        base.metadata,
        Column("id", Integer, primary_key=True),
        Column("short_name", String),
        Column("trophy_name", String),
        Column("description", String),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    drafts = Table(
        'drafts',
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("player_id", ForeignKey("players.id")),
        Column("year", String),
        Column("round", Integer),
        Column("pick", Integer),
        Column("team_id", ForeignKey("teams.id")),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    player_positions = Table(
        'player_positions',
        base.metadata,
        Column("player_id", ForeignKey("players.id"), primary_key=True),
        Column("position_id", ForeignKey("positions.id"), primary_key=True),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    team_seasons = Table(
        'team_seasons',
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("team_id", ForeignKey("teams.id")),
        Column("season_id", ForeignKey("seasons.id")),
        Column("arena_id", ForeignKey("arenas.id")),
        Column("games", Integer),
        Column("wins", Integer),
        Column("losses", Integer),
        Column("minutes_played", Integer),
        Column("pace_factor", Float),
        Column("relative_pace", Float),
        Column("offensive_rating", Float),
        Column("relative_offensive_rating", Float),
        Column("defensive_rating", Float),
        Column("relative_defensive_rating", Float),
        Column("points", Integer),
        Column("opponent_points_per_game", Float),
        Column("three_point_field_goals_made", Integer),
        Column("three_point_field_goals_attempts", Integer),
        Column("two_point_field_goals_made", Integer),
        Column("two_point_field_goals_attempts", Integer),
        Column("free_throws_made", Integer),
        Column("free_throws_attempts", Integer),
        Column("ft_per_fga", Float),
        Column("offensive_rebounds", Float),
        Column("offensive_rebound_percentage", Float),
        Column("defensive_rebounds", Float),
        Column("defensive_rebound_percentage", Float),
        Column("total_rebounds", Float),
        Column("total_rebound_percentage", Float),
        Column("assists", Integer),
        Column("assist_percentage", Float),
        Column("steals", Integer),
        Column("steal_percentage", Float),
        Column("blocks", Integer),
        Column("block_percentage", Float),
        Column("turnovers", Integer),
        Column("turnover_percentage", Float),
        Column("personal_fouls", Integer),
        Column("standing", Integer),
        Column("conference_standing", Integer),
        Column("playoff_result_id", ForeignKey("playoff_results.id")),
        Column("conference_champion", Boolean),
        Column("champion", Boolean),
        keep_existing=True,
        sqlite_autoincrement=True,
        __table_args__=(
            UniqueConstraint('team_id', 'season_id', name='uq_team_season'),
        )
    )

    player_seasons = Table(
        'player_seasons',
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("player_id", ForeignKey("players.id")),
        Column("team_season_id", ForeignKey("team_seasons.id")),
        Column("postion_id", ForeignKey("positions.id")),
        Column("games_played", Integer),
        Column("games_started", Integer),
        Column("minutes_played", Integer),
        Column("three_point_field_goals_made", Float),
        Column("three_point_field_goals_attempts", Float),
        Column("two_point_field_goals_made", Float),
        Column("two_point_field_goals_attempts", Float),
        Column("effective_field_goals_percentage", Float),
        Column("free_throws_made", Float),
        Column("free_throws_attempts", Float),
        Column("offensive_rebounds", Float),
        Column("offensive_rebound_percentage", Float),
        Column("defensive_rebounds", Float),
        Column("defensive_rebound_percentage", Float),
        Column("total_rebounds", Float),
        Column("total_rebound_percentage", Float),
        Column("assists", Float),
        Column("assist_percentage", Float),
        Column("steals", Float),
        Column("steal_percentage", Float),
        Column("blocks", Float),
        Column("block_percentage", Float),
        Column("turnovers", Float),
        Column("turnover_percentage", Float),
        Column("personal_fouls", Float),
        Column("points", Float),
        Column("player_efficiency_rating", Float),
        keep_existing=True,
        sqlite_autoincrement=True,
        __table_args__=(
            UniqueConstraint('player_id', 'team_season_id',
                             name='uq_player_team_season'),
        )
    )

    player_season_awards = Table(
        'player_season_awards',
        base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("award_id", ForeignKey("awards.id")),
        Column(
            "player_season_id",
            ForeignKey("player_seasons.id")
        ),
        keep_existing=True,
        sqlite_autoincrement=True
    )

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

        self.close()

    # ------------------------------------------------------------------
    # Database lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the current session."""
        self.session.close()

    # ------------------------------------------------------------------
    # Session helpers
    # ------------------------------------------------------------------

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def add(self, instance: Any) -> None:
        self.session.add(instance)

    def flush(self) -> None:
        self.session.flush()

    # ------------------------------------------------------------------
    # Generic helpers
    # ------------------------------------------------------------------

    def get(self, model: Type, primary_key: Any):
        """Return an object by primary key."""

        return self.session.get(model, primary_key)
    
    def find_first(self, model: Type, **filters):
        """Return an object by filter."""

        return self.session.query(model).filter_by(**filters).first()

    def exists(self, model: Type, **filters) -> bool:
        """Return True if a matching row exists."""

        return (
            self.session
            .query(model)
            .filter_by(**filters)
            .first()
            is not None
        )

    def get_or_create(
        self,
        model: Type,
        *,
        lookup: dict[str, Any],
        defaults: dict[str, Any] | None = None,
    ):
        """
        Return an existing object or create a new one.

        Args:
            model: SQLAlchemy model class.
            lookup: Fields used to search for an existing object.
            defaults: Additional fields used only when creating a new object.

        Returns:
            tuple(instance, created)
        """

        defaults = defaults or {}

        instance = (
            self.session
            .query(model)
            .filter_by(**lookup)
            .first()
        )

        if instance is not None:
            return instance, False

        instance = model(
            **lookup,
            **defaults,
        )

        self.session.add(instance)

        try:
            self.session.flush()
        except IntegrityError:
            # Another transaction may have created the row.
            self.session.rollback()

            instance = (
                self.session
                .query(model)
                .filter_by(**lookup)
                .one()
            )

            return instance, False

        return instance, True

    def count(self, model: Type) -> int:
        """Return the number of rows in a table."""

        return self.session.query(model).count()
