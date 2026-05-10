<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden bg-bg-dark">
    <!-- Background Effects -->
    <div class="absolute inset-0 z-0 overflow-hidden">
      <div class="absolute -top-1/2 -left-1/2 w-[100vw] h-[100vw] bg-primary-light/5 rounded-full blur-3xl mix-blend-screen"></div>
      <div class="absolute -bottom-1/2 -right-1/2 w-[100vw] h-[100vw] bg-accent-light/5 rounded-full blur-3xl mix-blend-screen"></div>
    </div>

    <div v-motion
         :initial="{ opacity: 0, scale: 0.95 }"
         :enter="{ opacity: 1, scale: 1, transition: { duration: 500 } }"
         class="relative z-10 w-full max-w-md p-8 glass-card rounded-3xl mx-4">
      
      <div class="text-center mb-8">
        <div class="w-16 h-16 mx-auto bg-gradient-premium rounded-2xl p-[2px] mb-6 shadow-lg shadow-primary-light/20">
          <div class="w-full h-full bg-bg-dark rounded-2xl flex items-center justify-center text-white">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>
          </div>
        </div>
        <h2 class="text-3xl font-bold text-white mb-2">Bon retour</h2>
        <p class="text-text-secondary text-sm">Connectez-vous pour accéder au Dashboard IA</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div class="space-y-2">
          <label class="text-sm font-medium text-text-secondary">Email</label>
          <input type="email" 
                 v-model="email"
                 required
                 class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-accent-light focus:ring-1 focus:ring-accent-light text-white transition-all placeholder:text-text-secondary/50"
                 placeholder="jean.dupont@entreprise.com">
        </div>

        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-text-secondary">Mot de passe</label>
            <a href="#" class="text-xs text-primary-light hover:text-white transition-colors">Mot de passe oublié ?</a>
          </div>
          <input type="password" 
                 v-model="password"
                 required
                 class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-accent-light focus:ring-1 focus:ring-accent-light text-white transition-all placeholder:text-text-secondary/50"
                 placeholder="••••••••">
        </div>

        <button type="submit" 
                class="w-full py-3 px-4 bg-gradient-premium rounded-xl text-white font-medium hover:opacity-90 transition-opacity flex items-center justify-center gap-2 glow-subtle">
          Se connecter
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" x2="3" y1="12" y2="12"/></svg>
        </button>
      </form>
      
      <div class="mt-8 text-center">
        <router-link to="/" class="text-sm text-text-secondary hover:text-white transition-colors">
          &larr; Retour à la vitrine
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')

const handleLogin = () => {
  // TODO: Call API for actual login
  console.log('Logging in with', email.value)
  // Mock login success
  router.push('/dashboard')
}
</script>
