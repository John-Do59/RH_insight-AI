<template>
  <div class="flex h-screen overflow-hidden" style="background: var(--color-bg-void);">

    <!-- Glass Sidebar -->
    <aside class="glass-sidebar w-64 flex-shrink-0 flex flex-col z-20">
      <!-- Logo -->
      <div class="h-16 flex items-center px-5 border-b border-white/5">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl flex items-center justify-center"
               style="background: linear-gradient(135deg, #3B82F6, #8B5CF6); box-shadow: 0 0 16px rgba(59,130,246,0.4)">
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>
          </div>
          <div>
            <span class="font-heading font-bold text-white tracking-tight text-sm block">RH Insight</span>
            <span class="text-[10px] text-text-secondary tracking-widest uppercase">AI Platform</span>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto py-5 px-3 space-y-1">
        <router-link v-for="item in navItems" :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 group"
          :class="isActive(item.to)
            ? 'bg-white/8 text-white border border-white/10'
            : 'text-text-secondary hover:text-white hover:bg-white/4'"
        >
          <span class="w-5 h-5 flex-shrink-0 transition-colors"
                :class="isActive(item.to) ? item.activeColor : 'text-text-muted group-hover:text-text-secondary'"
                v-html="item.icon"></span>
          {{ item.label }}
          <span v-if="item.badge" class="ml-auto badge badge--blue text-[10px]">{{ item.badge }}</span>
        </router-link>
      </nav>

      <!-- Bottom: user + logout -->
      <div class="p-3 border-t border-white/5">
        <div @click="handleLogout"
             class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-rose-500/10 cursor-pointer transition-all group">
          <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white"
               style="background: linear-gradient(135deg, #3B82F6, #8B5CF6);">
            {{ userInitials }}
          </div>
          <div class="flex-1 overflow-hidden">
            <p class="text-sm font-medium text-white truncate group-hover:text-rose-400">{{ userName }}</p>
            <p class="text-xs text-text-secondary">Déconnexion</p>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-text-muted group-hover:text-rose-400"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>
        </div>
      </div>
    </aside>

    <!-- Main area -->
    <main class="flex-1 flex flex-col min-w-0 overflow-hidden">

      <!-- Topbar -->
      <header class="h-16 flex items-center justify-between px-6 border-b border-white/5 flex-shrink-0"
              style="background: rgba(3,7,18,0.6); backdrop-filter: blur(20px);">
        <h1 class="font-heading font-semibold text-white tracking-tight">{{ pageTitle }}</h1>
        <div class="flex items-center gap-2">
          <span class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium"
                style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); color: #6EE7B7;">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            IA Opérationnelle
          </span>
        </div>
      </header>

      <!-- Page content -->
      <div class="flex-1 overflow-y-auto">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const userName = computed(() => authStore.user?.full_name || 'Utilisateur')
const userInitials = computed(() => {
  return userName.value.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2)
})

const pageTitle = computed(() => {
  const titles = {
    '/dashboard': 'Vue d\'ensemble',
    '/candidates': 'Candidats',
    '/jobs': 'Offres',
    '/job-agent': 'Assistant Recrutement',
    '/search': 'Recherche',
  }
  return titles[route.path] || 'RH Insight AI'
})

const isActive = (path) => route.path === path

const navItems = [
  {
    to: '/dashboard',
    label: 'Vue d\'ensemble',
    activeColor: 'text-blue-400',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>`
  },
  {
    to: '/candidates',
    label: 'Candidats',
    activeColor: 'text-purple-400',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`
  },
  {
    to: '/jobs',
    label: 'Offres d\'emploi',
    activeColor: 'text-amber-400',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`
  },
  {
    to: '/job-agent',
    label: 'Match d\'offre',
    activeColor: 'text-emerald-400',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>`
  },
  {
    to: '/chat',
    label: 'Assistant IA',
    activeColor: 'text-pink-400',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`
  },
  {
    to: '/ingestion',
    label: 'Ingestion Données',
    activeColor: 'text-orange-400',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>`
  },
]

const handleLogout = () => {
  authStore.logout()
  router.push('/auth')
}
</script>
