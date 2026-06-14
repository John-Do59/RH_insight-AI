<template>
  <div class="page-container">

    <!-- Header + Search -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6 reveal">
      <div>
        <h2 class="section-title">Candidats</h2>
        <p class="section-subtitle">{{ candidates.length }} profil(s) dans la base</p>
      </div>
      <div class="flex gap-2 w-full sm:w-auto">
        <input v-model="filters.skills" type="text" placeholder="Filtrer par compétences..." class="glass-input max-w-xs" />
        <input v-model="filters.exp" type="number" placeholder="Exp. min" class="glass-input w-24" />
        <button @click="fetchCandidates" class="glass-btn glass-btn--primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          Rechercher
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div v-for="n in 6" :key="n" class="glass-card p-5 animate-pulse">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-12 h-12 rounded-full bg-white/5"></div>
          <div class="flex-1"><div class="h-3 bg-white/5 rounded mb-2 w-3/4"></div><div class="h-2 bg-white/5 rounded w-1/2"></div></div>
        </div>
        <div class="h-2 bg-white/5 rounded mb-2"></div><div class="h-2 bg-white/5 rounded w-2/3"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="candidates.length === 0" class="flex flex-col items-center justify-center py-24 glass-card">
      <svg class="w-12 h-12 text-text-muted mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
      <p class="text-text-secondary font-medium">Aucun candidat trouvé</p>
      <p class="text-text-muted text-sm mt-1">Essayez d'élargir vos filtres ou d'ajouter des candidats.</p>
    </div>

    <!-- Candidate Cards -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div v-for="(c, i) in candidates" :key="c.id"
           class="glass-card p-5 group cursor-pointer reveal"
           :class="`reveal-delay-${(i % 4) + 1}`">

        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-3">
            <!-- Avatar -->
            <div class="w-11 h-11 rounded-2xl flex items-center justify-center font-bold text-sm text-white flex-shrink-0"
                 style="background: linear-gradient(135deg, #3B82F6, #8B5CF6); box-shadow: 0 4px 12px rgba(59,130,246,0.3)">
              {{ initials(c.name) }}
            </div>
            <div>
              <h3 class="text-sm font-semibold text-white group-hover:text-blue-300 transition-colors">{{ c.name }}</h3>
              <p class="text-xs text-text-secondary">{{ c.title || 'Profil non renseigné' }}</p>
            </div>
          </div>
          <div v-if="c.experience_years" class="badge badge--blue text-[10px]">
            {{ c.experience_years }} ans
          </div>
        </div>

        <!-- Skills -->
        <div v-if="c.skills && c.skills.length" class="flex flex-wrap gap-1.5 mb-4">
          <span v-for="skill in c.skills.slice(0, 4)" :key="skill" class="badge badge--purple text-[10px]">{{ skill }}</span>
          <span v-if="c.skills.length > 4" class="badge text-[10px]" style="background: rgba(255,255,255,0.05); color: #94A3B8;">+{{ c.skills.length - 4 }}</span>
        </div>

        <!-- Location -->
        <div v-if="c.location" class="flex items-center gap-1.5 text-xs text-text-muted">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
          {{ c.location }}
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const candidates = ref([])
const isLoading = ref(true)
const filters = ref({ skills: '', exp: null })

const initials = (name) => name?.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2) || '?'

const fetchCandidates = async () => {
  isLoading.value = true
  try {
    const params = {}
    if (filters.value.skills) params.skills = filters.value.skills
    if (filters.value.exp) params.exp = filters.value.exp
    const { data } = await api.get('/search/candidates', { params })
    candidates.value = data
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
    // Trigger scroll reveal
    setTimeout(() => {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('revealed'))
    }, 100)
  }
}

onMounted(fetchCandidates)
</script>
