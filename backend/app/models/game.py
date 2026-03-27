from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
    round_number: Mapped[int]
    table_number: Mapped[int]
    winning_team: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    killed_first_night_seat: Mapped[Optional[int]] = mapped_column(nullable=True)

    tournament = relationship("Tournament", back_populates="games")
    seats = relationship("GameSeat", back_populates="game", order_by="GameSeat.seat_number")
    best_move_guesses = relationship("BestMoveGuess", back_populates="game", cascade="all, delete-orphan")
