import { apiFetch } from './client'
import type { Game, Participant, StandingsEntry, Tournament } from '../types/api'

export function getTournament(id: number) {
  return apiFetch<Tournament>(`/tournaments/${id}`)
}

export function getParticipants(tournamentId: number) {
  return apiFetch<Participant[]>(`/tournaments/${tournamentId}/participants`)
}

export function getGames(tournamentId: number) {
  return apiFetch<Game[]>(`/tournaments/${tournamentId}/games`)
}

export function getStandings(tournamentId: number) {
  return apiFetch<StandingsEntry[]>(`/tournaments/${tournamentId}/standings`)
}
