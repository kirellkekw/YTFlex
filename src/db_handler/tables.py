# pylint: disable=invalid-name

"""This module contains the SQLAlchemy tables for the database."""

from abc import ABC, abstractmethod
import datetime
from dataclasses import dataclass
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    SmallInteger,
)
from src.db_handler import _Base, _engine

__all__ = ["DownloadLog", "API_Key"]


class AbstractIO(ABC):
    """Abstract class for IO operations on the database."""

    @abstractmethod
    @staticmethod
    def _wipe():
        """Deletes all entries in the table. Use with caution, or not at all."""

    @abstractmethod
    @staticmethod
    def get(entry_id: int):
        """Returns the entry with the given id."""

    @abstractmethod
    @staticmethod
    def get_all():
        """Returns all entries in the table."""

    @abstractmethod
    @staticmethod
    def delete(entry_id: int):
        """Deletes the entry with the given id."""

@dataclass
class DownloadLog(_Base):
    """Table for storing download information."""

    __tablename__ = "ytflex_downloads"
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_string = Column(
        String(200), nullable=False
    )  # parsed ID of the video, can track parsing errors with this
    time_of_request = Column(
        DateTime, nullable=False, default=datetime.datetime.now
    )  # pass the time of the request no matter what
    status_code = Column(SmallInteger)  # inside codes for the status of the download
    type_of_request = Column(
        String(10), nullable=False
    )  # type of request, either "video", "audio", "playlist_video" or "playlist_audio"
    requested_resolution = Column(SmallInteger)
    downloaded_resolution = Column(SmallInteger)
    title = Column(String(100))
    duration = Column(SmallInteger)
    api_key = Column(String(40))
    file_size = Column(SmallInteger)
    time_of_response = Column(DateTime)
    playlist_url_count = Column(SmallInteger)
    custom_file_life = Column(SmallInteger)

@dataclass
class API_Key(_Base):
    """Table for storing API keys."""

    @staticmethod
    def _default_expiration():
        """Returns datetime object of 30 days from now."""
        return datetime.datetime.now() + datetime.timedelta(days=30)

    __tablename__ = "ytflex_api_keys"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(40), nullable=False)
    owner = Column(String(40), nullable=False)
    tier = Column(SmallInteger, default=1)
    is_active = Column(Boolean, default=True)
    additional_file_life_requested = Column(SmallInteger, default=0)  # in hours
    credits_used = Column(
        Integer, default=0
    )  # hours * video size, no penalty for < 1 hour
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    last_used = Column(DateTime)
    last_ip = Column(String(20))
    usage_count = Column(Integer, default=0, autoincrement=True)
    expires_at = Column(DateTime, default=_default_expiration)


_Base.metadata.create_all(_engine)
