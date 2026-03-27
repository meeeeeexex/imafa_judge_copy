from app.core.enums import Role, Team
from app.services.scoring import calc_best_move_bonus, get_base_points, get_team_for_role, is_winner


class TestGetTeamForRole:
    def test_don_is_black(self):
        assert get_team_for_role(Role.DON) == Team.BLACK

    def test_mafia_is_black(self):
        assert get_team_for_role(Role.MAFIA) == Team.BLACK

    def test_sheriff_is_red(self):
        assert get_team_for_role(Role.SHERIFF) == Team.RED

    def test_civilian_is_red(self):
        assert get_team_for_role(Role.CIVILIAN) == Team.RED


class TestGetBasePoints:
    def test_don_wins_when_black_wins(self):
        assert get_base_points(Role.DON, Team.BLACK) == 2.0

    def test_don_loses_when_red_wins(self):
        assert get_base_points(Role.DON, Team.RED) == 1.0

    def test_sheriff_wins_when_red_wins(self):
        assert get_base_points(Role.SHERIFF, Team.RED) == 2.0

    def test_sheriff_loses_when_black_wins(self):
        assert get_base_points(Role.SHERIFF, Team.BLACK) == 1.0

    def test_mafia_wins_when_black_wins(self):
        assert get_base_points(Role.MAFIA, Team.BLACK) == 2.0

    def test_civilian_wins_when_red_wins(self):
        assert get_base_points(Role.CIVILIAN, Team.RED) == 2.0

    def test_civilian_loses_when_black_wins(self):
        assert get_base_points(Role.CIVILIAN, Team.BLACK) == 1.0


class TestIsWinner:
    def test_don_wins_black(self):
        assert is_winner(Role.DON, Team.BLACK) is True

    def test_don_loses_red(self):
        assert is_winner(Role.DON, Team.RED) is False

    def test_civilian_wins_red(self):
        assert is_winner(Role.CIVILIAN, Team.RED) is True

    def test_civilian_loses_black(self):
        assert is_winner(Role.CIVILIAN, Team.BLACK) is False


class TestBestMoveBonus:
    # Standard 10-seat game: seats 1=DON, 2=SHERIFF, 3=MAFIA, 4=MAFIA, 5-10=CIVILIAN
    SEAT_ROLES = {
        1: Role.DON, 2: Role.SHERIFF, 3: Role.MAFIA, 4: Role.MAFIA,
        5: Role.CIVILIAN, 6: Role.CIVILIAN, 7: Role.CIVILIAN,
        8: Role.CIVILIAN, 9: Role.CIVILIAN, 10: Role.CIVILIAN,
    }

    def test_zero_correct(self):
        assert calc_best_move_bonus([5, 6, 7], self.SEAT_ROLES) == 0.0

    def test_one_correct(self):
        # Seat 1 is DON (black team)
        assert calc_best_move_bonus([1, 5, 6], self.SEAT_ROLES) == 0.2

    def test_two_correct(self):
        # Seat 1=DON, seat 3=MAFIA
        assert calc_best_move_bonus([1, 3, 5], self.SEAT_ROLES) == 0.5

    def test_three_correct(self):
        # Seat 1=DON, seat 3=MAFIA, seat 4=MAFIA
        assert calc_best_move_bonus([1, 3, 4], self.SEAT_ROLES) == 0.8

    def test_empty_guesses(self):
        assert calc_best_move_bonus([], self.SEAT_ROLES) == 0.0

    def test_one_guess_correct(self):
        assert calc_best_move_bonus([3], self.SEAT_ROLES) == 0.2

    def test_two_guesses_both_correct(self):
        assert calc_best_move_bonus([1, 4], self.SEAT_ROLES) == 0.5
