<template>
  <div class="page-container h-full flex flex-col">
    <!-- Header -->
    <div class="mb-6 reveal">
      <h2 class="section-title">Dashboard RH Analytics</h2>
      <p class="section-subtitle">Aperçu en temps réel de votre vivier de candidats et des offres actives</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <svg class="animate-spin w-10 h-10 text-purple-400" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
    </div>

    <template v-else>
      <!-- KPI Grid -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div v-for="(kpi, i) in formattedKpis" :key="kpi.label"
             class="kpi-card reveal"
             :class="[`reveal-delay-${i+1}`, `glass-card--${kpi.color}`]">
          <div class="flex items-start justify-between mb-3">
            <div class="w-9 h-9 rounded-xl flex items-center justify-center"
                 :style="`background: rgba(${kpi.rgb}, 0.12); border: 1px solid rgba(${kpi.rgb}, 0.2);`">
              <span v-html="kpi.icon" :style="`color: ${kpi.hex};`" class="w-5 h-5"></span>
            </div>
          </div>
          <div class="kpi-card__value" :style="`color: ${kpi.hex};`">{{ kpi.value }}</div>
          <div class="kpi-card__label">{{ kpi.label }}</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <!-- Top Matches -->
        <div class="glass-card p-6 reveal reveal-delay-2 lg:col-span-1 flex flex-col">
          <h3 class="font-heading font-semibold text-white mb-4 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Meilleurs Matchs
          </h3>
          <div class="space-y-3 flex-1 overflow-y-auto min-h-0 pr-2 custom-scrollbar">
            <div v-if="topMatches.length === 0" class="text-text-muted text-sm italic">Aucun match trouvé.</div>
            <div v-for="match in topMatches" :key="match.id"
                 class="flex items-center gap-4 p-3 rounded-xl hover:bg-white/4 transition-colors cursor-pointer border border-white/5">
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-white truncate">{{ match.candidate }}</p>
                <p class="text-xs text-text-secondary truncate">{{ match.job }}</p>
                <div class="mt-2 h-1.5 rounded-full overflow-hidden bg-white/5">
                  <div class="h-full rounded-full transition-all duration-1000"
                       :style="`width: ${match.score}%; background: linear-gradient(90deg, #3B82F6, #8B5CF6);`"></div>
                </div>
              </div>
              <div class="text-right flex-shrink-0">
                <span class="font-heading font-bold text-lg" :class="match.score >= 80 ? 'text-emerald-400' : 'text-amber-400'">
                  {{ match.score }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="glass-card p-6 reveal reveal-delay-3 lg:col-span-2 flex flex-col">
          <h3 class="font-heading font-semibold text-white mb-4 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
            Candidats Récents
          </h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 flex-1 overflow-y-auto min-h-0 pr-2 custom-scrollbar">
            <div v-if="recentActivity.length === 0" class="text-text-muted text-sm italic col-span-2">Aucune activité.</div>
            <div v-for="(activity, i) in recentActivity" :key="activity.id"
                 class="flex items-center gap-3 p-3 rounded-xl transition-colors hover:bg-white/4 border border-white/5">
              <div class="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-xs font-bold"
                   :style="`background: rgba(59,130,246, 0.15); color: #60A5FA; border: 1px solid rgba(59,130,246, 0.3);`">
                {{ activity.initials }}
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-white truncate">{{ activity.name }}</p>
                <p class="text-xs text-text-secondary truncate">{{ activity.title }}</p>
              </div>
              <span class="text-[10px] text-text-muted flex-shrink-0 bg-white/5 px-2 py-1 rounded-md">
                {{ new Date(activity.created_at).toLocaleDateString() }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        <!-- Funnel -->
        <div class="glass-card p-6 reveal reveal-delay-4">
          <h3 class="font-heading font-semibold text-white mb-4">Entonnoir de Recrutement</h3>
          <div class="h-64 relative">
            <Bar v-if="funnelData" :data="funnelData" :options="chartOptions" />
          </div>
        </div>

        <!-- Skills -->
        <div class="glass-card p-6 reveal reveal-delay-5">
          <h3 class="font-heading font-semibold text-white mb-4">Top 10 Compétences (Candidats)</h3>
          <div class="h-64 relative">
            <Bar v-if="skillsData" :data="skillsData" :options="horizontalChartOptions" />
          </div>
        </div>

        <!-- Score Distribution -->
        <div class="glass-card p-6 reveal reveal-delay-6 xl:col-span-1 lg:col-span-2">
          <h3 class="font-heading font-semibold text-white mb-4">Distribution des Scores</h3>
          <div class="h-64 relative">
            <Bar v-if="scoreDistData" :data="scoreDistData" :options="chartOptions" />
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale
} from 'chart.js'
import api from '../services/api'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const loading = ref(true)
const kpis = ref({})
const recentActivity = ref([])
const topMatches = ref([])

// Charts data refs
const funnelData = ref(null)
const skillsData = ref(null)
const scoreDistData = ref(null)

const formattedKpis = computed(() => {
  return [
    { label: 'Candidats', value: kpis.value.total_candidates || 0, color: 'blue', hex: '#60A5FA', rgb: '59,130,246',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>` },
    { label: 'Offres actives', value: kpis.value.total_jobs || 0, color: 'purple', hex: '#A78BFA', rgb: '139,92,246',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>` },
    { label: 'Matchs calculés', value: kpis.value.total_matches || 0, color: 'amber', hex: '#FBBF24', rgb: '245,158,11',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>` },
    { label: 'Score moyen IA', value: kpis.value.avg_score ? kpis.value.avg_score + '%' : '—', color: 'green', hex: '#6EE7B7', rgb: '16,185,129',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>` },
  ]
})

// Chart global options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      titleColor: '#fff',
      bodyColor: '#94a3b8',
      borderColor: 'rgba(255,255,255,0.1)',
      borderWidth: 1,
      padding: 10,
      displayColors: false,
    }
  },
  scales: {
    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
  }
}

const horizontalChartOptions = {
  ...chartOptions,
  indexAxis: 'y',
  scales: {
    x: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
    y: { grid: { display: false }, ticks: { color: '#94a3b8' } }
  }
}

async function fetchAnalytics() {
  try {
    const [kpisRes, recentRes, matchesRes, skillsRes, scoreRes, funnelRes] = await Promise.all([
      api.get('/analytics/kpis'),
      api.get('/analytics/recent-activity'),
      api.get('/analytics/top-matches'),
      api.get('/analytics/skill-distribution'),
      api.get('/analytics/score-distribution'),
      api.get('/analytics/funnel'),
    ])

    kpis.value = kpisRes.data
    recentActivity.value = recentRes.data
    topMatches.value = matchesRes.data

    // Prepare charts
    funnelData.value = {
      labels: funnelRes.data.map(d => d.label),
      datasets: [{
        data: funnelRes.data.map(d => d.count),
        backgroundColor: 'rgba(96, 165, 250, 0.6)',
        borderColor: 'rgba(96, 165, 250, 1)',
        borderWidth: 1,
        borderRadius: 4,
      }]
    }

    skillsData.value = {
      labels: skillsRes.data.map(d => d.skill),
      datasets: [{
        data: skillsRes.data.map(d => d.count),
        backgroundColor: 'rgba(167, 139, 250, 0.6)',
        borderColor: 'rgba(167, 139, 250, 1)',
        borderWidth: 1,
        borderRadius: 4,
      }]
    }

    scoreDistData.value = {
      labels: scoreRes.data.map(d => d.range),
      datasets: [{
        data: scoreRes.data.map(d => d.count),
        backgroundColor: 'rgba(52, 211, 153, 0.6)',
        borderColor: 'rgba(52, 211, 153, 1)',
        borderWidth: 1,
        borderRadius: 4,
      }]
    }
  } catch (e) {
    console.error("Error fetching analytics", e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAnalytics().then(() => {
    // Reveal animation
    setTimeout(() => {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('revealed') })
      }, { threshold: 0.1 })
      document.querySelectorAll('.reveal').forEach(el => observer.observe(el))
    }, 100)
  })
})
</script>
