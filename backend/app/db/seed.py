"""Seed script: real tournament data — 10 players, 25 games with preassigned seating."""

from app.db.session import SessionLocal
from app.models.tournament import Tournament
from app.models.participant import Participant
from app.models.game import Game
from app.models.game_seat import GameSeat
from app.models.best_move import BestMoveGuess  # noqa: F401

# userId -> display_name mapping (stable participant IDs derived from order)
PLAYERS = [
    ("038273a4-b78b-479b-9c42-d01590fda690", "Логика"),
    ("e8941b45-9e50-4249-adde-f00998ecf582", "Sugar"),
    ("2b3cf5f0-cc37-418c-bb0a-9f866ead2148", "Крис"),
    ("24db657b-3fab-4bb7-8b08-d87acb22b702", "Кукла"),
    ("598cf2f1-7136-448e-abbd-fa5e235a0b8f", "Певица"),
    ("55c32abb-01cd-4b5f-9c7d-dea1d2c84db1", "Bandera"),
    ("2e2dd762-c509-4927-9739-79c6f23f7e24", "Шершень"),
    ("3d9c8d21-35ce-45df-a7ee-3ac147b4e61a", "Космiчна"),
    ("48901c62-45ce-4ca9-a550-8e1540f117a1", "f5"),
    ("27dcb0db-65cb-4a50-9801-de9c0e910e94", "filister"),
]

# Map source userId -> our participant_id (1-based)
UID_TO_PID = {uid: i + 1 for i, (uid, _) in enumerate(PLAYERS)}

# fmt: off
# Each game: list of userIds in seat order (seat 1..10)
GAMES_SEATING = {
    1: ["038273a4-b78b-479b-9c42-d01590fda690","e8941b45-9e50-4249-adde-f00998ecf582","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","24db657b-3fab-4bb7-8b08-d87acb22b702","598cf2f1-7136-448e-abbd-fa5e235a0b8f","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","2e2dd762-c509-4927-9739-79c6f23f7e24","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","48901c62-45ce-4ca9-a550-8e1540f117a1","27dcb0db-65cb-4a50-9801-de9c0e910e94"],
    2: ["24db657b-3fab-4bb7-8b08-d87acb22b702","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","598cf2f1-7136-448e-abbd-fa5e235a0b8f","27dcb0db-65cb-4a50-9801-de9c0e910e94","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","038273a4-b78b-479b-9c42-d01590fda690","e8941b45-9e50-4249-adde-f00998ecf582","2e2dd762-c509-4927-9739-79c6f23f7e24","48901c62-45ce-4ca9-a550-8e1540f117a1"],
    3: ["48901c62-45ce-4ca9-a550-8e1540f117a1","2e2dd762-c509-4927-9739-79c6f23f7e24","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","598cf2f1-7136-448e-abbd-fa5e235a0b8f","e8941b45-9e50-4249-adde-f00998ecf582","038273a4-b78b-479b-9c42-d01590fda690","24db657b-3fab-4bb7-8b08-d87acb22b702","27dcb0db-65cb-4a50-9801-de9c0e910e94"],
    4: ["e8941b45-9e50-4249-adde-f00998ecf582","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","48901c62-45ce-4ca9-a550-8e1540f117a1","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","27dcb0db-65cb-4a50-9801-de9c0e910e94","2e2dd762-c509-4927-9739-79c6f23f7e24","038273a4-b78b-479b-9c42-d01590fda690","24db657b-3fab-4bb7-8b08-d87acb22b702","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","598cf2f1-7136-448e-abbd-fa5e235a0b8f"],
    5: ["27dcb0db-65cb-4a50-9801-de9c0e910e94","598cf2f1-7136-448e-abbd-fa5e235a0b8f","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","48901c62-45ce-4ca9-a550-8e1540f117a1","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","e8941b45-9e50-4249-adde-f00998ecf582","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","2e2dd762-c509-4927-9739-79c6f23f7e24","038273a4-b78b-479b-9c42-d01590fda690","24db657b-3fab-4bb7-8b08-d87acb22b702"],
    6: ["2e2dd762-c509-4927-9739-79c6f23f7e24","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","24db657b-3fab-4bb7-8b08-d87acb22b702","038273a4-b78b-479b-9c42-d01590fda690","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","27dcb0db-65cb-4a50-9801-de9c0e910e94","48901c62-45ce-4ca9-a550-8e1540f117a1","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","e8941b45-9e50-4249-adde-f00998ecf582","598cf2f1-7136-448e-abbd-fa5e235a0b8f"],
    7: ["2b3cf5f0-cc37-418c-bb0a-9f866ead2148","27dcb0db-65cb-4a50-9801-de9c0e910e94","e8941b45-9e50-4249-adde-f00998ecf582","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","24db657b-3fab-4bb7-8b08-d87acb22b702","48901c62-45ce-4ca9-a550-8e1540f117a1","598cf2f1-7136-448e-abbd-fa5e235a0b8f","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","038273a4-b78b-479b-9c42-d01590fda690","2e2dd762-c509-4927-9739-79c6f23f7e24"],
    8: ["598cf2f1-7136-448e-abbd-fa5e235a0b8f","038273a4-b78b-479b-9c42-d01590fda690","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","2e2dd762-c509-4927-9739-79c6f23f7e24","27dcb0db-65cb-4a50-9801-de9c0e910e94","e8941b45-9e50-4249-adde-f00998ecf582","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","48901c62-45ce-4ca9-a550-8e1540f117a1","24db657b-3fab-4bb7-8b08-d87acb22b702"],
    9: ["2e2dd762-c509-4927-9739-79c6f23f7e24","24db657b-3fab-4bb7-8b08-d87acb22b702","e8941b45-9e50-4249-adde-f00998ecf582","598cf2f1-7136-448e-abbd-fa5e235a0b8f","48901c62-45ce-4ca9-a550-8e1540f117a1","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","27dcb0db-65cb-4a50-9801-de9c0e910e94","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","038273a4-b78b-479b-9c42-d01590fda690"],
    10: ["55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","27dcb0db-65cb-4a50-9801-de9c0e910e94","2e2dd762-c509-4927-9739-79c6f23f7e24","24db657b-3fab-4bb7-8b08-d87acb22b702","038273a4-b78b-479b-9c42-d01590fda690","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","e8941b45-9e50-4249-adde-f00998ecf582","598cf2f1-7136-448e-abbd-fa5e235a0b8f","48901c62-45ce-4ca9-a550-8e1540f117a1"],
    11: ["038273a4-b78b-479b-9c42-d01590fda690","27dcb0db-65cb-4a50-9801-de9c0e910e94","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","48901c62-45ce-4ca9-a550-8e1540f117a1","e8941b45-9e50-4249-adde-f00998ecf582","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","598cf2f1-7136-448e-abbd-fa5e235a0b8f","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","24db657b-3fab-4bb7-8b08-d87acb22b702","2e2dd762-c509-4927-9739-79c6f23f7e24"],
    12: ["e8941b45-9e50-4249-adde-f00998ecf582","598cf2f1-7136-448e-abbd-fa5e235a0b8f","2e2dd762-c509-4927-9739-79c6f23f7e24","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","038273a4-b78b-479b-9c42-d01590fda690","48901c62-45ce-4ca9-a550-8e1540f117a1","24db657b-3fab-4bb7-8b08-d87acb22b702","27dcb0db-65cb-4a50-9801-de9c0e910e94","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1"],
    13: ["55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","038273a4-b78b-479b-9c42-d01590fda690","24db657b-3fab-4bb7-8b08-d87acb22b702","e8941b45-9e50-4249-adde-f00998ecf582","598cf2f1-7136-448e-abbd-fa5e235a0b8f","2e2dd762-c509-4927-9739-79c6f23f7e24","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","48901c62-45ce-4ca9-a550-8e1540f117a1","27dcb0db-65cb-4a50-9801-de9c0e910e94","2b3cf5f0-cc37-418c-bb0a-9f866ead2148"],
    14: ["598cf2f1-7136-448e-abbd-fa5e235a0b8f","48901c62-45ce-4ca9-a550-8e1540f117a1","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","e8941b45-9e50-4249-adde-f00998ecf582","27dcb0db-65cb-4a50-9801-de9c0e910e94","2e2dd762-c509-4927-9739-79c6f23f7e24","038273a4-b78b-479b-9c42-d01590fda690","24db657b-3fab-4bb7-8b08-d87acb22b702","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a"],
    15: ["2b3cf5f0-cc37-418c-bb0a-9f866ead2148","24db657b-3fab-4bb7-8b08-d87acb22b702","598cf2f1-7136-448e-abbd-fa5e235a0b8f","e8941b45-9e50-4249-adde-f00998ecf582","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","48901c62-45ce-4ca9-a550-8e1540f117a1","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","2e2dd762-c509-4927-9739-79c6f23f7e24","27dcb0db-65cb-4a50-9801-de9c0e910e94","038273a4-b78b-479b-9c42-d01590fda690"],
    16: ["48901c62-45ce-4ca9-a550-8e1540f117a1","e8941b45-9e50-4249-adde-f00998ecf582","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","2e2dd762-c509-4927-9739-79c6f23f7e24","27dcb0db-65cb-4a50-9801-de9c0e910e94","038273a4-b78b-479b-9c42-d01590fda690","24db657b-3fab-4bb7-8b08-d87acb22b702","598cf2f1-7136-448e-abbd-fa5e235a0b8f","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a"],
    17: ["3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","038273a4-b78b-479b-9c42-d01590fda690","27dcb0db-65cb-4a50-9801-de9c0e910e94","598cf2f1-7136-448e-abbd-fa5e235a0b8f","e8941b45-9e50-4249-adde-f00998ecf582","24db657b-3fab-4bb7-8b08-d87acb22b702","48901c62-45ce-4ca9-a550-8e1540f117a1","2e2dd762-c509-4927-9739-79c6f23f7e24","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1"],
    18: ["27dcb0db-65cb-4a50-9801-de9c0e910e94","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","038273a4-b78b-479b-9c42-d01590fda690","24db657b-3fab-4bb7-8b08-d87acb22b702","48901c62-45ce-4ca9-a550-8e1540f117a1","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","e8941b45-9e50-4249-adde-f00998ecf582","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","598cf2f1-7136-448e-abbd-fa5e235a0b8f","2e2dd762-c509-4927-9739-79c6f23f7e24"],
    19: ["3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","48901c62-45ce-4ca9-a550-8e1540f117a1","27dcb0db-65cb-4a50-9801-de9c0e910e94","038273a4-b78b-479b-9c42-d01590fda690","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","e8941b45-9e50-4249-adde-f00998ecf582","2e2dd762-c509-4927-9739-79c6f23f7e24","598cf2f1-7136-448e-abbd-fa5e235a0b8f","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","24db657b-3fab-4bb7-8b08-d87acb22b702"],
    20: ["24db657b-3fab-4bb7-8b08-d87acb22b702","2e2dd762-c509-4927-9739-79c6f23f7e24","038273a4-b78b-479b-9c42-d01590fda690","27dcb0db-65cb-4a50-9801-de9c0e910e94","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","598cf2f1-7136-448e-abbd-fa5e235a0b8f","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","48901c62-45ce-4ca9-a550-8e1540f117a1","e8941b45-9e50-4249-adde-f00998ecf582"],
    21: ["e8941b45-9e50-4249-adde-f00998ecf582","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","2e2dd762-c509-4927-9739-79c6f23f7e24","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","27dcb0db-65cb-4a50-9801-de9c0e910e94","24db657b-3fab-4bb7-8b08-d87acb22b702","598cf2f1-7136-448e-abbd-fa5e235a0b8f","48901c62-45ce-4ca9-a550-8e1540f117a1","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","038273a4-b78b-479b-9c42-d01590fda690"],
    22: ["3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","48901c62-45ce-4ca9-a550-8e1540f117a1","e8941b45-9e50-4249-adde-f00998ecf582","038273a4-b78b-479b-9c42-d01590fda690","24db657b-3fab-4bb7-8b08-d87acb22b702","598cf2f1-7136-448e-abbd-fa5e235a0b8f","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","27dcb0db-65cb-4a50-9801-de9c0e910e94","2e2dd762-c509-4927-9739-79c6f23f7e24","2b3cf5f0-cc37-418c-bb0a-9f866ead2148"],
    23: ["598cf2f1-7136-448e-abbd-fa5e235a0b8f","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","24db657b-3fab-4bb7-8b08-d87acb22b702","2e2dd762-c509-4927-9739-79c6f23f7e24","038273a4-b78b-479b-9c42-d01590fda690","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","27dcb0db-65cb-4a50-9801-de9c0e910e94","48901c62-45ce-4ca9-a550-8e1540f117a1","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","e8941b45-9e50-4249-adde-f00998ecf582"],
    # NOTE: source data had Космiчна duplicated on seats 5 and 9; seat 9 corrected to Крис (the missing player)
    24: ["48901c62-45ce-4ca9-a550-8e1540f117a1","e8941b45-9e50-4249-adde-f00998ecf582","55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","27dcb0db-65cb-4a50-9801-de9c0e910e94","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a","2e2dd762-c509-4927-9739-79c6f23f7e24","24db657b-3fab-4bb7-8b08-d87acb22b702","038273a4-b78b-479b-9c42-d01590fda690","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","598cf2f1-7136-448e-abbd-fa5e235a0b8f"],
    25: ["55c32abb-01cd-4b5f-9c7d-dea1d2c84db1","2b3cf5f0-cc37-418c-bb0a-9f866ead2148","48901c62-45ce-4ca9-a550-8e1540f117a1","24db657b-3fab-4bb7-8b08-d87acb22b702","2e2dd762-c509-4927-9739-79c6f23f7e24","038273a4-b78b-479b-9c42-d01590fda690","27dcb0db-65cb-4a50-9801-de9c0e910e94","598cf2f1-7136-448e-abbd-fa5e235a0b8f","e8941b45-9e50-4249-adde-f00998ecf582","3d9c8d21-35ce-45df-a7ee-3ac147b4e61a"],
}
# fmt: on


def seed():
    db = SessionLocal()
    try:
        if db.query(Tournament).first():
            print("Database already seeded, skipping.")
            return

        tournament = Tournament(id=1, name="IMAFA Tournament 2026")
        db.add(tournament)
        db.flush()

        for uid, display_name in PLAYERS:
            pid = UID_TO_PID[uid]
            db.add(Participant(id=pid, tournament_id=1, display_name=display_name))
        db.flush()

        for game_number, seat_uids in GAMES_SEATING.items():
            game = Game(
                tournament_id=1,
                round_number=game_number,
                table_number=1,
            )
            db.add(game)
            db.flush()

            for seat_num, uid in enumerate(seat_uids, start=1):
                pid = UID_TO_PID[uid]
                db.add(GameSeat(
                    game_id=game.id,
                    seat_number=seat_num,
                    participant_id=pid,
                ))

        db.commit()
        print(f"Seeded: 1 tournament, {len(PLAYERS)} participants, {len(GAMES_SEATING)} games.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
