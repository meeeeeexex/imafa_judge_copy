from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.routes.tournaments import _game_to_read
from app.db.session import get_db
from app.models.game import Game
from app.schemas.game import GameRead, GameResultInput
from app.services.game_results import validate_and_save_result

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/{game_id}", response_model=GameRead)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return _game_to_read(game)


@router.put("/{game_id}/result", response_model=GameRead)
def submit_game_result(
    game_id: int, data: GameResultInput, db: Session = Depends(get_db)
):
    game = db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    game = validate_and_save_result(db, game, data)
    return _game_to_read(game)
