import api from './api';

export const authService = {
  async login(email, password) {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    
    const response = await api.post('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  async register(email, password, fullName) {
    const response = await api.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  async getMe() {
    const response = await api.get('/auth/me');
    return response.data;
  },
};
