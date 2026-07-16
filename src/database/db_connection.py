from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

from typing import Any, Type

import os
from dotenv import load_dotenv

load_dotenv()

base = declarative_base()

class Database:
    """
    A thin wrapper around SQLAlchemy engine and session.
    """

    def __init__(self) -> None:
        connection_string = os.getenv("CONNECTION_STRING")

        self.engine = create_engine(connection_string)
        self.session = Session(self.engine)
        base.metadata.create_all(self.engine)
    
    # ------------------------------------------------------------------
    # Migrations
    # ------------------------------------------------------------------
    
    players = Table(
        "players",
        base.metadata,
        Column("id", String, primary_key=True),
        keep_existing=True
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
    
    from typing import Type

    def count(self, model: Type) -> int:
        """Return the number of rows in a table."""
        
        return self.session.query(model).count()
