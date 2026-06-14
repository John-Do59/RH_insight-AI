<template>
  <div class="page-container">
    <!-- Header -->
    <div class="mb-8 reveal">
      <h2 class="section-title">Ingestion des Données</h2>
      <p class="section-subtitle">Importez vos CVs et vos offres d'emploi — l'IA analyse et structure automatiquement les données.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- === CANDIDAT UPLOAD === -->
      <div class="glass-card p-6 flex flex-col gap-5 reveal reveal-delay-1">
        <div class="flex items-center gap-3 mb-1">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center" style="background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.3);">
            <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </div>
          <h3 class="font-heading font-semibold text-xl text-purple-400">Ajouter un Candidat</h3>
        </div>

        <!-- Drop zone -->
        <div
          class="min-h-[12rem] border-2 border-dashed rounded-2xl flex flex-col items-center justify-center p-8 cursor-pointer transition-all duration-300"
          :class="[
            candidateDragging ? 'border-purple-500/70 bg-purple-500/10 scale-[1.01]' : 'border-white/10 hover:border-purple-500/50 hover:bg-purple-500/5',
            candidateStatus === 'processing' ? 'pointer-events-none opacity-60' : ''
          ]"
          @click="$refs.candidateFileInput.click()"
          @dragover.prevent="candidateDragging = true"
          @dragleave.prevent="candidateDragging = false"
          @drop.prevent="onCandidateDrop"
        >
          <input ref="candidateFileInput" type="file" class="hidden" accept=".pdf,.docx,.txt" @change="onCandidateFile" />

          <div v-if="candidateStatus === 'idle'" class="text-center">
            <svg class="w-12 h-12 mx-auto mb-3 text-purple-400/40" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
            <p class="text-white/80 font-medium">Glissez un CV ici ou <span class="text-purple-400 underline underline-offset-2">parcourez</span></p>
            <p class="text-text-muted text-xs mt-1">PDF, DOCX ou TXT — max 10 MB</p>
          </div>

          <div v-else-if="candidateStatus === 'uploading'" class="text-center">
            <svg class="animate-spin w-10 h-10 mx-auto mb-3 text-purple-400" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            <p class="text-purple-300 text-sm font-medium">Envoi en cours…</p>
          </div>

          <div v-else-if="candidateStatus === 'processing'" class="text-center">
            <div class="relative w-12 h-12 mx-auto mb-3">
              <svg class="animate-spin w-12 h-12 text-purple-500/30" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3"/></svg>
              <svg class="animate-spin w-12 h-12 text-purple-400 absolute inset-0" fill="none" viewBox="0 0 24 24" style="animation-duration:1.2s"><path class="opacity-80" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            </div>
            <p class="text-purple-300 text-sm font-medium">Analyse IA en cours…</p>
            <p class="text-text-muted text-xs mt-1">Extraction des compétences, expériences, formations…</p>
          </div>
        </div>

        <!-- Processing steps indicator -->
        <div v-if="candidateStatus === 'processing'" class="flex items-center gap-2 text-xs text-text-muted px-1">
          <span v-for="(step, i) in parsingSteps" :key="i"
            class="flex items-center gap-1 transition-all duration-500"
            :class="i <= candidateStep ? 'text-purple-400' : 'text-text-muted/40'">
            <svg v-if="i < candidateStep" class="w-3 h-3 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
            <svg v-else-if="i === candidateStep" class="animate-spin w-3 h-3" fill="none" viewBox="0 0 24 24"><path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            <span v-else class="w-3 h-3 rounded-full border border-current inline-block"></span>
            {{ step }}
            <span v-if="i < parsingSteps.length - 1" class="mx-1 text-text-muted/30">›</span>
          </span>
        </div>

        <!-- Success result -->
        <transition name="slide-up">
          <div v-if="candidateResult" class="p-4 rounded-xl text-sm bg-emerald-500/10 border border-emerald-500/20">
            <div class="flex items-start gap-3">
              <div class="mt-0.5 w-8 h-8 rounded-lg bg-emerald-500/15 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              </div>
              <div class="flex-1">
                <p class="font-semibold text-emerald-300 text-sm">Candidat ajouté avec succès !</p>
                <p class="text-emerald-400/70 text-xs mt-0.5">
                  <span v-if="candidateFilename">{{ candidateFilename }} — </span>L'analyse IA est en cours en arrière-plan.
                </p>
              </div>
              <button @click="candidateResult = null; candidateStatus = 'idle'" class="text-white/30 hover:text-white/70 transition-colors">✕</button>
            </div>
          </div>
        </transition>

        <!-- Error -->
        <transition name="slide-up">
          <div v-if="candidateError" class="p-4 rounded-xl text-sm bg-rose-500/10 border border-rose-500/20">
            <div class="flex items-start gap-3">
              <span class="text-rose-400 text-lg">⚠</span>
              <div class="flex-1">
                <p class="font-semibold text-rose-300 text-sm">Erreur d'upload</p>
                <p class="text-rose-400/70 text-xs mt-0.5">{{ candidateError }}</p>
              </div>
              <button @click="candidateError = null; candidateStatus = 'idle'" class="text-white/30 hover:text-white/70 transition-colors">✕</button>
            </div>
          </div>
        </transition>
      </div>

      <!-- === OFFRE D'EMPLOI UPLOAD === -->
      <div class="glass-card p-6 flex flex-col gap-5 reveal reveal-delay-2">
        <div class="flex items-center gap-3 mb-1">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center" style="background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3);">
            <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
          </div>
          <h3 class="font-heading font-semibold text-xl text-amber-400">Ajouter une Offre d'Emploi</h3>
        </div>

        <!-- Drop zone -->
        <div
          class="min-h-[12rem] border-2 border-dashed rounded-2xl flex flex-col items-center justify-center p-8 cursor-pointer transition-all duration-300"
          :class="[
            jobDragging ? 'border-amber-500/70 bg-amber-500/10 scale-[1.01]' : 'border-white/10 hover:border-amber-500/50 hover:bg-amber-500/5',
            jobStatus === 'processing' ? 'pointer-events-none opacity-60' : ''
          ]"
          @click="$refs.jobFileInput.click()"
          @dragover.prevent="jobDragging = true"
          @dragleave.prevent="jobDragging = false"
          @drop.prevent="onJobDrop"
        >
          <input ref="jobFileInput" type="file" class="hidden" accept=".pdf,.docx,.txt" @change="onJobFile" />

          <div v-if="jobStatus === 'idle'" class="text-center">
            <svg class="w-12 h-12 mx-auto mb-3 text-amber-400/40" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <p class="text-white/80 font-medium">Glissez une offre ici ou <span class="text-amber-400 underline underline-offset-2">parcourez</span></p>
            <p class="text-text-muted text-xs mt-1">PDF, DOCX ou TXT — max 10 MB</p>
          </div>

          <div v-else-if="jobStatus === 'uploading'" class="text-center">
            <svg class="animate-spin w-10 h-10 mx-auto mb-3 text-amber-400" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            <p class="text-amber-300 text-sm font-medium">Envoi en cours…</p>
          </div>

          <div v-else-if="jobStatus === 'processing'" class="text-center">
            <div class="relative w-12 h-12 mx-auto mb-3">
              <svg class="animate-spin w-12 h-12 text-amber-500/30" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3"/></svg>
              <svg class="animate-spin w-12 h-12 text-amber-400 absolute inset-0" fill="none" viewBox="0 0 24 24" style="animation-duration:1.2s"><path class="opacity-80" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            </div>
            <p class="text-amber-300 text-sm font-medium">Analyse IA en cours…</p>
            <p class="text-text-muted text-xs mt-1">Extraction du titre, compétences, contrat…</p>
          </div>
        </div>

        <!-- Processing steps -->
        <div v-if="jobStatus === 'processing'" class="flex items-center gap-2 text-xs text-text-muted px-1">
          <span v-for="(step, i) in parsingSteps" :key="i"
            class="flex items-center gap-1 transition-all duration-500"
            :class="i <= jobStep ? 'text-amber-400' : 'text-text-muted/40'">
            <svg v-if="i < jobStep" class="w-3 h-3 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
            <svg v-else-if="i === jobStep" class="animate-spin w-3 h-3" fill="none" viewBox="0 0 24 24"><path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            <span v-else class="w-3 h-3 rounded-full border border-current inline-block"></span>
            {{ step }}
            <span v-if="i < parsingSteps.length - 1" class="mx-1 text-text-muted/30">›</span>
          </span>
        </div>

        <!-- Success -->
        <transition name="slide-up">
          <div v-if="jobResult" class="p-4 rounded-xl text-sm bg-emerald-500/10 border border-emerald-500/20">
            <div class="flex items-start gap-3">
              <div class="mt-0.5 w-8 h-8 rounded-lg bg-emerald-500/15 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              </div>
              <div class="flex-1">
                <p class="font-semibold text-emerald-300 text-sm">Offre ajoutée avec succès !</p>
                <p class="text-emerald-400/70 text-xs mt-0.5">
                  <span v-if="jobFilename">{{ jobFilename }} — </span>L'analyse IA est en cours en arrière-plan.
                </p>
              </div>
              <button @click="jobResult = null; jobStatus = 'idle'" class="text-white/30 hover:text-white/70 transition-colors">✕</button>
            </div>
          </div>
        </transition>

        <!-- Error -->
        <transition name="slide-up">
          <div v-if="jobError" class="p-4 rounded-xl text-sm bg-rose-500/10 border border-rose-500/20">
            <div class="flex items-start gap-3">
              <span class="text-rose-400 text-lg">⚠</span>
              <div class="flex-1">
                <p class="font-semibold text-rose-300 text-sm">Erreur d'upload</p>
                <p class="text-rose-400/70 text-xs mt-0.5">{{ jobError }}</p>
              </div>
              <button @click="jobError = null; jobStatus = 'idle'" class="text-white/30 hover:text-white/70 transition-colors">✕</button>
            </div>
          </div>
        </transition>
      </div>

    </div>

    <!-- Info banner -->
    <div class="mt-6 glass-card p-4 flex items-center gap-3 text-sm text-text-muted reveal reveal-delay-3">
      <svg class="w-5 h-5 text-blue-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
      <span>
        <strong class="text-white/80">Traitement asynchrone :</strong>
        L'upload est immédiat. L'extraction IA (LLM → PostgreSQL → ChromaDB) se traite en arrière-plan en quelques secondes.
        Les données apparaîtront dans <strong class="text-blue-400">Candidats</strong> et <strong class="text-amber-400">Offres</strong> une fois l'analyse terminée.
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

// ── Parsing step labels ──────────────────────────────────────────────
const parsingSteps = ['Extraction', 'Analyse LLM', 'Sauvegarde DB', 'Indexation']

// ── Candidate state ──────────────────────────────────────────────────
const candidateFileInput = ref(null)
const candidateDragging = ref(false)
const candidateStatus = ref('idle')   // 'idle' | 'uploading' | 'processing'
const candidateStep = ref(0)
const candidateResult = ref(null)
const candidateError = ref(null)
const candidateFilename = ref('')
let candidateStepTimer = null

// ── Job state ────────────────────────────────────────────────────────
const jobFileInput = ref(null)
const jobDragging = ref(false)
const jobStatus = ref('idle')
const jobStep = ref(0)
const jobResult = ref(null)
const jobError = ref(null)
const jobFilename = ref('')
let jobStepTimer = null

// ── Step animation ───────────────────────────────────────────────────
function animateSteps(stepRef, timerRef, onDone) {
  stepRef.value = 0
  let i = 0
  timerRef.value = setInterval(() => {
    i++
    if (i < parsingSteps.length) {
      stepRef.value = i
    } else {
      clearInterval(timerRef.value)
      onDone()
    }
  }, 1800)
}

// ── Candidate upload ─────────────────────────────────────────────────
async function uploadCandidate(file) {
  if (!file) return
  candidateFilename.value = file.name
  candidateStatus.value = 'uploading'
  candidateResult.value = null
  candidateError.value = null
  candidateStep.value = 0

  const formData = new FormData()
  formData.append('file', file)

  try {
    await api.post('/candidates/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    // Backend returned 200 — now animate the "processing" steps
    candidateStatus.value = 'processing'
    animateSteps(candidateStep, { value: candidateStepTimer }, () => {
      candidateResult.value = { ok: true }
      candidateStatus.value = 'idle'
    })
  } catch (err) {
    candidateError.value = err.response?.data?.detail || err.message || "Erreur d'upload"
    candidateStatus.value = 'idle'
  } finally {
    if (candidateFileInput.value) candidateFileInput.value.value = ''
  }
}

function onCandidateFile(event) { uploadCandidate(event.target.files[0]) }
function onCandidateDrop(event) {
  candidateDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) uploadCandidate(file)
}

// ── Job upload ───────────────────────────────────────────────────────
async function uploadJob(file) {
  if (!file) return
  jobFilename.value = file.name
  jobStatus.value = 'uploading'
  jobResult.value = null
  jobError.value = null
  jobStep.value = 0

  const formData = new FormData()
  formData.append('file', file)

  try {
    await api.post('/jobs/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    jobStatus.value = 'processing'
    animateSteps(jobStep, { value: jobStepTimer }, () => {
      jobResult.value = { ok: true }
      jobStatus.value = 'idle'
    })
  } catch (err) {
    jobError.value = err.response?.data?.detail || err.message || "Erreur d'upload"
    jobStatus.value = 'idle'
  } finally {
    if (jobFileInput.value) jobFileInput.value.value = ''
  }
}

function onJobFile(event) { uploadJob(event.target.files[0]) }
function onJobDrop(event) {
  jobDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) uploadJob(file)
}

// ── Scroll reveal ────────────────────────────────────────────────────
onMounted(() => {
  const obs = new IntersectionObserver(
    entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('revealed') }),
    { threshold: 0.1 }
  )
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el))
})
</script>

<style scoped>

/* ── Transition ────────────────────────────────────── */
.slide-up-enter-active { transition: all .35s cubic-bezier(.16,1,.3,1); }
.slide-up-enter-from   { transform: translateY(10px); opacity: 0; }
</style>
