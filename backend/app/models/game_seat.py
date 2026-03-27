from typing import Optional

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class GameSeat(Base):
    __tablename__ = "game_seats"
    __table_args__ = (
        UniqueConstraint("game_id", "seat_number", name="uq_game_seat"),
        UniqueConstraint("game_id", "participant_id", name="uq_game_participant"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    seat_number: Mapped[int]
    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id"))
    role: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    extra_points: Mapped[float] = mapped_column(default=0.0)

    game = relationship("Game", back_populates="seats")
    participant = relationship("Participant")
