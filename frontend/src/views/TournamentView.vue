<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getTournament, getParticipants } from '../api/tournaments'
import type { Tournament, Participant } from '../types/api'

const route = useRoute()
const tournament = ref<Tournament | null>(null)
const participants = ref<Participant[]>([])
const loading = ref(true)

onMounted(async () => {
  const id = Number(route.params.id)
  const [t, p] = await Promise.all([getTournament(id), getParticipants(id)])
  tournament.value = t
  participants.value = p
  loading.value = false
})
</script>

<template>
  <div v-if="loading" class="flex items-center gap-3 py-16 text-slate-400">
    <svg class="h-6 w-6 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
    <span>Loading tournament...</span>
  </div>

  <div v-else-if="tournament" class="space-y-6">
    <div class="rounded-xl border border-slate-800 bg-surface p-6">
      <h1 class="font-display text-4xl font-bold tracking-tight text-slate-50">{{ tournament.name }}</h1>
      <p class="mt-1 text-slate-400">{{ participants.length }} participants</p>
    </div>

    <div>
      <h2 class="mb-3 text-xl font-semibold text-slate-200">Participants</h2>
      <div class="overflow-hidden rounded-xl border border-slate-800">
        <table class="w-full">
          <thead>
            <tr class="border-b border-slate-700 bg-slate-800/50">
              <th class="px-5 py-3.5 text-left text-sm font-semibold uppercase tracking-wider text-slate-400">#</th>
              <th class="px-5 py-3.5 text-left text-sm font-semibold uppercase tracking-wider text-slate-400">Name</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800">
            <tr v-for="p in participants" :key="p.id" class="transition-colors hover:bg-slate-800/30">
              <td class="px-5 py-3.5 font-medium text-slate-400">{{ p.id }}</td>
              <td class="px-5 py-3.5 text-slate-200">{{ p.display_name }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
