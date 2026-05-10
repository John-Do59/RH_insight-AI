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
        <h2 class="text-3xl font-bold text-white mb-2">{{ isLogin ? 'Bon retour' : 'Rejoindre RH Insight' }}</h2>
        <p class="text-text-secondary text-sm">{{ isLogin ? 'Connectez-vous pour accéder au Dashboard IA' : 'Créez un compte pour commencer l\'analyse de vos candidats' }}</p>
      </div>

      <!-- Error Message -->
      <div v-if="authStore.error" class="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm text-center">
        {{ authStore.error }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-5">
        <!-- Full Name (Only for Register) -->
        <div v-if="!isLogin" class="space-y-2">
          <label class="text-sm font-medium text-text-secondary">Nom complet</label>
          <input type="text" 
                 v-model="fullName"
                 required
                 class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-accent-light focus:ring-1 focus:ring-accent-light text-white transition-all placeholder:text-text-secondary/50"
                 placeholder="Amaury Dupont">
        </div>

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
            <a v-if="isLogin" href="#" class="text-xs text-primary-light hover:text-white transition-colors">Mot de passe oublié ?</a>
          </div>
          <input type="password" 
                 v-model="password"
                 required
                 class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-accent-light focus:ring-1 focus:ring-accent-light text-white transition-all placeholder:text-text-secondary/50"
                 placeholder="••••••••">
        </div>

        <button type="submit" 
                :disabled="authStore.loading"
                class="w-full py-3 px-4 bg-gradient-premium rounded-xl text-white font-medium hover:opacity-90 transition-opacity flex items-center justify-center gap-2 glow-subtle disabled:opacity-50 disabled:cursor-not-allowed mt-2">
          <span v-if="authStore.loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          <span v-else>{{ isLogin ? 'Se connecter' : 'Créer un compte' }}</span>
          <svg v-if="!authStore.loading" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" x2="3" y1="12" y2="12"/></svg>
        </button>
      </form>
      
      <div class="mt-6 text-center space-y-4">
        <p class="text-sm text-text-secondary">
          {{ isLogin ? "Pas encore de compte ?" : "Déjà un compte ?" }}
          <button @click="isLogin = !isLogin" class="text-primary-light hover:text-white font-medium transition-colors ml-1">
            {{ isLogin ? "S'inscrire" : "Se connecter" }}
          </button>
        </p>
        
        <router-link to="/" class="block text-sm text-text-secondary hover:text-white transition-colors">
          &larr; Retour à la vitrine
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isLogin = ref(true)
const email = ref('')
const password = ref('')
const fullName = ref('')

const handleSubmit = async () => {
  let success = false
  if (isLogin.value) {
    success = await authStore.login(email.value, password.value)
  } else {
    success = await authStore.register(email.value, password.value, fullName.value)
  }
  
  if (success) {
    router.push('/dashboard')
  }
}
</script>
