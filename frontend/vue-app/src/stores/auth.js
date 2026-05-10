import { defineStore } from 'pinia';
import { authService } from '../services/auth';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email, password) {
      this.loading = true;
      this.error = null;
      try {
        const data = await authService.login(email, password);
        this.token = data.access_token;
        localStorage.setItem('token', this.token);
        await this.fetchUser();
        return true;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Erreur lors de la connexion';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async register(email, password, fullName) {
      this.loading = true;
      this.error = null;
      try {
        await authService.register(email, password, fullName);
        return await this.login(email, password);
      } catch (err) {
        this.error = err.response?.data?.detail || "Erreur lors de l'inscription";
        return false;
      } finally {
        this.loading = false;
      }
    },

    async fetchUser() {
      if (!this.token) return;
      try {
        this.user = await authService.getMe();
      } catch (err) {
        this.logout();
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('token');
    },
  },
});
