from sqlalchemy.orm import Session

from app.core.enums import Role, Team
from app.models.game import Game
from app.models.game_seat import GameSeat
from app.models.participant import Participant
from app.schemas.standings import StandingsEntry
from app.services.scoring import get_base_points, is_winner


def compute_standings(db: Session, tournament_id: int) -> list[StandingsEntry]:
    participants = (
        db.query(Participant)
        .filter(Participant.tournament_id == tournament_id)
        .all()
    )
    participant_map = {p.id: p.display_name for p in participants}

    # Get all completed games for this tournament
    completed_games = (
        db.query(Game)
        .filter(Game.tournament_id == tournament_id, Game.winning_team.isnot(None))
        .all()
    )

    # Accumulate stats per participant
    stats: dict[int, dict] = {
        pid: {
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "base_points": 0.0,
            "extra_points": 0.0,
        }
        for pid in participant_map
    }

    for game in completed_games:
        winning_team = Team(game.winning_team)
        for seat in game.seats:
            if seat.role is None:
                continue
            pid = seat.participant_id
            if pid not in stats:
                continue
            role = Role(seat.role)
            bp = get_base_points(role, winning_team)
            won = is_winner(role, winning_team)

            stats[pid]["games_played"] += 1
            stats[pid]["wins"] += 1 if won else 0
            stats[pid]["losses"] += 0 if won else 1
            stats[pid]["base_points"] += bp
            stats[pid]["extra_points"] += seat.extra_points

    entries = []
    for pid, s in stats.items():
        entries.append(
            StandingsEntry(
                participant_id=pid,
                display_name=participant_map[pid],
                games_played=s["games_played"],
                wins=s["wins"],
                losses=s["losses"],
                base_points=s["base_points"],
                extra_points=round(s["extra_points"], 1),
                total_points=round(s["base_points"] + s["extra_points"], 1),
            )
        )

    # Sort: total desc, extra desc, base desc, name asc
    entries.sort(
        key=lambda e: (-e.total_points, -e.extra_points, -e.base_points, e.display_name)
    )
    return entries
