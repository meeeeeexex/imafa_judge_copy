# CLAUDE.md — IMAFA Judge

## Project mission

MVP tournament management system for Mafia games. Operators enter game results, the system calculates standings automatically.

The project is intentionally simple:
- participant list is static (seeded)
- player seating is static (seeded)
- the main task is entering results for preconfigured games
- standings are computed dynamically from results

Do not overengineer. Prefer the simplest implementation. Do not add features unless explicitly requested.

---

## Technical stack

### Backend
- **FastAPI** 0.115.6 — web framework
- **SQLAlchemy** 2.0.36 — ORM (mapped_column, DeclarativeBase)
- **Pydantic** 2.10.4 — request/response validation
- **Alembic** 1.14.1 — database migrations
- **SQLite** — single file `backend/tournament.db`
- **Uvicorn** 0.34.0 — ASGI server
- **Pytest** 8.3.4 — testing

### Frontend
- **Vue 3** 3.5.30 — Composition API with `<script setup lang="ts">`
- **Vite** 8.0.1 — build tool
- **TypeScript** 5.9.3 — strict mode enabled
- **Tailwind CSS** 4.2.2 — via `@tailwindcss/vite` plugin
- **Vue Router** 4.6.4 — SPA routing

### Development
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:5173` (Vite dev server)
- CORS is open (`allow_origins=["*"]`)
- No Docker, no `.env` files — simple local setup
- Python venv at `backend/venv/`

---

## Project structure

```text
imafa_judge_copy/
├── CLAUDE.md
├── backend/
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── tournament.db              # SQLite database file
│   ├── venv/
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── 2e4e3b8b3ba6_initial_tables.py
│   │       └── 9ba6fa261a9e_add_best_move_feature.py
│   └── app/
│       ├── main.py                # FastAPI app entry point
│       ├── api/routes/
│       │   ├── health.py          # GET /health
│       │   ├── tournaments.py     # GET /tournaments/{id}, /participants, /games
│       │   ├── games.py           # GET /games/{id}, PUT /games/{id}/result
│       │   └── standings.py       # GET /tournaments/{id}/standings
│       ├── core/
│       │   ├── config.py          # DATABASE_URL, BASE_DIR
│       │   └── enums.py           # Role, Team, RED_ROLES, BLACK_ROLES
│       ├── db/
│       │   ├── base.py            # DeclarativeBase
│       │   ├── session.py         # engine, SessionLocal, get_db()
│       │   └── seed.py            # Seeds 1 tournament, 10 players, 25 games
│       ├── models/
│       │   ├── tournament.py      # Tournament model
│       │   ├── participant.py     # Participant model
│       │   ├── game.py            # Game model
│       │   ├── game_seat.py       # GameSeat model
│       │   └── best_move.py       # BestMoveGuess model
│       ├── schemas/
│       │   ├── tournament.py      # TournamentRead
│       │   ├── participant.py     # ParticipantRead
│       │   ├── game.py            # GameRead, GameSeatRead, GameResultInput, GameSeatInput
│       │   └── standings.py       # StandingsEntry
│       ├── services/
│       │   ├── scoring.py         # get_base_points, is_winner, calc_best_move_bonus
│       │   ├── game_results.py    # validate_and_save_result
│       │   └── standings.py       # compute_standings
│       └── tests/
│           ├── conftest.py        # db, seeded_db fixtures (in-memory SQLite)
│           ├── test_scoring.py    # 22 tests: roles, points, winner, best move
│           └── test_standings.py  # 5 tests: empty, single game, extras, sorting, multi-game
└── frontend/
    ├── index.html                 # Google Fonts (Inter, Outfit), body dark classes
    ├── package.json
    ├── vite.config.ts             # vue() + tailwindcss() plugins
    ├── tsconfig.json
    ├── tsconfig.app.json          # strict, noUnusedLocals, noUnusedParameters
    ├── tsconfig.node.json
    ├── public/
    │   ├── favicon.svg            # Terminal-style "$_" icon
    │   └── icons.svg              # Social media icon sprites (unused)
    └── src/
        ├── main.ts                # createApp, router, style.css import
        ├── router.ts              # 5 routes, "/" redirects to /tournament/1/standings
        ├── style.css              # @import "tailwindcss", @theme block, scrollbar, selection
        ├── App.vue                # Sticky frosted-glass nav, max-w-5xl container
        ├── api/
        │   ├── client.ts          # apiFetch<T>() — generic fetch wrapper, BASE_URL=localhost:8000
        │   ├── tournaments.ts     # getTournament, getParticipants, getGames, getStandings
        │   └── games.ts           # getGame, submitGameResult
        ├── types/
        │   └── api.ts             # Role, Team, Tournament, Participant, Game, GameSeat, StandingsEntry, GameResultInput, GameSeatInput
        ├── views/
        │   ├── StandingsView.vue  # Leaderboard table with medal ranks (gold/silver/bronze)
        │   ├── GamesView.vue      # Games table with team/status pill badges
        │   ├── TournamentView.vue # Tournament info card + participants table
        │   └── GameEditView.vue   # Full game result form: team, roles, extras, best move
        ├── components/            # Empty — all UI is in views
        └── assets/                # hero.png, vite.svg (unused)
```

---

## Domain model

### Tournament
| Field | Type | Notes |
|-------|------|-------|
| id | int | primary key |
| name | str(200) | |

Relationships: participants, games

### Participant
| Field | Type | Notes |
|-------|------|-------|
| id | int | primary key |
| tournament_id | int | FK → tournaments.id |
| display_name | str(200) | |

### Game
| Field | Type | Notes |
|-------|------|-------|
| id | int | primary key |
| tournament_id | int | FK → tournaments.id |
| round_number | int | |
| table_number | int | |
| winning_team | str(10) | nullable, "RED" or "BLACK" |
| killed_first_night_seat | int | nullable |

Relationships: seats (GameSeat), best_move_guesses (BestMoveGuess, cascade delete)

### GameSeat
| Field | Type | Notes |
|-------|------|-------|
| id | int | primary key |
| game_id | int | FK → games.id |
| seat_number | int | |
| participant_id | int | FK → participants.id |
| role | str(10) | nullable, one of Role enum |
| extra_points | float | default 0.0 |

Constraints: UNIQUE(game_id, seat_number), UNIQUE(game_id, participant_id)

### BestMoveGuess
| Field | Type | Notes |
|-------|------|-------|
| id | int | primary key |
| game_id | int | FK → games.id |
| guessed_seat_number | int | |

Constraint: UNIQUE(game_id, guessed_seat_number)

---

## Enums

```python
class Role(str, enum.Enum):
    DON = "DON"
    SHERIFF = "SHERIFF"
    MAFIA = "MAFIA"
    CIVILIAN = "CIVILIAN"

class Team(str, enum.Enum):
    RED = "RED"
    BLACK = "BLACK"

RED_ROLES = {Role.SHERIFF, Role.CIVILIAN}
BLACK_ROLES = {Role.DON, Role.MAFIA}
```

---

## Business rules

### Scoring
- Win = 2.0 base points (player's team matches winning_team)
- Loss = 1.0 base point
- total_points = base_points + extra_points

### Best move bonus
When a player is killed on the first night, they can guess up to 3 black-team members:
- 0 correct guesses → 0.0 bonus
- 1 correct → 0.2
- 2 correct → 0.5
- 3 correct → 0.8

The bonus is added to the killed player's extra_points.

### Result validation (game_results.py)
A game result submission must satisfy:
- All submitted seat numbers match existing seating
- All participant IDs match assigned seats
- killed_first_night_seat must be a valid seat number (if provided)
- best_move_guesses must be valid seat numbers
- best_move_guesses requires killed_first_night_seat to be set
- Best move: max 3 guesses, must be unique seat numbers

### Standings sorting
1. total_points descending
2. extra_points descending
3. base_points descending
4. display_name ascending

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check → `{"status": "ok"}` |
| GET | `/tournaments/{id}` | Tournament details |
| GET | `/tournaments/{id}/participants` | List participants (ordered by id) |
| GET | `/tournaments/{id}/games` | List games with seats (ordered by round, table) |
| GET | `/tournaments/{id}/standings` | Computed standings (dynamically calculated) |
| GET | `/games/{id}` | Single game with seats and best_move_guesses |
| PUT | `/games/{id}/result` | Submit/update game result |

### PUT /games/{id}/result — request body
```json
{
  "winning_team": "RED",
  "killed_first_night_seat": 3,
  "best_move_guesses": [5, 7],
  "seats": [
    {
      "seat_number": 1,
      "participant_id": 1,
      "role": "SHERIFF",
      "extra_points": 0.5
    }
  ]
}
```

### PUT /games/{id}/result — response
Returns full GameRead with updated seats, winning_team, killed_first_night_seat, best_move_guesses[].

---

## Seed data

`backend/app/db/seed.py` populates the database with real tournament data:
- 1 tournament: "IMAFA Tournament"
- 10 participants: Логика, Sugar, Крис, Кукла, Певица, Bandera, Шершень, Космiчна, f5, filister
- 25 games with predefined seating (10 seats per game)
- Seating maps UUIDs to participant IDs via UID_TO_PID dictionary

Run: `python -c "from app.db.seed import seed; seed()"`

---

## Alembic migrations

Two migrations in `backend/alembic/versions/`:

1. **2e4e3b8b3ba6** — `initial_tables` (2026-03-27)
   - Creates: tournaments, participants, games, game_seats

2. **9ba6fa261a9e** — `add_best_move_feature` (2026-03-27)
   - Creates: best_move_guesses table
   - Adds: killed_first_night_seat column to games

Run migrations: `cd backend && alembic upgrade head`

---

## Frontend design system

### Tailwind CSS v4 theme (style.css `@theme` block)

| Token | Value | Tailwind class | Usage |
|-------|-------|---------------|-------|
| --font-sans | Inter | `font-sans` | Body text |
| --font-display | Outfit | `font-display` | Headings (text-4xl font-bold) |
| --color-surface | #1E293B | `bg-surface` | Card backgrounds |
| --color-accent | #22C55E | `text-accent`, `bg-accent` | Wins, CTAs, active nav |
| --color-danger | #EF4444 | `text-danger` | Losses, errors |
| --color-info | #06B6D4 | `text-info` | Links, extra points, info |
| --color-warning | #EAB308 | `text-warning` | Pending badges, seat numbers |
| --color-muted | #94A3B8 | `text-muted` | Muted text |

### Design patterns
- **Page background**: `bg-slate-950` (#020617)
- **Nav**: Sticky, frosted glass (`bg-slate-950/80 backdrop-blur-lg`)
- **Brand**: Green "IJ" square + "IMAFA Judge" in display font
- **Tables**: Rounded card container (`overflow-hidden rounded-xl border border-slate-800`)
- **Table headers**: `bg-slate-800/50`, uppercase, tracking-wider, text-sm
- **Table rows**: `divide-y divide-slate-800`, `hover:bg-slate-800/30`
- **Pill badges**: `rounded-full px-3 py-1 text-sm font-semibold ring-1 ring-inset`
- **Form controls**: `rounded-lg border-slate-700 bg-slate-900 focus:border-accent focus:ring-1 focus:ring-accent`
- **Primary button**: `bg-accent text-slate-950 hover:bg-green-400 hover:shadow-lg`
- **Ghost button**: `border border-slate-700 text-slate-400`
- **Error banner**: `border-red-500/30 bg-red-500/5 text-red-400`
- **Success banner**: `border-accent/30 bg-accent/5 text-accent`
- **Loading state**: SVG spinner with `animate-spin` + text
- **Base font size**: 18px
- **Max content width**: `max-w-5xl` (1024px)

### Nav link order
Standings → Games → Tournament (Standings is default page, `/` redirects to `/tournament/1/standings`)

---

## Frontend routing

| Path | View | Description |
|------|------|-------------|
| `/` | — | Redirects to `/tournament/1/standings` |
| `/tournament/:id` | TournamentView | Tournament info + participants table |
| `/tournament/:id/games` | GamesView | All games with status badges |
| `/game/:id/edit` | GameEditView | Game result form |
| `/tournament/:id/standings` | StandingsView | Leaderboard with medal ranks |

---

## Frontend views detail

### StandingsView (main page)
- Fetches `getStandings(tournamentId)`
- Leaderboard table: rank (medal badges for top 3: gold/silver/bronze), player, GP, W, L, base, extra, total
- Top 3 rows get `bg-accent/5` highlight
- Wins in green, losses in red, extra in cyan, total in bold green

### GamesView
- Fetches `getGames(tournamentId)`
- Table: ID, round, table, winner (RED=red pill / BLACK=purple pill), status (Complete=green / Pending=yellow), edit link
- "Edit Result" links to `/game/{id}/edit`

### GameEditView (most complex)
- Fetches `getGame(gameId)`
- Sections in card layout:
  1. **Winning Team** — select dropdown + team badge
  2. **Seats Table** — 10 rows: seat number (yellow badge), player name, role select, extra points input
  3. **Best Move** — killed-first-night select, 3 guess selects, real-time bonus display
  4. **Actions** — Save (green filled) + Back (ghost) buttons
  5. **Messages** — error/success tinted banners
- `canSubmit` computed: requires winningTeam + all roles filled
- `bestMoveBonus` computed: counts correct black-role guesses → maps to bonus points
- On save: calls `submitGameResult()`, refreshes seatExtras from response

### TournamentView
- Fetches `getTournament(id)` + `getParticipants(id)` in parallel
- Card with tournament name + participant count
- Simple participants table: #, name

---

## Frontend API client

`src/api/client.ts` — generic `apiFetch<T>(path, options?)`:
- Base URL: `http://localhost:8000`
- Sets `Content-Type: application/json`
- Throws `Error("API error {status}: {body}")` on non-ok response

Functions:
- `getTournament(id)` → `GET /tournaments/{id}`
- `getParticipants(tournamentId)` → `GET /tournaments/{id}/participants`
- `getGames(tournamentId)` → `GET /tournaments/{id}/games`
- `getStandings(tournamentId)` → `GET /tournaments/{id}/standings`
- `getGame(id)` → `GET /games/{id}`
- `submitGameResult(gameId, data)` → `PUT /games/{gameId}/result`

---

## Backend service layer

### scoring.py
- `get_team_for_role(role) → Team` — maps Role to RED/BLACK
- `get_base_points(role, winning_team) → float` — 2.0 if same team, 1.0 otherwise
- `is_winner(role, winning_team) → bool`
- `calc_best_move_bonus(guessed_seats, seat_roles) → float` — counts hits against BLACK_ROLES

### game_results.py
- `validate_and_save_result(db, game, data) → Game` — validates seats, participants, saves roles/extras, calculates and adds best move bonus to killed player, replaces best_move_guesses

### standings.py
- `compute_standings(db, tournament_id) → list[StandingsEntry]` — aggregates across all completed games, sorts by total→extra→base→name

---

## Testing

Run: `cd backend && python -m pytest app/tests/ -v`

### test_scoring.py (22 tests)
- TestGetTeamForRole — DON→BLACK, SHERIFF→RED, MAFIA→BLACK, CIVILIAN→RED
- TestGetBasePoints — win/loss for each role + both teams
- TestIsWinner — 4 combinations
- TestBestMoveBonus — 0 guesses, empty, 1/2/3 hits, mixed guesses

### test_standings.py (5 tests)
- No completed games → all zeros
- Single BLACK win → correct points distribution
- Extra points included in total
- Sorting order verified
- Multiple games accumulation

Fixtures: in-memory SQLite with `db` and `seeded_db` (1 tournament, 10 participants, 1 game, 10 seats).

---

## How to run

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -c "from app.db.seed import seed; seed()"
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Tests
```bash
cd backend
python -m pytest app/tests/ -v
```

### Build frontend
```bash
cd frontend
npm run build    # runs vue-tsc -b && vite build
```

---

## Architecture principles

1. Simple monolith — backend serves API, frontend is a separate SPA
2. No premature abstractions — direct, readable code
3. Business rules centralized in `services/` and tested
4. Persist only what is necessary — standings computed dynamically
5. Static data (participants, seating) seeded from `seed.py`
6. Optimize for delivery speed and clarity, not flexibility

---

## What NOT to build

Do not add unless explicitly requested:
- authentication/authorization
- multi-tenant support
- audit log
- live updates/websockets
- complex admin panel
- granular permissions
- event sourcing / message brokers / background workers
- caching layer
- plugin architecture
- generic form engines
- advanced filtering/reporting
- drag-and-drop tournament editor

---

## Coding conventions

### Backend
- Use `Role` and `Team` enums everywhere — no raw strings
- Use `mapped_column` (SQLAlchemy 2.0 style)
- Use `model_config = {"from_attributes": True}` for Pydantic schemas
- Keep route handlers thin — delegate to services
- Validate input in service layer before persisting
- `get_db()` as FastAPI dependency for sessions

### Frontend
- Composition API with `<script setup lang="ts">` — no Options API
- No Pinia/Vuex — state is local to each view via `ref()`/`computed()`
- No component library — Tailwind utility classes only
- No `<style scoped>` blocks — all styling via Tailwind classes in templates
- `active-class` prop on router-link for active nav state
- Conditional classes via Vue `:class` bindings

### General
- Prefer explicit code over abstraction
- Keep functions short
- Do not create needless layers or helpers for one-time operations
- Do not add comments, docstrings, or type annotations to code you didn't change
