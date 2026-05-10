import api from './api';

export const chatService = {
  async sendMessage(question, history = []) {
    const response = await api.post('/chat/', {
      question,
      history,
    });
    return response.data;
  },
};
