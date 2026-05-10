import { useAuthStore } from '../stores/auth';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const chatService = {
  async streamMessage(question, history = [], onToken) {
    const authStore = useAuthStore();
    const token = authStore.token;

    const response = await fetch(`${API_URL}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        question,
        history
      })
    });

    if (!response.ok) {
      throw new Error('Failed to stream message');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let done = false;

    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      const chunkValue = decoder.decode(value);
      if (chunkValue) {
        onToken(chunkValue);
      }
    }
  }
};
