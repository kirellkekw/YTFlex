"""This module contains the IO classes for the tables in the database."""

from src.db_handler.tables import DownloadLog, AbstractIO, API_Key
from sqlalchemy.orm import Session
from src.db_handler import _engine

__all__ = ["DownloadLog_IO", "API_Key_IO", "get_session"]


def get_session():
    """Returns a new session to the database."""
    return Session(_engine)


class DownloadLog_IO(AbstractIO):
    """IO class for the DownloadLog table."""

    @staticmethod
    def _wipe():
        try:
            session = get_session()
            session.query(DownloadLog).delete()
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

    @staticmethod
    def get(entry_id: int):
        try:
            session = get_session()
            return session.get(DownloadLog, entry_id)
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def get_all():
        try:
            session = get_session()
            return session.query(DownloadLog).all()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def delete(entry_id: int):
        try:
            session = get_session()
            session.query(DownloadLog).filter(DownloadLog.id == entry_id).delete()
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()


class API_Key_IO(AbstractIO):
    """IO class for the API_Key table."""

    @staticmethod
    def _wipe():
        try:
            session = get_session()
            session.query(API_Key).delete()
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def get(entry_id: int):
        try:
            session = get_session()
            return session.get(API_Key, entry_id)
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def get_all():
        try:
            session = get_session()
            return session.query(API_Key).all()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def delete(entry_id: int):
        try:
            session = get_session()
            session.query(API_Key).filter(API_Key.id == entry_id).delete()
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
