from typing import Any

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models, providing common functionality.
    """

    # methods do not affect mapping
    def IntoDict(self) -> dict[str, Any]:
        """
        Converts the model instance to a dictionary, excluding private attributes.
        """
        return {
            key: value for key, value in vars(self).items() if not key.startswith("_")
        }
