from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.standings import StandingsEntry
from app.services.standings import compute_standings

router = APIRouter(tags=["standings"])


@router.get(
    "/tournaments/{tournament_id}/standings", response_model=list[StandingsEntry]
)
def get_standings(tournament_id: int, db: Session = Depends(get_db)):
    return compute_standings(db, tournament_id)
