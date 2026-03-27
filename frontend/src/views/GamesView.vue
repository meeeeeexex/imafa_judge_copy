<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getGames } from '../api/tournaments'
import type { Game } from '../types/api'

const route = useRoute()
const games = ref<Game[]>([])
const loading = ref(true)

onMounted(async () => {
  const id = Number(route.params.id)
  games.value = await getGames(id)
  loading.value = false
})
</script>

<template>
  <div v-if="loading" class="flex items-center gap-3 py-16 text-slate-400">
    <svg class="h-6 w-6 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
    <span>Loading games...</span>
  </div>

  <div v-else class="space-y-4 sm:space-y-6">
    <h1 class="font-display text-3xl font-bold tracking-tight text-slate-50 sm:text-4xl">Games</h1>

    <!-- Desktop table -->
    <div class="hidden sm:block overflow-hidden rounded-xl border border-slate-800">
      <table class="w-full">
        <thead>
          <tr class="border-b border-slate-700 bg-slate-800/50">
            <th class="px-5 py-3.5 text-left text-sm font-semibold uppercase tracking-wider text-slate-400">Round</th>
            <th class="px-5 py-3.5 text-left text-sm font-semibold uppercase tracking-wider text-slate-400">Table</th>
            <th class="px-5 py-3.5 text-left text-sm font-semibold uppercase tracking-wider text-slate-400">Winner</th>
            <th class="px-5 py-3.5 text-left text-sm font-semibold uppercase tracking-wider text-slate-400">Status</th>
            <th class="px-5 py-3.5 text-right text-sm font-semibold uppercase tracking-wider text-slate-400"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <router-link
            v-for="game in games"
            :key="game.id"
            :to="`/game/${game.id}/edit`"
            custom
            v-slot="{ navigate }"
          >
            <tr
              @click="navigate"
              class="cursor-pointer transition-colors hover:bg-slate-800/30"
            >
              <td class="px-5 py-3.5 text-slate-200">{{ game.round_number }}</td>
              <td class="px-5 py-3.5 text-slate-200">{{ game.table_number }}</td>
              <td class="px-5 py-3.5">
                <span
                  v-if="game.winning_team"
                  class="inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold ring-1 ring-inset"
                  :class="game.winning_team === 'RED'
                    ? 'bg-red-500/10 text-red-400 ring-red-500/20'
                    : 'bg-purple-500/10 text-purple-400 ring-purple-500/20'"
                >
                  {{ game.winning_team }}
                </span>
                <span v-else class="text-slate-600">---</span>
              </td>
              <td class="px-5 py-3.5">
                <span
                  class="inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold ring-1 ring-inset"
                  :class="game.winning_team
                    ? 'bg-accent/10 text-accent ring-accent/20'
                    : 'bg-warning/10 text-warning ring-warning/20'"
                >
                  {{ game.winning_team ? 'Complete' : 'Pending' }}
                </span>
              </td>
              <td class="px-5 py-3.5 text-right">
                <span class="inline-flex items-center gap-1 text-sm font-medium text-info">
                  Edit
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                  </svg>
                </span>
              </td>
            </tr>
          </router-link>
        </tbody>
      </table>
    </div>

    <!-- Mobile cards -->
    <div class="space-y-3 sm:hidden">
      <router-link
        v-for="game in games"
        :key="game.id"
        :to="`/game/${game.id}/edit`"
        class="block cursor-pointer rounded-xl border border-slate-800 bg-surface p-4 transition-colors active:bg-slate-800/50"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span class="text-base font-semibold text-slate-200">Round {{ game.round_number }}</span>
            <span class="text-sm text-slate-500">Table {{ game.table_number }}</span>
          </div>
          <span
            class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ring-1 ring-inset"
            :class="game.winning_team
              ? 'bg-accent/10 text-accent ring-accent/20'
              : 'bg-warning/10 text-warning ring-warning/20'"
          >
            {{ game.winning_team ? 'Done' : 'Pending' }}
          </span>
        </div>

        <div class="mt-2 flex items-center justify-between">
          <div>
            <span
              v-if="game.winning_team"
              class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ring-1 ring-inset"
              :class="game.winning_team === 'RED'
                ? 'bg-red-500/10 text-red-400 ring-red-500/20'
                : 'bg-purple-500/10 text-purple-400 ring-purple-500/20'"
            >
              {{ game.winning_team }} wins
            </span>
            <span v-else class="text-sm text-slate-600">No result yet</span>
          </div>
          <span class="inline-flex items-center gap-1 text-sm font-medium text-info">
            Edit
            <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </span>
        </div>
      </router-link>
    </div>
  </div>
</template>
