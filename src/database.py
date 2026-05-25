"""Database models and SQLAlchemy setup."""

import os
from datetime import datetime

from sqlalchemy import create_engine, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    from pathlib import Path
    DATABASE_PATH = Path(__file__).parent.parent / "deploys.db"
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


class Base(DeclarativeBase):
    pass


class Deploy(Base):
    __tablename__ = "deploys"

    id: Mapped[int] = mapped_column(primary_key=True)
    repo: Mapped[str] = mapped_column(String(255), nullable=False)
    branch: Mapped[str] = mapped_column(String(255), nullable=False)
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    provider: Mapped[str] = mapped_column(String(20), default="aws")
    duration_s: Mapped[float] = mapped_column(Float, nullable=False)
    runner_size: Mapped[str] = mapped_column(String(20), default="medium")
    co2_grams: Mapped[float] = mapped_column(Float, nullable=False)
    carbon_intensity: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    commit_sha: Mapped[str] = mapped_column(String(40), nullable=True)
    workflow_name: Mapped[str] = mapped_column(String(255), nullable=True)


engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)


def get_session():
    return SessionLocal()