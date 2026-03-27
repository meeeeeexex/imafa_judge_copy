<template>
  <div class="min-h-screen bg-slate-950">
    <nav class="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/80 backdrop-blur-lg">
      <div class="mx-auto flex max-w-5xl items-center gap-6 px-4 py-3 sm:px-6">
        <router-link to="/tournament/1" class="flex items-center gap-2.5 no-underline">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-accent font-display text-sm font-bold text-slate-950">
            IJ
          </div>
          <span class="font-display text-lg font-bold tracking-tight text-slate-50">IMAFA Judge</span>
        </router-link>

        <div class="flex items-center gap-1">
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
      </div>
    </nav>

    <main class="mx-auto max-w-5xl px-4 py-8 sm:px-6">
      <router-view />
    </main>
  </div>
</template>
