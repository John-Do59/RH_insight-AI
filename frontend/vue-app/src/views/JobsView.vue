<template>
  <div class="page-container">

    <!-- Header + Search -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6 reveal">
      <div>
        <h2 class="section-title">Offres d'emploi</h2>
        <p class="section-subtitle">{{ jobs.length }} offre(s) disponible(s)</p>
      </div>
      <div class="flex gap-2 w-full sm:w-auto">
        <input v-model="filters.skills" type="text" placeholder="Compétences requises..." class="glass-input max-w-xs" />
        <input v-model="filters.location" type="text" placeholder="Lieu..." class="glass-input w-32" />
        <button @click="fetchJobs" class="glass-btn glass-btn--primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          Filtrer
        </button>
      </div>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div v-for="n in 6" :key="n" class="glass-card p-5 animate-pulse">
        <div class="h-4 bg-white/5 rounded w-3/4 mb-3"></div>
        <div class="h-3 bg-white/5 rounded w-1/2 mb-4"></div>
        <div class="flex gap-2 mb-4"><div class="h-5 w-16 bg-white/5 rounded-full"></div><div class="h-5 w-20 bg-white/5 rounded-full"></div></div>
        <div class="h-3 bg-white/5 rounded w-1/3"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="jobs.length === 0" class="flex flex-col items-center justify-center py-24 glass-card">
      <svg class="w-12 h-12 text-text-muted mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><rect width="20" height="14" x="2" y="7" rx="2" stroke-width="1.5"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" stroke-width="1.5"/></svg>
      <p class="text-text-secondary font-medium">Aucune offre trouvée</p>
    </div>

    <!-- Job Cards -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div v-for="(j, i) in jobs" :key="j.id"
           class="glass-card p-5 group cursor-pointer reveal"
           :class="`reveal-delay-${(i % 4) + 1}`"
           @click="selectJob(j)">

        <!-- Header -->
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="font-heading font-semibold text-white text-sm group-hover:text-amber-300 transition-colors">{{ j.title }}</h3>
            <p class="text-xs text-text-secondary mt-0.5">{{ j.company || 'Entreprise non précisée' }}</p>
          </div>
          <div v-if="j.contract_type" class="badge badge--blue text-[10px] flex-shrink-0 ml-2">{{ j.contract_type }}</div>
        </div>

        <!-- Required skills -->
        <div v-if="j.skills && j.skills.length" class="flex flex-wrap gap-1.5 mb-4">
          <span v-for="skill in j.skills.slice(0, 4)" :key="skill" class="badge badge--purple text-[10px]">{{ skill }}</span>
          <span v-if="j.skills.length > 4" class="badge text-[10px]" style="background: rgba(255,255,255,0.05); color: #94A3B8;">+{{ j.skills.length - 4 }}</span>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-between">
          <div v-if="j.location" class="flex items-center gap-1 text-xs text-text-muted">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            {{ j.location }}
          </div>
          <button @click.stop="rankCandidates(j)" class="glass-btn text-xs py-1 px-3">
            Voir les profils →
          </button>
        </div>
      </div>
    </div>

    <!-- Ranking Panel -->
    <div v-if="selectedJob" class="fixed inset-0 z-50 flex items-center justify-center p-4" style="background: rgba(3,7,18,0.8); backdrop-filter: blur(8px);">
      <div class="glass-card w-full max-w-2xl max-h-[80vh] flex flex-col">
        <div class="flex items-center justify-between p-6 border-b border-white/5">
          <div>
            <h3 class="font-heading font-semibold text-white">Top candidats pour</h3>
            <p class="text-blue-400 font-medium">{{ selectedJob.title }}</p>
          </div>
          <button @click="selectedJob = null; ranking = []" class="glass-btn py-1.5 px-3 text-xs">Fermer ✕</button>
        </div>
        <div class="flex-1 overflow-y-auto p-6 space-y-3">
          <div v-if="isRanking" class="flex items-center justify-center py-12">
            <div class="animate-spin w-8 h-8 border-2 border-blue-400 border-t-transparent rounded-full"></div>
          </div>
          <div v-else v-for="(r, i) in ranking" :key="r.candidate_id"
               class="flex items-center gap-4 p-4 rounded-xl hover:bg-white/4 transition-colors">
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold"
                 :style="`background: rgba(${i === 0 ? '245,158,11' : '59,130,246'}, 0.15); color: ${i === 0 ? '#FCD34D' : '#93C5FD'};`">
              {{ i + 1 }}
            </div>
            <div class="flex-1">
              <p class="text-sm font-semibold text-white">{{ r.name }}</p>
              <div class="flex flex-wrap gap-1 mt-1">
                <span v-for="s in r.strengths.slice(0,3)" :key="s" class="badge badge--green text-[10px]">{{ s }}</span>
              </div>
            </div>
            <div class="text-right">
              <span class="font-heading font-bold text-xl"
                    :class="r.score >= 80 ? 'text-emerald-400' : r.score >= 60 ? 'text-amber-400' : 'text-rose-400'">
                {{ Math.round(r.score) }}
              </span>
              <p class="text-[10px] text-text-muted">/100</p>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const jobs = ref([])
const isLoading = ref(true)
const filters = ref({ skills: '', location: '' })
const selectedJob = ref(null)
const ranking = ref([])
const isRanking = ref(false)

const fetchJobs = async () => {
  isLoading.value = true
  try {
    const params = {}
    if (filters.value.skills) params.skills = filters.value.skills
    if (filters.value.location) params.location = filters.value.location
    const { data } = await api.get('/search/jobs', { params })
    jobs.value = data
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
    setTimeout(() => {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('revealed'))
    }, 100)
  }
}

const selectJob = (j) => { selectedJob.value = j }

const rankCandidates = async (j) => {
  selectedJob.value = j
  isRanking.value = true
  ranking.value = []
  try {
    const { data } = await api.post(`/ranking/job/${j.id}?top_n=10`)
    ranking.value = data
  } catch (e) {
    console.error(e)
  } finally {
    isRanking.value = false
  }
}

onMounted(fetchJobs)
</script>
