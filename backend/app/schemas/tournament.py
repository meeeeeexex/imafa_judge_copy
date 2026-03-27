from pydantic import BaseModel


class TournamentRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
