<template>
  <div class="page-container h-full flex flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h2 class="section-title">Assistant RH IA</h2>
      <p class="section-subtitle">Posez vos questions sur le recrutement ou le matching.</p>
    </div>

    <!-- Chat Box -->
    <div class="flex-1 flex flex-col glass-card overflow-hidden">
      <!-- Messages Area -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="messagesContainer">
        <div v-for="(msg, idx) in messages" :key="idx" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
          <div 
            class="max-w-[80%] rounded-2xl px-4 py-3 text-sm"
            :class="msg.role === 'user' ? 'bg-blue-600/80 text-white rounded-br-none' : 'bg-white/10 text-white rounded-bl-none'"
          >
            {{ msg.content }}
          </div>
        </div>
        <div v-if="isLoading" class="flex justify-start">
          <div class="max-w-[80%] rounded-2xl rounded-bl-none px-4 py-3 bg-white/10 text-white text-sm flex items-center gap-2">
            <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Réflexion en cours...
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="p-4 border-t border-white/5 bg-white/5">
        <form @submit.prevent="sendMessage" class="flex gap-2">
          <input 
            v-model="newMessage" 
            type="text" 
            placeholder="Écrivez votre message..." 
            class="flex-1 glass-input py-2 px-4 rounded-xl"
            :disabled="isLoading"
          />
          <button 
            type="submit" 
            class="glass-btn glass-btn--primary px-4 rounded-xl flex items-center justify-center"
            :disabled="isLoading || !newMessage.trim()"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';

const messagesContainer = ref(null);
const messages = ref([
  { role: 'assistant', content: 'Bonjour ! Je suis votre assistant RH intelligent. Comment puis-je vous aider aujourd\'hui ?' }
]);
const newMessage = ref('');
const isLoading = ref(false);

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const sendMessage = async () => {
  const text = newMessage.value.trim();
  if (!text) return;

  messages.value.push({ role: 'user', content: text });
  newMessage.value = '';
  isLoading.value = true;
  await scrollToBottom();

  try {
    const token = localStorage.getItem('token');
    
    // We send request as simple JSON and process the stream
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        question: text,
        history: messages.value.map(m => ({ 
          role: m.role, 
          content: m.content 
        }))
      })
    });

    if (!response.ok) throw new Error("Erreur réseau");

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    
    messages.value.push({ role: 'assistant', content: '' });
    const lastIdx = messages.value.length - 1;
    isLoading.value = false;

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      messages.value[lastIdx].content += chunk;
      await scrollToBottom();
    }
  } catch (error) {
    console.error("Chat error:", error);
    messages.value.push({ role: 'assistant', content: "Désolé, une erreur s'est produite lors de la communication avec l'IA." });
  } finally {
    isLoading.value = false;
    await scrollToBottom();
  }
};
</script>
