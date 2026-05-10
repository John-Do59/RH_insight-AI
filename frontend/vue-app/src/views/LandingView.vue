<template>
  <div class="relative min-h-screen flex flex-col items-center justify-center overflow-hidden">
    
    <!-- Background Effects -->
    <div class="absolute inset-0 z-0">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-light/10 rounded-full blur-3xl mix-blend-screen animate-pulse"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-light/10 rounded-full blur-3xl mix-blend-screen animate-pulse" style="animation-delay: 2s;"></div>
    </div>

    <!-- Main Content -->
    <main class="relative z-10 flex flex-col items-center text-center px-6 max-w-4xl mx-auto mt-20">
      
      <!-- Premium Badge -->
      <div v-motion
           :initial="{ opacity: 0, y: 20 }"
           :enter="{ opacity: 1, y: 0, transition: { duration: 800 } }"
           class="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 backdrop-blur-md mb-8">
        <span class="w-2 h-2 rounded-full bg-accent animate-pulse"></span>
        <span class="text-sm font-medium tracking-wide text-text-secondary">AI-Powered Recruitment</span>
      </div>

      <!-- Hero Heading -->
      <h1 v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 800, delay: 200 } }"
          class="text-5xl md:text-7xl font-bold mb-6 tracking-tight">
        L'intelligence artificielle au service du <span class="text-gradient-premium">recrutement</span>
      </h1>
      
      <p v-motion
         :initial="{ opacity: 0, y: 30 }"
         :enter="{ opacity: 1, y: 0, transition: { duration: 800, delay: 400 } }"
         class="text-lg md:text-xl text-text-secondary mb-12 max-w-2xl leading-relaxed">
        Analysez les CV, croisez les données GitHub et interrogez notre base de données grâce à un assistant IA nouvelle génération conçu pour les professionnels RH.
      </p>

      <!-- CTA Buttons -->
      <div v-motion
           :initial="{ opacity: 0, scale: 0.9 }"
           :enter="{ opacity: 1, scale: 1, transition: { duration: 500, delay: 600 } }"
           class="flex flex-col sm:flex-row gap-6">
        
        <router-link to="/auth" class="group relative px-8 py-4 rounded-xl font-semibold text-white transition-all duration-300 hover:scale-105">
          <div class="absolute inset-0 w-full h-full bg-gradient-premium rounded-xl opacity-90 group-hover:opacity-100 transition-opacity"></div>
          <div class="absolute inset-0 w-full h-full rounded-xl glow-subtle opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <span class="relative flex items-center gap-2">
            Accéder au Dashboard
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:translate-x-1 transition-transform"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </span>
        </router-link>
        
        <a href="#features" class="px-8 py-4 rounded-xl font-medium text-text-primary bg-white/5 border border-white/10 hover:bg-white/10 transition-colors backdrop-blur-md">
          Découvrir les fonctionnalités
        </a>
      </div>
    </main>

    <!-- Features Section (Simplified) -->
    <section id="features" class="relative z-10 w-full max-w-6xl mx-auto px-6 py-32 mt-20">
      <div class="grid md:grid-cols-3 gap-8">
        
        <div v-motion
             :initial="{ opacity: 0, y: 50 }"
             :visible="{ opacity: 1, y: 0, transition: { duration: 600 } }"
             class="glass-card p-8 rounded-2xl group hover:glow-subtle transition-all duration-500">
          <div class="w-12 h-12 rounded-lg bg-primary-light/20 flex items-center justify-center mb-6 text-primary-light">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg>
          </div>
          <h3 class="text-xl font-semibold mb-3 text-white">Analyse RAG Avancée</h3>
          <p class="text-text-secondary text-sm leading-relaxed">Recherche sémantique instantanée dans les CV et documents RH avec compréhension du contexte.</p>
        </div>

        <div v-motion
             :initial="{ opacity: 0, y: 50 }"
             :visible="{ opacity: 1, y: 0, transition: { duration: 600, delay: 100 } }"
             class="glass-card p-8 rounded-2xl group hover:glow-blue transition-all duration-500">
          <div class="w-12 h-12 rounded-lg bg-accent/20 flex items-center justify-center mb-6 text-accent-light">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>
          </div>
          <h3 class="text-xl font-semibold mb-3 text-white">Bases SQL & Métadonnées</h3>
          <p class="text-text-secondary text-sm leading-relaxed">Interrogation naturelle de bases de données relationnelles pour trouver les candidats parfaits.</p>
        </div>

        <div v-motion
             :initial="{ opacity: 0, y: 50 }"
             :visible="{ opacity: 1, y: 0, transition: { duration: 600, delay: 200 } }"
             class="glass-card p-8 rounded-2xl group hover:glow-subtle transition-all duration-500">
          <div class="w-12 h-12 rounded-lg bg-white/10 flex items-center justify-center mb-6 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
          </div>
          <h3 class="text-xl font-semibold mb-3 text-white">Insights GitHub</h3>
          <p class="text-text-secondary text-sm leading-relaxed">Analyse des dépôts techniques et des langages maîtrisés pour valider les compétences des développeurs.</p>
        </div>

      </div>
    </section>

  </div>
</template>

<script setup>
// Landing page component
</script>
