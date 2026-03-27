<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getGame, submitGameResult } from '../api/games'
import type { Game, Role, Team, GameResultInput } from '../types/api'

const ROLES: Role[] = ['DON', 'SHERIFF', 'MAFIA', 'CIVILIAN']
const BLACK_ROLES: Role[] = ['DON', 'MAFIA']
const BEST_MOVE_POINTS: Record<number, number> = { 0: 0, 1: 0.2, 2: 0.5, 3: 0.8 }

const route = useRoute()
const router = useRouter()
const game = ref<Game | null>(null)
const winningTeam = ref<Team | ''>('')
const seatRoles = ref<(Role | '')[]>([])
const seatExtras = ref<number[]>([])
const killedSeat = ref<number | ''>('')
const bestMoveGuesses = ref<(number | '')[]>(['', '', ''])
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const success = ref('')

onMounted(async () => {
  const id = Number(route.params.id)
  game.value = await getGame(id)
  winningTeam.value = game.value.winning_team ?? ''
  seatRoles.value = game.value.seats.map(s => s.role ?? '')
  seatExtras.value = game.value.seats.map(s => s.extra_points)
  killedSeat.value = game.value.killed_first_night_seat ?? ''
  const guesses = game.value.best_move_guesses ?? []
  bestMoveGuesses.value = [guesses[0] ?? '', guesses[1] ?? '', guesses[2] ?? '']
  loading.value = false
})

const canSubmit = computed(() => {
  if (!winningTeam.value) return false
  return seatRoles.value.every(r => r !== '')
})

const bestMoveBonus = computed(() => {
  if (!killedSeat.value || !game.value) return 0
  const guesses = bestMoveGuesses.value.filter(g => g !== '') as number[]
  if (guesses.length === 0) return 0
  const hits = guesses.filter((seatNum) => {
    const idx = game.value!.seats.findIndex(s => s.seat_number === seatNum)
    if (idx === -1) return false
    const role = seatRoles.value[idx]
    return role !== '' && BLACK_ROLES.includes(role as Role)
  }).length
  return BEST_MOVE_POINTS[hits] ?? 0
})

async function submit() {
  if (!game.value || !canSubmit.value) return
  saving.value = true
  error.value = ''
  success.value = ''

  const guesses = bestMoveGuesses.value.filter(g => g !== '') as number[]

  const data: GameResultInput = {
    winning_team: winningTeam.value as Team,
    killed_first_night_seat: killedSeat.value !== '' ? killedSeat.value as number : null,
    best_move_guesses: guesses,
    seats: game.value.seats.map((s, i) => ({
      seat_number: s.seat_number,
      participant_id: s.participant_id,
      role: seatRoles.value[i] as Role,
      extra_points: seatExtras.value[i] ?? 0,
    })),
  }

  try {
    game.value = await submitGameResult(game.value.id, data)
    seatExtras.value = game.value.seats.map(s => s.extra_points)
    success.value = 'Result saved!'
  } catch (e: any) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div v-if="loading" class="flex items-center gap-3 py-16 text-slate-400">
    <svg class="h-6 w-6 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
    <span>Loading game data...</span>
  </div>

  <div v-else-if="game" class="space-y-4 sm:space-y-6">
    <!-- Header -->
    <div>
      <h1 class="font-display text-3xl font-bold tracking-tight text-slate-50 sm:text-4xl">Game #{{ game.id }}</h1>
      <p class="mt-1 text-slate-400">Round {{ game.round_number }} &middot; Table {{ game.table_number }}</p>
    </div>

    <!-- Winning Team -->
    <div class="rounded-xl border border-slate-800 bg-surface p-4 sm:p-6">
      <label class="mb-3 block text-sm font-semibold uppercase tracking-wider text-slate-400">Winning Team</label>
      <div class="flex items-center gap-4">
        <select
          v-model="winningTeam"
          class="min-h-[44px] rounded-lg border border-slate-700 bg-slate-900 px-4 py-2.5 text-slate-200 transition-colors focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent"
        >
          <option value="">-- Select --</option>
          <option value="RED">RED</option>
          <option value="BLACK">BLACK</option>
        </select>
        <span
          v-if="winningTeam"
          class="inline-flex items-center rounded-full px-3.5 py-1 text-sm font-bold ring-1 ring-inset"
          :class="winningTeam === 'RED'
            ? 'bg-red-500/10 text-red-400 ring-red-500/20'
            : 'bg-purple-500/10 text-purple-400 ring-purple-500/20'"
        >
          {{ winningTeam }}
        </span>
      </div>
    </div>

    <!-- Seats: Desktop Table -->
    <div class="hidden sm:block overflow-hidden rounded-xl border border-slate-800">
      <table class="w-full">
        <thead>
          <tr class="border-b border-slate-700 bg-slate-800/50">
            <th class="px-5 py-3.5 text-center text-sm font-semibold uppercase tracking-wider text-slate-400">Seat</th>
            <th class="px-5 py-3.5 text-left text-sm font-semibold uppercase tracking-wider text-slate-400">Player</th>
            <th class="px-5 py-3.5 text-left text-sm font-semibold uppercase tracking-wider text-slate-400">Role</th>
            <th class="px-5 py-3.5 text-left text-sm font-semibold uppercase tracking-wider text-slate-400">Extra Pts</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <tr v-for="(seat, i) in game.seats" :key="seat.id" class="transition-colors hover:bg-slate-800/30">
            <td class="px-5 py-3.5 text-center">
              <span class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-warning/10 text-sm font-bold text-warning">
                {{ seat.seat_number }}
              </span>
            </td>
            <td class="px-5 py-3.5 font-medium text-slate-200">{{ seat.display_name }}</td>
            <td class="px-5 py-3.5">
              <select
                v-model="seatRoles[i]"
                class="w-full rounded-lg border border-slate-700 bg-slate-900 px-4 py-2.5 text-slate-200 transition-colors focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent"
              >
                <option value="">-- Role --</option>
                <option v-for="role in ROLES" :key="role" :value="role">{{ role }}</option>
              </select>
            </td>
            <td class="px-5 py-3.5">
              <input
                type="number"
                step="0.1"
                v-model.number="seatExtras[i]"
                class="w-24 rounded-lg border border-slate-700 bg-slate-900 px-4 py-2.5 text-slate-200 transition-colors focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Seats: Mobile Cards -->
    <div class="space-y-3 sm:hidden">
      <div v-for="(seat, i) in game.seats" :key="seat.id" class="rounded-xl border border-slate-800 bg-surface p-4">
        <div class="flex items-center gap-3 mb-3">
          <span class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-warning/10 text-sm font-bold text-warning">
            {{ seat.seat_number }}
          </span>
          <span class="text-base font-medium text-slate-200">{{ seat.display_name }}</span>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-medium uppercase text-slate-500">Role</label>
            <select
              v-model="seatRoles[i]"
              class="min-h-[44px] w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2.5 text-sm text-slate-200 transition-colors focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent"
            >
              <option value="">-- Role --</option>
              <option v-for="role in ROLES" :key="role" :value="role">{{ role }}</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium uppercase text-slate-500">Extra Pts</label>
            <input
              type="number"
              step="0.1"
              v-model.number="seatExtras[i]"
              class="min-h-[44px] w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2.5 text-sm text-slate-200 transition-colors focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Best Move Section -->
    <div class="rounded-xl border border-slate-800 bg-surface p-4 sm:p-6">
      <h2 class="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-400">First Night Kill & Best Move</h2>

      <div class="space-y-3">
        <div class="flex flex-col gap-1.5 sm:flex-row sm:items-center sm:gap-4">
          <label class="text-sm font-medium text-slate-400 sm:w-44">Killed first night</label>
          <select
            v-model="killedSeat"
            class="min-h-[44px] w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2.5 text-sm text-slate-200 transition-colors focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent sm:w-auto sm:px-4 sm:text-base"
          >
            <option value="">-- None --</option>
            <option
              v-for="seat in game.seats"
              :key="seat.seat_number"
              :value="seat.seat_number"
            >
              Seat {{ seat.seat_number }} — {{ seat.display_name }}
            </option>
          </select>
        </div>

        <template v-if="killedSeat !== ''">
          <div v-for="n in 3" :key="n" class="flex flex-col gap-1.5 sm:flex-row sm:items-center sm:gap-4">
            <label class="text-sm font-medium text-info sm:w-44">Guess {{ n }}</label>
            <select
              v-model="bestMoveGuesses[n - 1]"
              class="min-h-[44px] w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2.5 text-sm text-slate-200 transition-colors focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent sm:w-auto sm:px-4 sm:text-base"
            >
              <option value="">-- None --</option>
              <option
                v-for="seat in game.seats"
                :key="seat.seat_number"
                :value="seat.seat_number"
              >
                Seat {{ seat.seat_number }} — {{ seat.display_name }}
              </option>
            </select>
          </div>

          <div class="mt-2 rounded-lg border border-accent/30 bg-accent/5 px-4 py-3">
            Best move bonus: <span class="text-lg font-bold text-accent">+{{ bestMoveBonus }}</span>
          </div>
        </template>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex items-center gap-3">
      <button
        @click="submit"
        :disabled="!canSubmit || saving"
        class="min-h-[44px] flex-1 cursor-pointer rounded-lg bg-accent px-6 py-3 font-semibold text-slate-950 transition-all hover:bg-green-400 hover:shadow-lg hover:shadow-accent/25 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-accent disabled:hover:shadow-none sm:flex-none"
      >
        {{ saving ? 'Saving...' : 'Save Result' }}
      </button>
      <button
        @click="router.back()"
        type="button"
        class="min-h-[44px] cursor-pointer rounded-lg border border-slate-700 px-6 py-3 font-medium text-slate-400 transition-colors hover:border-slate-500 hover:text-slate-200"
      >
        Back
      </button>
    </div>

    <!-- Messages -->
    <div v-if="error" class="rounded-lg border border-red-500/30 bg-red-500/5 px-4 py-3 text-red-400">
      {{ error }}
    </div>
    <div v-if="success" class="rounded-lg border border-accent/30 bg-accent/5 px-4 py-3 text-accent">
      {{ success }}
    </div>
  </div>
</template>
