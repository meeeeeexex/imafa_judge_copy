from app.core.enums import Role, Team
from app.models.game import Game
from app.models.game_seat import GameSeat
from app.services.standings import compute_standings


class TestStandings:
    def test_no_completed_games_returns_zeroes(self, seeded_db):
        standings = compute_standings(seeded_db, tournament_id=1)
        assert len(standings) == 10
        for entry in standings:
            assert entry.games_played == 0
            assert entry.total_points == 0.0

    def test_one_game_black_wins(self, seeded_db):
        # Set up game 1: BLACK wins
        game = seeded_db.get(Game, 1)
        game.winning_team = Team.BLACK.value

        roles = [
            Role.DON, Role.SHERIFF, Role.MAFIA, Role.CIVILIAN, Role.CIVILIAN,
            Role.MAFIA, Role.CIVILIAN, Role.CIVILIAN, Role.CIVILIAN, Role.CIVILIAN,
        ]
        for seat in game.seats:
            seat.role = roles[seat.seat_number - 1].value
            seat.extra_points = 0.0
        seeded_db.commit()

        standings = compute_standings(seeded_db, tournament_id=1)
        assert len(standings) == 10

        # Alice (DON) should have won
        alice = next(e for e in standings if e.display_name == "Alice")
        assert alice.wins == 1
        assert alice.losses == 0
        assert alice.base_points == 2.0
        assert alice.total_points == 2.0

        # Bob (SHERIFF) should have lost
        bob = next(e for e in standings if e.display_name == "Bob")
        assert bob.wins == 0
        assert bob.losses == 1
        assert bob.base_points == 1.0
        assert bob.total_points == 1.0

    def test_extra_points_included(self, seeded_db):
        game = seeded_db.get(Game, 1)
        game.winning_team = Team.RED.value

        for seat in game.seats:
            seat.role = Role.CIVILIAN.value
            seat.extra_points = 0.0
        # Give Alice extra points
        game.seats[0].role = Role.DON.value
        game.seats[0].extra_points = 0.5
        game.seats[1].role = Role.SHERIFF.value
        game.seats[1].extra_points = 0.3
        seeded_db.commit()

        standings = compute_standings(seeded_db, tournament_id=1)

        alice = next(e for e in standings if e.display_name == "Alice")
        # DON loses when RED wins: 1 base + 0.5 extra = 1.5
        assert alice.base_points == 1.0
        assert alice.extra_points == 0.5
        assert alice.total_points == 1.5

        bob = next(e for e in standings if e.display_name == "Bob")
        # SHERIFF wins when RED wins: 2 base + 0.3 extra = 2.3
        assert bob.base_points == 2.0
        assert bob.extra_points == 0.3
        assert bob.total_points == 2.3

    def test_sorting_order(self, seeded_db):
        game = seeded_db.get(Game, 1)
        game.winning_team = Team.BLACK.value

        # Make Alice DON (win, 2bp), give Bob (SHERIFF, loss, 1bp) 1.5 extra
        roles = [
            Role.DON, Role.SHERIFF, Role.MAFIA, Role.CIVILIAN, Role.CIVILIAN,
            Role.MAFIA, Role.CIVILIAN, Role.CIVILIAN, Role.CIVILIAN, Role.CIVILIAN,
        ]
        for seat in game.seats:
            seat.role = roles[seat.seat_number - 1].value
            seat.extra_points = 0.0
        game.seats[1].extra_points = 1.5  # Bob: 1 + 1.5 = 2.5
        game.seats[0].extra_points = 0.0  # Alice: 2 + 0 = 2.0
        seeded_db.commit()

        standings = compute_standings(seeded_db, tournament_id=1)

        # Bob (2.5 total) should be first, then Alice (2.0)
        assert standings[0].display_name == "Bob"
        assert standings[0].total_points == 2.5
        assert standings[1].display_name == "Alice"
        assert standings[1].total_points == 2.0

    def test_multiple_games(self, seeded_db):
        # Add a second game
        game2 = Game(id=2, tournament_id=1, round_number=2, table_number=1)
        seeded_db.add(game2)
        seeded_db.flush()
        for seat_num in range(1, 11):
            seeded_db.add(GameSeat(game_id=2, seat_number=seat_num, participant_id=seat_num))
        seeded_db.commit()

        # Game 1: BLACK wins, Alice=DON
        game1 = seeded_db.get(Game, 1)
        game1.winning_team = Team.BLACK.value
        roles1 = [
            Role.DON, Role.SHERIFF, Role.MAFIA, Role.CIVILIAN, Role.CIVILIAN,
            Role.MAFIA, Role.CIVILIAN, Role.CIVILIAN, Role.CIVILIAN, Role.CIVILIAN,
        ]
        for seat in game1.seats:
            seat.role = roles1[seat.seat_number - 1].value
            seat.extra_points = 0.0

        # Game 2: RED wins, Alice=CIVILIAN (wins)
        game2 = seeded_db.get(Game, 2)
        game2.winning_team = Team.RED.value
        roles2 = [
            Role.CIVILIAN, Role.DON, Role.SHERIFF, Role.MAFIA, Role.MAFIA,
            Role.CIVILIAN, Role.CIVILIAN, Role.CIVILIAN, Role.CIVILIAN, Role.CIVILIAN,
        ]
        for seat in game2.seats:
            seat.role = roles2[seat.seat_number - 1].value
            seat.extra_points = 0.0
        seeded_db.commit()

        standings = compute_standings(seeded_db, tournament_id=1)
        alice = next(e for e in standings if e.display_name == "Alice")
        # Game 1: DON + BLACK win = 2bp. Game 2: CIVILIAN + RED win = 2bp.
        assert alice.games_played == 2
        assert alice.wins == 2
        assert alice.base_points == 4.0
        assert alice.total_points == 4.0
