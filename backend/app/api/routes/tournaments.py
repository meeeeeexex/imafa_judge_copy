from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.game import Game
from app.models.participant import Participant
from app.models.tournament import Tournament
from app.schemas.game import GameRead, GameSeatRead
from app.schemas.participant import ParticipantRead
from app.schemas.tournament import TournamentRead

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


@router.get("/{tournament_id}", response_model=TournamentRead)
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    t = db.get(Tournament, tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return t


@router.get("/{tournament_id}/participants", response_model=list[ParticipantRead])
def get_participants(tournament_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Participant)
        .filter(Participant.tournament_id == tournament_id)
        .order_by(Participant.id)
        .all()
    )


@router.get("/{tournament_id}/games", response_model=list[GameRead])
def get_games(tournament_id: int, db: Session = Depends(get_db)):
    games = (
        db.query(Game)
        .filter(Game.tournament_id == tournament_id)
        .order_by(Game.round_number, Game.table_number)
        .all()
    )
    return [_game_to_read(g) for g in games]


def _game_to_read(game: Game) -> GameRead:
    from app.core.enums import Team

    seats = [
        GameSeatRead(
            id=s.id,
            seat_number=s.seat_number,
            participant_id=s.participant_id,
            display_name=s.participant.display_name if s.participant else None,
            role=s.role,
            extra_points=s.extra_points,
        )
        for s in game.seats
    ]
    return GameRead(
        id=game.id,
        tournament_id=game.tournament_id,
        round_number=game.round_number,
        table_number=game.table_number,
        winning_team=game.winning_team,
        killed_first_night_seat=game.killed_first_night_seat,
        best_move_guesses=[g.guessed_seat_number for g in game.best_move_guesses],
        seats=seats,
    )
