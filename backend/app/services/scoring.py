from app.core.enums import BLACK_ROLES, RED_ROLES, Role, Team

WIN_POINTS = 2.0
LOSS_POINTS = 1.0
BEST_MOVE_POINTS = {0: 0.0, 1: 0.2, 2: 0.5, 3: 0.8}


def get_team_for_role(role: Role) -> Team:
    if role in RED_ROLES:
        return Team.RED
    return Team.BLACK


def get_base_points(role: Role, winning_team: Team) -> float:
    player_team = get_team_for_role(role)
    if player_team == winning_team:
        return WIN_POINTS
    return LOSS_POINTS


def is_winner(role: Role, winning_team: Team) -> bool:
    return get_team_for_role(role) == winning_team


def calc_best_move_bonus(
    guessed_seat_numbers: list[int],
    seat_roles: dict[int, Role],
) -> float:
    """Calculate bonus for the killed-first-night player's best move.

    guessed_seat_numbers: seat numbers the player named (up to 3)
    seat_roles: mapping of seat_number -> Role for all seats in the game
    Returns bonus points: 0 hits=0.0, 1=0.2, 2=0.5, 3=0.8
    """
    hits = sum(
        1 for sn in guessed_seat_numbers
        if sn in seat_roles and seat_roles[sn] in BLACK_ROLES
    )
    return BEST_MOVE_POINTS.get(hits, 0.0)
