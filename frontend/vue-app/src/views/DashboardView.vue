<template>
  <div class="flex h-screen bg-bg-darker text-text-primary overflow-hidden">
    
    <!-- Sidebar -->
    <aside class="w-64 flex-shrink-0 bg-bg-dark border-r border-white/5 flex flex-col z-20">
      <!-- Logo Area -->
      <div class="h-16 flex items-center px-6 border-b border-white/5">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-gradient-premium flex items-center justify-center glow-subtle">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>
          </div>
          <span class="font-heading font-bold text-lg tracking-tight">RH Insight</span>
        </div>
      </div>
      
      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto py-6 px-4 space-y-1">
        <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-white/5 text-white font-medium border border-white/5">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-accent-light"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          AI Chat
        </a>
        <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-secondary hover:text-white hover:bg-white/5 transition-all group">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:text-primary-light transition-colors"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Candidates
        </a>
        <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-secondary hover:text-white hover:bg-white/5 transition-all group">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:text-primary-light transition-colors"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>
          Analytics
        </a>
        <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-secondary hover:text-white hover:bg-white/5 transition-all group">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:text-primary-light transition-colors"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
          GitHub Insights
        </a>
      </nav>
      
      <!-- User Profile -->
      <div class="p-4 border-t border-white/5">
        <div class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 cursor-pointer transition-colors">
          <div class="w-8 h-8 rounded-full bg-surface border border-white/10 flex items-center justify-center text-sm font-medium">
            JD
          </div>
          <div class="flex-1 overflow-hidden">
            <p class="text-sm font-medium text-white truncate">Jean Dupont</p>
            <p class="text-xs text-text-secondary truncate">Admin</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Chat Area -->
    <main class="flex-1 flex flex-col relative">
      <!-- Topbar -->
      <header class="h-16 flex items-center justify-between px-6 border-b border-white/5 bg-bg-dark/50 backdrop-blur-sm z-10">
        <div class="flex items-center gap-2">
          <span class="flex items-center gap-2 px-2.5 py-1 rounded-md bg-accent/10 border border-accent/20 text-xs font-medium text-accent-light">
            <span class="w-1.5 h-1.5 rounded-full bg-accent-light animate-pulse"></span>
            DeepSeek-R1 Active
          </span>
        </div>
        <div class="flex items-center gap-4">
          <button class="text-text-secondary hover:text-white transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
          </button>
        </div>
      </header>

      <!-- Chat History -->
      <div class="flex-1 overflow-y-auto p-6 space-y-6">
        
        <!-- Welcome Message -->
        <div v-if="messages.length === 0" class="h-full flex flex-col items-center justify-center text-center max-w-2xl mx-auto">
          <div class="w-16 h-16 rounded-2xl bg-gradient-premium p-[1px] mb-6 shadow-lg shadow-accent/20">
            <div class="w-full h-full bg-bg-dark rounded-2xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-accent-light"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>
            </div>
          </div>
          <h2 class="text-2xl font-bold mb-2">Comment puis-je vous aider ?</h2>
          <p class="text-text-secondary mb-8">Posez des questions sur les candidats, analysez des CVs, ou cherchez des profils GitHub spécifiques.</p>
          
          <div class="grid grid-cols-2 gap-4 w-full">
            <button class="text-left p-4 rounded-xl glass-card hover:bg-white/10 hover:border-white/20 transition-all group">
              <span class="block text-sm font-medium text-white mb-1 group-hover:text-primary-light transition-colors">Trouver un Dev Vue.js</span>
              <span class="block text-xs text-text-secondary">Rechercher dans la base de données...</span>
            </button>
            <button class="text-left p-4 rounded-xl glass-card hover:bg-white/10 hover:border-white/20 transition-all group">
              <span class="block text-sm font-medium text-white mb-1 group-hover:text-accent-light transition-colors">Analyser le CV de Paul</span>
              <span class="block text-xs text-text-secondary">Extraire les compétences clés...</span>
            </button>
          </div>
        </div>

        <!-- Messages -->
        <div v-for="(msg, index) in messages" :key="index" 
             class="flex gap-4" 
             :class="msg.role === 'user' ? 'flex-row-reverse' : ''">
          
          <!-- Avatar -->
          <div class="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center"
               :class="msg.role === 'user' ? 'bg-surface border border-white/10' : 'bg-gradient-premium'">
            <span v-if="msg.role === 'user'" class="text-xs font-medium">JD</span>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>
          </div>

          <!-- Bubble -->
          <div class="max-w-[80%] rounded-2xl px-5 py-3.5 text-sm leading-relaxed"
               :class="msg.role === 'user' ? 'bg-primary-light text-white rounded-tr-sm' : 'glass-card border border-white/5 rounded-tl-sm text-text-primary'">
            {{ msg.content }}
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="p-6 bg-bg-darker/80 backdrop-blur-md">
        <div class="max-w-4xl mx-auto relative">
          <form @submit.prevent="sendMessage" class="relative group">
            <div class="absolute -inset-1 bg-gradient-premium rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
            <div class="relative flex items-end gap-2 bg-surface border border-white/10 rounded-2xl p-2 focus-within:border-accent-light/50 transition-colors">
              <button type="button" class="p-2 text-text-secondary hover:text-white transition-colors rounded-lg hover:bg-white/5">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
              </button>
              
              <textarea v-model="inputText"
                        @keydown.enter.prevent="sendMessage"
                        placeholder="Posez votre question à RH Insight..." 
                        class="w-full bg-transparent text-white border-none focus:ring-0 resize-none py-2 px-2 max-h-32 focus:outline-none placeholder:text-text-secondary/50 text-sm"
                        rows="1"></textarea>
              
              <button type="submit" 
                      :disabled="!inputText.trim()"
                      class="p-2 bg-gradient-premium rounded-xl text-white hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed glow-subtle">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
              </button>
            </div>
          </form>
          <div class="text-center mt-2">
            <p class="text-xs text-text-secondary">L'IA peut faire des erreurs. Vérifiez toujours les informations importantes.</p>
          </div>
        </div>
      </div>
    </main>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const inputText = ref('')
const messages = ref([])

const sendMessage = () => {
  if (!inputText.value.trim()) return

  // Add user message
  messages.value.push({
    role: 'user',
    content: inputText.value
  })

  const query = inputText.value
  inputText.value = ''

  // Simulate AI Response (To be replaced with actual API call)
  setTimeout(() => {
    messages.value.push({
      role: 'assistant',
      content: "Je suis connecté à la nouvelle interface. L'intégration de l'API FastAPI et de l'architecture async est en cours de développement."
    })
  }, 1000)
}
</script>
