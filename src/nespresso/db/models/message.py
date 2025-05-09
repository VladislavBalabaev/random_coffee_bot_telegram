from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import BigInteger, DateTime, Enum as SqlEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from nespresso.db.base import Base


class MessageSide(Enum):
    Bot = "bot"
    User = "user"


class Message(Base):
    __tablename__ = "message"

    message_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )

    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(tz=UTC)
    )
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    side: Mapped[MessageSide] = mapped_column(SqlEnum(MessageSide), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
