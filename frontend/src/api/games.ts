import { apiFetch } from './client'
import type { Game, GameResultInput } from '../types/api'

export function getGame(id: number) {
  return apiFetch<Game>(`/games/${id}`)
}

export function submitGameResult(gameId: number, data: GameResultInput) {
  return apiFetch<Game>(`/games/${gameId}/result`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}
