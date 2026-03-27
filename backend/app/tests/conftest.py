import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.tournament import Tournament
from app.models.participant import Participant
from app.models.game import Game
from app.models.game_seat import GameSeat
from app.models.best_move import BestMoveGuess  # noqa: F401


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def seeded_db(db):
    """DB with 1 tournament, 10 participants, 1 game with 10 seats."""
    tournament = Tournament(id=1, name="Test Tournament")
    db.add(tournament)
    db.flush()

    names = ["Alice", "Bob", "Charlie", "Diana", "Eve",
             "Frank", "Grace", "Hank", "Ivy", "Jack"]
    for i, name in enumerate(names, start=1):
        db.add(Participant(id=i, tournament_id=1, display_name=name))
    db.flush()

    game = Game(id=1, tournament_id=1, round_number=1, table_number=1)
    db.add(game)
    db.flush()

    for seat_num in range(1, 11):
        db.add(GameSeat(game_id=1, seat_number=seat_num, participant_id=seat_num))
    db.commit()

    return db
