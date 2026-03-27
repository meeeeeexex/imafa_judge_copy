from pydantic import BaseModel, field_validator

from app.core.enums import Role, Team


class GameSeatRead(BaseModel):
    id: int
    seat_number: int
    participant_id: int
    display_name: str | None = None
    role: Role | None = None
    extra_points: float

    model_config = {"from_attributes": True}


class GameRead(BaseModel):
    id: int
    tournament_id: int
    round_number: int
    table_number: int
    winning_team: Team | None = None
    killed_first_night_seat: int | None = None
    best_move_guesses: list[int] = []
    seats: list[GameSeatRead] = []

    model_config = {"from_attributes": True}


class GameSeatInput(BaseModel):
    seat_number: int
    participant_id: int
    role: Role
    extra_points: float = 0.0


class GameResultInput(BaseModel):
    winning_team: Team
    seats: list[GameSeatInput]
    killed_first_night_seat: int | None = None
    best_move_guesses: list[int] = []

    @field_validator("best_move_guesses")
    @classmethod
    def validate_best_move_guesses(cls, v: list[int]) -> list[int]:
        if len(v) > 3:
            raise ValueError("Best move allows at most 3 guesses")
        if len(v) != len(set(v)):
            raise ValueError("Best move guesses must be unique seat numbers")
        return v
