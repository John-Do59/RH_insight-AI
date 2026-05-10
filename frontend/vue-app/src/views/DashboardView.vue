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
          <span class="font-heading font-bold text-lg tracking-tight text-white">RH Insight</span>
        </div>
      </div>
      
      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto py-6 px-4 space-y-1">
        <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-white/5 text-white font-medium border border-white/5">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-accent-light"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          AI Chat
        </a>
        <!-- Other Nav Items (Placeholder) -->
      </nav>
      
      <!-- User Profile -->
      <div class="p-4 border-t border-white/5">
        <div @click="handleLogout" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-red-500/10 cursor-pointer transition-colors group">
          <div class="w-8 h-8 rounded-full bg-surface border border-white/10 flex items-center justify-center text-sm font-medium text-white group-hover:border-red-500/20">
            {{ userInitials }}
          </div>
          <div class="flex-1 overflow-hidden">
            <p class="text-sm font-medium text-white truncate group-hover:text-red-400">{{ userName }}</p>
            <p class="text-xs text-text-secondary truncate">Déconnexion</p>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-text-secondary group-hover:text-red-400"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>
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
      </header>

      <!-- Chat History -->
      <div class="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth" ref="chatContainer">
        
        <!-- Welcome Message -->
        <div v-if="messages.length === 0" class="h-full flex flex-col items-center justify-center text-center max-w-2xl mx-auto">
          <div class="w-16 h-16 rounded-2xl bg-gradient-premium p-[1px] mb-6 shadow-lg shadow-accent/20">
            <div class="w-full h-full bg-bg-dark rounded-2xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-accent-light"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>
            </div>
          </div>
          <h2 class="text-2xl font-bold mb-2 text-white">Comment puis-je vous aider, {{ userName }} ?</h2>
          <p class="text-text-secondary mb-8">Posez des questions sur les candidats ou analysez les données RH.</p>
        </div>

        <!-- Messages -->
        <div v-for="(msg, index) in messages" :key="index" 
             class="flex gap-4" 
             :class="msg.role === 'user' ? 'flex-row-reverse' : ''">
          
          <!-- Avatar -->
          <div class="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center"
               :class="msg.role === 'user' ? 'bg-surface border border-white/10' : 'bg-gradient-premium'">
            <span v-if="msg.role === 'user'" class="text-xs font-medium text-white">{{ userInitials }}</span>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>
          </div>

          <!-- Bubble -->
          <div class="max-w-[80%] rounded-2xl px-5 py-3.5 text-sm leading-relaxed"
               :class="msg.role === 'user' ? 'bg-primary-light text-white rounded-tr-sm' : 'glass-card border border-white/5 rounded-tl-sm text-text-primary'">
            <div class="whitespace-pre-wrap">{{ msg.content }}</div>
            
            <!-- Metadata for assistant responses -->
            <div v-if="msg.role === 'assistant' && msg.sources && msg.sources.length" class="mt-3 pt-3 border-t border-white/5 flex flex-wrap gap-2">
              <span v-for="source in msg.sources" :key="source" class="px-2 py-0.5 rounded bg-white/5 text-[10px] text-text-secondary uppercase tracking-wider font-bold">
                {{ source }}
              </span>
            </div>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="flex gap-4">
          <div class="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center bg-gradient-premium">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>
          </div>
          <div class="glass-card border border-white/5 rounded-2xl rounded-tl-sm px-5 py-3.5">
            <div class="flex gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-text-secondary animate-bounce" style="animation-delay: 0ms"></span>
              <span class="w-1.5 h-1.5 rounded-full bg-text-secondary animate-bounce" style="animation-delay: 150ms"></span>
              <span class="w-1.5 h-1.5 rounded-full bg-text-secondary animate-bounce" style="animation-delay: 300ms"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="p-6 bg-bg-darker/80 backdrop-blur-md">
        <div class="max-w-4xl mx-auto relative">
          <form @submit.prevent="handleSendMessage" class="relative group">
            <div class="absolute -inset-1 bg-gradient-premium rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
            <div class="relative flex items-end gap-2 bg-surface border border-white/10 rounded-2xl p-2 focus-within:border-accent-light/50 transition-colors">
              <textarea v-model="inputText"
                        @keydown.enter.prevent="handleSendMessage"
                        placeholder="Posez votre question à RH Insight..." 
                        class="w-full bg-transparent text-white border-none focus:ring-0 resize-none py-2 px-2 max-h-32 focus:outline-none placeholder:text-text-secondary/50 text-sm"
                        rows="1"></textarea>
              
              <button type="submit" 
                      :disabled="!inputText.trim() || isTyping"
                      class="p-2 bg-gradient-premium rounded-xl text-white hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed glow-subtle">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onUpdated, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { chatService } from '../services/chat'

const router = useRouter()
const authStore = useAuthStore()
const chatContainer = ref(null)

const inputText = ref('')
const messages = ref([])
const isTyping = ref(false)

const userName = computed(() => authStore.user?.full_name || 'Utilisateur')
const userInitials = computed(() => {
  const name = userName.value
  return name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2)
})

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

onUpdated(() => {
  scrollToBottom()
})

const handleLogout = () => {
  authStore.logout()
  router.push('/auth')
}

const handleSendMessage = async () => {
  if (!inputText.value.trim() || isTyping.value) return

  const question = inputText.value
  messages.value.push({ role: 'user', content: question })
  inputText.value = ''
  isTyping.value = true

  // Add an empty assistant message to fill with tokens
  const messageIndex = messages.value.push({
    role: 'assistant',
    content: '',
    sources: ['streaming...']
  }) - 1

  try {
    const history = messages.value.slice(0, -2) // Exclude current user msg and empty assistant msg
    
    await chatService.streamMessage(question, history, (token) => {
      isTyping.value = false // Hide typing indicator once we start receiving tokens
      messages.value[messageIndex].content += token
      nextTick(() => scrollToBottom())
    })
    
    // Finalize message (remove 'streaming...' tag)
    messages.value[messageIndex].sources = ['finalized']
    
  } catch (err) {
    console.error('Chat error:', err)
    messages.value[messageIndex].content = "Désolé, une erreur est survenue lors de la communication avec le serveur."
    messages.value[messageIndex].sources = ['error']
  } finally {
    isTyping.value = false
    nextTick(() => scrollToBottom())
  }
}
</script>
