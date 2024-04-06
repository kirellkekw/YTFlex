# pylint: disable=invalid-name, broad-exception-caught
"""This module contains the IO classes for the tables in the database."""

from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src.db_handler import _engine
from src.db_handler.tables import DownloadLog, API_Key

__all__ = ["DownloadLog_IO", "API_Key_IO", "get_session"]


def get_session():
    """Returns a new session to the database."""
    return Session(_engine)


class AbstractIO(ABC):
    """Abstract class for IO operations on the database."""

    @staticmethod
    @abstractmethod
    def _wipe(session: Session):
        """Deletes all entries in the table. Use with caution, or not at all."""

    @staticmethod
    @abstractmethod
    def get(entry_id: int, session: Session):
        """Returns the entry with the given id."""

    @staticmethod
    @abstractmethod
    def get_all(session: Session):
        """Returns all entries in the table."""

    @staticmethod
    @abstractmethod
    def delete(entry_id: int, session: Session):
        """Deletes the entry with the given id."""


class DownloadLog_IO(AbstractIO):
    """IO class for the DownloadLog table."""

    @staticmethod
    def _wipe(session: Session):
        try:
            session.query(DownloadLog).delete()
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

    @staticmethod
    def get(entry_id: int, session: Session):
        try:
            return session.get(DownloadLog, entry_id)
        except Exception as e:
            print(e)
            session.rollback()
            return None

    @staticmethod
    def get_all(session: Session):
        try:
            return session.query(DownloadLog).all()
        except Exception as e:
            print(e)
            session.rollback()
            return None

    @staticmethod
    def delete(entry_id: int, session: Session):
        try:
            session.query(DownloadLog).filter(DownloadLog.id == entry_id).delete()
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()


class API_Key_IO(AbstractIO):
    """IO class for the API_Key table."""

    @staticmethod
    def _wipe(session: Session):
        try:
            session.query(API_Key).delete()
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

    @staticmethod
    def get(entry_id: int, session: Session):
        try:
            return session.get(API_Key, entry_id)
        except Exception as e:
            print(e)
            session.rollback()
            return None

    @staticmethod
    def get_all(session: Session):
        try:
            return session.query(API_Key).all()
        except Exception as e:
            print(e)
            session.rollback()
            return None

    @staticmethod
    def delete(entry_id: int, session: Session):
        try:
            session.query(API_Key).filter(API_Key.id == entry_id).delete()
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
