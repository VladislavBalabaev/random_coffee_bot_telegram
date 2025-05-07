import datetime
from enum import Enum

from sqlalchemy import BigInteger, DateTime, Enum as SqlEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from nespresso.db.base import Base


class MessageSide(Enum):
    Bot = "bot"
    User = "user"


class Message(Base):
    __tablename__ = "messages"

    chat_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, index=True
    )  # what is key in this table??

    time: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(tz=datetime.UTC)
    )
    side: Mapped[MessageSide] = mapped_column(SqlEnum(MessageSide), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
