"""
Easy import for all side processes.
"""

from src.api_handler.side_processes.purge_old_files import purge_old_files

# makes it easier to import everything from this file

__all__ = ["purge_old_files"]
