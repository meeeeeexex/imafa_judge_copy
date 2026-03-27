import { createRouter, createWebHistory } from 'vue-router'
import TournamentView from './views/TournamentView.vue'
import GamesView from './views/GamesView.vue'
import GameEditView from './views/GameEditView.vue'
import StandingsView from './views/StandingsView.vue'

const routes = [
  { path: '/', redirect: '/tournament/1/standings' },
  { path: '/tournament/:id', component: TournamentView },
  { path: '/tournament/:id/games', component: GamesView },
  { path: '/game/:id/edit', component: GameEditView },
  { path: '/tournament/:id/standings', component: StandingsView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
