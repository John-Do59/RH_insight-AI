<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

const authStore = useAuthStore();
const jobMessage = ref('');
const isAnalyzing = ref(false);
const parsedJob = ref(null);
const candidates = ref([]);
const showDebug = ref(false);

const analyzeJob = async () => {
  if (!jobMessage.value.trim()) return;
  
  isAnalyzing.value = true;
  parsedJob.value = null;
  candidates.value = [];
  
  try {
    const response = await api.post('/job-agent/analyze', {
      message: jobMessage.value
    });
    
    parsedJob.value = response.data.job;
    candidates.value = response.data.candidates;
  } catch (error) {
    console.error("Error analyzing job:", error);
    alert("Une erreur s'est produite lors de l'analyse.");
  } finally {
    isAnalyzing.value = false;
  }
};
</script>

<template>
  <div class="page-container h-full flex flex-col">
    <!-- Header -->
    <div class="mb-6 reveal">
      <h2 class="section-title">Assistant Recrutement IA</h2>
      <p class="section-subtitle">Analysez une description de poste en texte libre et trouvez les meilleurs profils.</p>
    </div>

    <div class="flex flex-col lg:flex-row gap-6 flex-1 min-h-0">
      
      <!-- Input Panel -->
      <div class="w-full lg:w-1/2 flex flex-col gap-4 reveal reveal-delay-1">
        <div class="glass-card p-5 flex flex-col flex-1 min-h-0">
          <textarea 
            v-model="jobMessage"
            placeholder="Ex: Recherche un développeur Backend Python avec de solides compétences en FastAPI et PostgreSQL. Au moins 3 ans d'expérience. Le profil doit aussi connaître Docker..."
            class="glass-input flex-1 resize-none font-medium mb-4"
            :disabled="isAnalyzing"
          ></textarea>
          
          <div class="flex justify-between items-center mt-auto pt-2 border-t border-white/5">
            <label class="flex items-center gap-2 text-xs text-text-secondary cursor-pointer hover:text-white transition-colors">
              <input type="checkbox" v-model="showDebug" class="rounded bg-white/5 border-white/10 text-blue-500 focus:ring-0 focus:ring-offset-0">
              <span>Mode Debug (JSON)</span>
            </label>
            <button 
              @click="analyzeJob"
              :disabled="isAnalyzing || !jobMessage"
              class="glass-btn glass-btn--primary"
            >
              <span v-if="isAnalyzing" class="flex items-center gap-2">
                <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyse...
              </span>
              <span v-else class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                Analyser l'offre
              </span>
            </button>
          </div>
        </div>

        <!-- Debug Panel -->
        <div v-if="showDebug && parsedJob" class="glass-card border-emerald-500/20 p-4 overflow-auto text-xs font-mono h-48 reveal">
          <p class="text-emerald-400 mb-2">// Extraction structurée via LLM</p>
          <pre class="text-text-secondary">{{ JSON.stringify(parsedJob, null, 2) }}</pre>
        </div>
      </div>

      <!-- Results Panel -->
      <div class="w-full lg:w-1/2 flex flex-col gap-4 reveal reveal-delay-2">
        
        <div v-if="isAnalyzing" class="glass-card flex-1 flex flex-col items-center justify-center p-12 relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-premium opacity-5 animate-pulse"></div>
          <div class="relative z-10 flex flex-col items-center">
            <div class="w-16 h-16 rounded-full flex items-center justify-center bg-blue-500/10 border border-blue-500/20 mb-6 glow-blue">
              <svg class="animate-spin h-8 w-8 text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
            <h3 class="font-heading font-semibold text-white mb-2">Analyse sémantique en cours</h3>
            <p class="text-sm text-text-secondary text-center">Extraction des compétences et calcul de la distance vectorielle dans pgvector...</p>
          </div>
        </div>

        <div v-else-if="candidates.length > 0" class="flex-col gap-4 overflow-y-auto pr-2" style="max-height: calc(100vh - 12rem);">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-heading font-semibold text-white flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Top Matchs ({{ candidates.length }})
            </h3>
          </div>
          
          <div v-for="(candidate, index) in candidates" :key="candidate.id" 
               class="glass-card p-4 hover:border-white/10 transition-colors mb-3 reveal"
               :class="`reveal-delay-${(index % 4) + 1}`">
            <div class="flex justify-between items-start mb-4">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold"
                     :style="`background: rgba(${index === 0 ? '245,158,11' : '59,130,246'}, 0.15); color: ${index === 0 ? '#FCD34D' : '#93C5FD'};`">
                  {{ index + 1 }}
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-white">{{ candidate.name }}</h3>
                </div>
              </div>
              <div class="text-right">
                <span class="font-heading font-bold text-xl"
                      :class="candidate.score >= 80 ? 'text-emerald-400' : candidate.score >= 60 ? 'text-amber-400' : 'text-rose-400'">
                  {{ Math.round(candidate.score) }}
                </span>
                <span class="text-[10px] text-text-muted">/100</span>
              </div>
            </div>
            
            <div class="space-y-3">
              <div v-if="candidate.strengths && candidate.strengths.length > 0">
                <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block mb-1.5">Forces</span>
                <div class="flex flex-wrap gap-1">
                  <span v-for="skill in candidate.strengths" :key="skill" class="badge badge--green text-[10px]">
                    {{ skill }}
                  </span>
                </div>
              </div>
              
              <div v-if="candidate.gaps && candidate.gaps.length > 0">
                <span class="text-[10px] font-bold text-rose-400 uppercase tracking-wider block mb-1.5">Manques</span>
                <div class="flex flex-wrap gap-1">
                  <span v-for="skill in candidate.gaps" :key="skill" class="badge badge--red text-[10px]">
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="parsedJob !== null && candidates.length === 0" class="glass-card border-rose-500/20 p-8 flex flex-col items-center justify-center text-center">
          <svg class="w-10 h-10 text-rose-400/50 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
          <p class="text-rose-200 font-medium text-sm">Aucun candidat correspondant trouvé.</p>
          <p class="text-rose-400/70 text-xs mt-1">Essayez d'assouplir vos critères.</p>
        </div>

        <div v-else class="glass-card flex-1 flex flex-col items-center justify-center p-12 text-center opacity-50">
          <svg class="w-12 h-12 text-white/20 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <p class="text-text-secondary text-sm">En attente d'une offre d'emploi à analyser.</p>
        </div>
      </div>
      
    </div>
  </div>
</template>

<style scoped>
/* Scoped styles if needed, mostly handled by tailwind & style.css */
textarea {
  min-height: 200px;
}
</style>
