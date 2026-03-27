from pydantic import BaseModel


class ParticipantRead(BaseModel):
    id: int
    tournament_id: int
    display_name: str

    model_config = {"from_attributes": True}
