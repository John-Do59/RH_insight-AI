import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import LandingView from '../views/LandingView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },
    {
      path: '/auth',
      name: 'auth',
      component: () => import('../views/AuthView.vue'),
      meta: { guest: true },
    },
    {
      // Dashboard shell (sidebar + topbar) — all protected pages live here
      path: '/',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('../views/OverviewView.vue'),
        },
        {
          path: 'candidates',
          name: 'candidates',
          component: () => import('../views/CandidatesView.vue'),
        },
        {
          path: 'jobs',
          name: 'jobs',
          component: () => import('../views/JobsView.vue'),
        },
        {
          path: 'job-agent',
          name: 'job-agent',
          component: () => import('../views/JobAgentView.vue'),
        },
        {
          path: 'ingestion',
          name: 'ingestion',
          component: () => import('../views/DataIngestionView.vue'),
        },
        {
          path: 'chat',
          name: 'chat',
          component: () => import('../views/ChatView.vue'),
        },
      ],
    },
  ],
});

router.beforeEach(async (to, from) => {
  const authStore = useAuthStore();

  if (authStore.token && !authStore.user) {
    await authStore.fetchUser();
  }

  const isAuthenticated = authStore.isAuthenticated;

  if (to.meta.requiresAuth && !isAuthenticated) {
    return { name: 'auth' };
  } else if (to.meta.guest && isAuthenticated) {
    return { name: 'dashboard' };
  }
});

export default router;
