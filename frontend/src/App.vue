<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const menuOpen = ref(false)
const router = useRouter()

router.afterEach(() => {
  menuOpen.value = false
})
</script>

<template>
  <div class="min-h-screen bg-slate-950">
    <nav class="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/80 backdrop-blur-lg">
      <div class="mx-auto flex max-w-5xl items-center justify-between px-4 py-3 sm:px-6">
        <router-link to="/tournament/1" class="flex items-center gap-2.5 no-underline">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-accent font-display text-sm font-bold text-slate-950">
            IJ
          </div>
          <span class="font-display text-lg font-bold tracking-tight text-slate-50">IMAFA Judge</span>
        </router-link>

        <!-- Desktop nav -->
        <div class="hidden sm:flex sm:items-center sm:gap-1">
          <router-link
            to="/tournament/1/standings"
            active-class="!bg-accent/10 !text-accent"
            class="rounded-lg px-3 py-1.5 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-50"
          >
            Standings
          </router-link>
          <router-link
            to="/tournament/1/games"
            active-class="!bg-accent/10 !text-accent"
            class="rounded-lg px-3 py-1.5 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-50"
          >
            Games
          </router-link>
          <router-link
            to="/tournament/1"
            active-class="!bg-accent/10 !text-accent"
            class="rounded-lg px-3 py-1.5 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-50"
          >
            Tournament
          </router-link>
        </div>

        <!-- Mobile hamburger button -->
        <button
          @click="menuOpen = !menuOpen"
          class="flex sm:hidden h-10 w-10 cursor-pointer items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-50"
          :aria-label="menuOpen ? 'Close menu' : 'Open menu'"
        >
          <svg v-if="!menuOpen" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Mobile menu dropdown -->
      <div v-if="menuOpen" class="border-t border-slate-800 bg-slate-950/95 backdrop-blur-lg sm:hidden">
        <div class="space-y-1 px-4 py-3">
          <router-link
            to="/tournament/1/standings"
            active-class="!bg-accent/10 !text-accent"
            class="block rounded-lg px-3 py-2.5 text-base font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-50"
          >
            Standings
          </router-link>
          <router-link
            to="/tournament/1/games"
            active-class="!bg-accent/10 !text-accent"
            class="block rounded-lg px-3 py-2.5 text-base font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-50"
          >
            Games
          </router-link>
          <router-link
            to="/tournament/1"
            active-class="!bg-accent/10 !text-accent"
            class="block rounded-lg px-3 py-2.5 text-base font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-50"
          >
            Tournament
          </router-link>
        </div>
      </div>
    </nav>

    <main class="mx-auto max-w-5xl px-4 py-6 sm:px-6 sm:py-8">
      <router-view />
    </main>
  </div>
</template>
