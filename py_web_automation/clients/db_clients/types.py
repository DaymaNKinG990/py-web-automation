"""
Type definitions for database clients.

This module contains shared types and enums used across database client modules.
"""

# Python imports
from enum import StrEnum


class DBCommandType(StrEnum):
    """Database command type."""

    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

