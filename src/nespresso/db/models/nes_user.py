from datetime import datetime

from sqlalchemy import JSON, BigInteger, DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column

from nespresso.db.base import Base


class NesUser(Base):
    __tablename__ = "nes_user"

    nes_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # Personal info
    name: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String, nullable=True)

    # NES alumni info
    program: Mapped[str] = mapped_column(String, nullable=True)
    class_name: Mapped[str] = mapped_column(String, nullable=True)

    # Hobbies and expertise
    hobbies: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    industry_expertise: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    country_expertise: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    professional_expertise: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    # Work experiences
    main_work: Mapped[dict[str, str]] = mapped_column(JSON, nullable=True)
    additional_work: Mapped[list[dict[str, str]]] = mapped_column(JSON, nullable=True)

    # Education
    pre_nes_educ: Mapped[list[dict[str, str]]] = mapped_column(JSON, nullable=True)
    post_nes_educ: Mapped[list[dict[str, str]]] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
