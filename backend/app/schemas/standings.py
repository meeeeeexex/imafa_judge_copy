from pydantic import BaseModel


class StandingsEntry(BaseModel):
    participant_id: int
    display_name: str
    games_played: int
    wins: int
    losses: int
    base_points: float
    extra_points: float
    total_points: float
