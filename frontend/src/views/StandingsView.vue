<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getStandings } from '../api/tournaments'
import type { StandingsEntry } from '../types/api'

const route = useRoute()
const standings = ref<StandingsEntry[]>([])
const loading = ref(true)

onMounted(async () => {
  const id = Number(route.params.id)
  standings.value = await getStandings(id)
  loading.value = false
})
</script>

<template>
  <div v-if="loading" class="flex items-center gap-3 py-16 text-slate-400">
    <svg class="h-6 w-6 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
    <span>Computing standings...</span>
  </div>

  <div v-else class="space-y-4 sm:space-y-6">
    <h1 class="font-display text-3xl font-bold tracking-tight text-slate-50 sm:text-4xl">Standings</h1>

    <!-- Desktop table -->
    <div class="hidden sm:block overflow-hidden rounded-xl border border-slate-800">
      <table class="w-full">
        <thead>
          <tr class="border-b border-slate-700 bg-slate-800/50">
            <th class="px-5 py-3.5 text-center text-sm font-semibold uppercase tracking-wider text-slate-400">#</th>
            <th class="px-5 py-3.5 text-left text-sm font-semibold uppercase tracking-wider text-slate-400">Player</th>
            <th class="px-5 py-3.5 text-center text-sm font-semibold uppercase tracking-wider text-slate-400">GP</th>
            <th class="px-5 py-3.5 text-center text-sm font-semibold uppercase tracking-wider text-slate-400">W</th>
            <th class="px-5 py-3.5 text-center text-sm font-semibold uppercase tracking-wider text-slate-400">L</th>
            <th class="px-5 py-3.5 text-center text-sm font-semibold uppercase tracking-wider text-slate-400">Base</th>
            <th class="px-5 py-3.5 text-center text-sm font-semibold uppercase tracking-wider text-slate-400">Extra</th>
            <th class="px-5 py-3.5 text-center text-sm font-semibold uppercase tracking-wider text-slate-400">Total</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <tr
            v-for="(entry, i) in standings"
            :key="entry.participant_id"
            class="transition-colors hover:bg-slate-800/30"
            :class="{ 'bg-accent/5': i < 3 }"
          >
            <td class="px-5 py-3.5 text-center">
              <span
                class="inline-flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold"
                :class="
                  i === 0 ? 'bg-yellow-500/20 text-yellow-400' :
                  i === 1 ? 'bg-slate-400/20 text-slate-300' :
                  i === 2 ? 'bg-amber-600/20 text-amber-500' :
                  'text-slate-500'
                "
              >
                {{ i + 1 }}
              </span>
            </td>
            <td class="px-5 py-3.5 font-medium text-slate-200">{{ entry.display_name }}</td>
            <td class="px-5 py-3.5 text-center text-slate-400">{{ entry.games_played }}</td>
            <td class="px-5 py-3.5 text-center font-semibold text-accent">{{ entry.wins }}</td>
            <td class="px-5 py-3.5 text-center font-semibold text-danger">{{ entry.losses }}</td>
            <td class="px-5 py-3.5 text-center text-slate-300">{{ entry.base_points }}</td>
            <td class="px-5 py-3.5 text-center text-info">{{ entry.extra_points }}</td>
            <td class="px-5 py-3.5 text-center">
              <span class="text-lg font-bold text-accent">{{ entry.total_points }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mobile cards -->
    <div class="space-y-3 sm:hidden">
      <div
        v-for="(entry, i) in standings"
        :key="entry.participant_id"
        class="rounded-xl border border-slate-800 p-4"
        :class="i < 3 ? 'bg-accent/5' : 'bg-surface'"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span
              class="inline-flex h-9 w-9 items-center justify-center rounded-full text-sm font-bold"
              :class="
                i === 0 ? 'bg-yellow-500/20 text-yellow-400' :
                i === 1 ? 'bg-slate-400/20 text-slate-300' :
                i === 2 ? 'bg-amber-600/20 text-amber-500' :
                'bg-slate-800 text-slate-500'
              "
            >
              {{ i + 1 }}
            </span>
            <span class="text-base font-semibold text-slate-200">{{ entry.display_name }}</span>
          </div>
          <span class="text-xl font-bold text-accent">{{ entry.total_points }}</span>
        </div>

        <div class="mt-3 grid grid-cols-4 gap-2 text-center text-sm">
          <div class="rounded-lg bg-slate-800/50 px-2 py-1.5">
            <div class="text-xs text-slate-500">GP</div>
            <div class="font-medium text-slate-300">{{ entry.games_played }}</div>
          </div>
          <div class="rounded-lg bg-slate-800/50 px-2 py-1.5">
            <div class="text-xs text-slate-500">W</div>
            <div class="font-semibold text-accent">{{ entry.wins }}</div>
          </div>
          <div class="rounded-lg bg-slate-800/50 px-2 py-1.5">
            <div class="text-xs text-slate-500">L</div>
            <div class="font-semibold text-danger">{{ entry.losses }}</div>
          </div>
          <div class="rounded-lg bg-slate-800/50 px-2 py-1.5">
            <div class="text-xs text-slate-500">Extra</div>
            <div class="font-medium text-info">{{ entry.extra_points }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
