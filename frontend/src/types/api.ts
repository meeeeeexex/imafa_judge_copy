export type Role = 'DON' | 'SHERIFF' | 'MAFIA' | 'CIVILIAN'
export type Team = 'RED' | 'BLACK'

export interface Tournament {
  id: number
  name: string
}

export interface Participant {
  id: number
  tournament_id: number
  display_name: string
}

export interface GameSeat {
  id: number
  seat_number: number
  participant_id: number
  display_name: string | null
  role: Role | null
  extra_points: number
}

export interface Game {
  id: number
  tournament_id: number
  round_number: number
  table_number: number
  winning_team: Team | null
  killed_first_night_seat: number | null
  best_move_guesses: number[]
  seats: GameSeat[]
}

export interface GameSeatInput {
  seat_number: number
  participant_id: number
  role: Role
  extra_points: number
}

export interface GameResultInput {
  winning_team: Team
  seats: GameSeatInput[]
  killed_first_night_seat: number | null
  best_move_guesses: number[]
}

export interface StandingsEntry {
  participant_id: number
  display_name: string
  games_played: number
  wins: number
  losses: number
  base_points: number
  extra_points: number
  total_points: number
}
