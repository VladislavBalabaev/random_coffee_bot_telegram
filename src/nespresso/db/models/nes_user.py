from datetime import UTC, datetime

from sqlalchemy import JSON, BigInteger, Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from nespresso.db.base import Base


class NesUser(Base):
    __tablename__ = "nes_user"

    nes_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # Personal info
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String, nullable=True)

    # NES alumni info
    program: Mapped[str] = mapped_column(String, nullable=False)
    class_name: Mapped[str] = mapped_column(String, nullable=True)
    diploma_received: Mapped[bool] = mapped_column(Boolean, nullable=True)

    # Contacts
    email_primary: Mapped[str] = mapped_column(String, nullable=True)
    email_secondary: Mapped[str] = mapped_column(String, nullable=True)
    mobile_phone: Mapped[str] = mapped_column(String, nullable=True)
    work_phone: Mapped[str] = mapped_column(String, nullable=True)
    homepage_social: Mapped[str] = mapped_column(String, nullable=True)

    # NES specific
    research_interests: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    certificates: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    # Hobbies and expertise
    hobbies: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    industry_expertise: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    country_expertise: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    professional_expertise: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    # Work experiences
    main_work: Mapped[dict[str, str]] = mapped_column(JSON, nullable=True)
    additional_work: Mapped[list[dict[str, str]]] = mapped_column(JSON, nullable=True)

    # Education
    pre_nes_education: Mapped[list[dict[str, str]]] = mapped_column(JSON, nullable=True)
    post_nes_education: Mapped[list[dict[str, str]]] = mapped_column(
        JSON, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
