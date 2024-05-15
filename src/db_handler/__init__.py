"""
Database handler package for the ytflex project. 
Contains the database engine and the base object for all tables.
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import config

__all__ = ["_engine", "_Base"]  # private namespace since it won't leave the package

_db_string = config.get(
    "database_url",
    f"sqlite:///{Path(__file__).resolve().parent.parent.parent.as_posix()}"
    + "/mountpoint/database/ytflex_database.db",
)
# Create the database engine
_engine = create_engine(_db_string)

# Base object for all tables
_Base = declarative_base()
# modules are in private namespace since they are only used by the adapters
# and not meant to be used outside of the db_handler package
# if you're creating a new table, import _Base from here, despite the fact that it's private
# it's not a very elegant solution, but it's the best I could come up with
# bear with me here, thanks
