<template>
  <div class="min-h-screen bg-bg-dark text-text-primary selection:bg-accent-light/30">
    <router-view />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
/* We use Tailwind v4 in style.css, but we can also add global transitions here */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
