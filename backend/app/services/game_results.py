from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import Role, Team
from app.models.best_move import BestMoveGuess
from app.models.game import Game
from app.models.game_seat import GameSeat
from app.schemas.game import GameResultInput
from app.services.scoring import calc_best_move_bonus


def validate_and_save_result(db: Session, game: Game, data: GameResultInput) -> Game:
    existing_seats = {s.seat_number: s for s in game.seats}
    expected_seat_numbers = set(existing_seats.keys())

    # Validate all submitted seats match existing seating
    submitted_seat_numbers = {s.seat_number for s in data.seats}
    if submitted_seat_numbers != expected_seat_numbers:
        raise HTTPException(
            status_code=400,
            detail=f"Seats mismatch. Expected {sorted(expected_seat_numbers)}, "
            f"got {sorted(submitted_seat_numbers)}",
        )

    # Validate participant_ids match
    for seat_input in data.seats:
        existing = existing_seats[seat_input.seat_number]
        if seat_input.participant_id != existing.participant_id:
            raise HTTPException(
                status_code=400,
                detail=f"Seat {seat_input.seat_number}: participant mismatch. "
                f"Expected {existing.participant_id}, got {seat_input.participant_id}",
            )

    # Validate killed_first_night_seat
    if data.killed_first_night_seat is not None:
        if data.killed_first_night_seat not in expected_seat_numbers:
            raise HTTPException(
                status_code=400,
                detail=f"killed_first_night_seat {data.killed_first_night_seat} is not a valid seat",
            )

    # Validate best_move_guesses are valid seats
    for guess_sn in data.best_move_guesses:
        if guess_sn not in expected_seat_numbers:
            raise HTTPException(
                status_code=400,
                detail=f"Best move guess seat {guess_sn} is not a valid seat",
            )

    # If best_move_guesses provided, killed_first_night_seat must be set
    if data.best_move_guesses and data.killed_first_night_seat is None:
        raise HTTPException(
            status_code=400,
            detail="best_move_guesses requires killed_first_night_seat to be set",
        )

    # Save basic result
    game.winning_team = data.winning_team.value
    game.killed_first_night_seat = data.killed_first_night_seat

    # Build role map from input for bonus calc
    seat_roles = {s.seat_number: s.role for s in data.seats}

    for seat_input in data.seats:
        seat = existing_seats[seat_input.seat_number]
        seat.role = seat_input.role.value
        seat.extra_points = seat_input.extra_points

    # Calculate and add best move bonus to killed player
    if data.killed_first_night_seat is not None and data.best_move_guesses:
        bonus = calc_best_move_bonus(data.best_move_guesses, seat_roles)
        killed_seat = existing_seats[data.killed_first_night_seat]
        killed_seat.extra_points = round(killed_seat.extra_points + bonus, 1)

    # Save best move guesses (replace existing)
    for old_guess in list(game.best_move_guesses):
        db.delete(old_guess)
    db.flush()
    for guess_sn in data.best_move_guesses:
        game.best_move_guesses.append(
            BestMoveGuess(game_id=game.id, guessed_seat_number=guess_sn)
        )

    db.commit()
    db.refresh(game)
    return game
