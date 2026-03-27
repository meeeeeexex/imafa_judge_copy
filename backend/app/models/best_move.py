from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BestMoveGuess(Base):
    __tablename__ = "best_move_guesses"
    __table_args__ = (
        UniqueConstraint("game_id", "guessed_seat_number", name="uq_game_guess"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    guessed_seat_number: Mapped[int]

    game = relationship("Game", back_populates="best_move_guesses")
