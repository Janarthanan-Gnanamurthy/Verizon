<template>
  <div class="bg-gradient-to-br from-base-100 to-base-200 min-h-screen flex flex-col">
    <!-- Navbar -->
    <div class="navbar bg-base-100 shadow-lg sticky top-0 z-50 backdrop-blur-sm bg-opacity-90">
      <div class="container mx-auto px-4">
        <div class="flex-1">
          <router-link to="/" class="btn btn-ghost gap-2 normal-case text-xl">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84 51.13 51.13 0 0 0-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
            </svg>
            EduConnect
          </router-link>
        </div>
        <div class="flex-none">
          <label class="swap swap-rotate mx-2">
            <!-- this hidden checkbox controls the state -->
            <input type="checkbox" class="theme-controller" value="dark" />
            <!-- sun icon -->
            <svg class="swap-on fill-current w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z"/></svg>
            <!-- moon icon -->
            <svg class="swap-off fill-current w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z"/></svg>
          </label>
          <ul class="menu menu-horizontal px-1">
            <li>
              <router-link to="/" class="font-medium">Home</router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="flex-1 container mx-auto p-4">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="footer footer-center p-6 bg-base-300 text-base-content">
      <div>
        <div class="grid grid-flow-col gap-4">
          <a class="link link-hover">About</a>
          <a class="link link-hover">Privacy</a>
          <a class="link link-hover">Terms</a>
          <a class="link link-hover">Contact</a>
        </div>
        <div class="mt-4">
          <p>© 2023 EduConnect - Interactive Learning Platform</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Theme handling
const setTheme = () => {
  // Check for saved theme
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  
  // Set the checkbox state based on theme
  const themeController = document.querySelector('.theme-controller');
  if (themeController) {
    themeController.checked = savedTheme === 'dark';
  }
};

// Add event listener for theme changes
const setupThemeListener = () => {
  const themeController = document.querySelector('.theme-controller');
  if (themeController) {
    themeController.addEventListener('change', (e) => {
      const newTheme = e.target.checked ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    });
  }
};

// Set theme on mount
import { onMounted } from 'vue';

onMounted(() => {
  setTheme();
  setupThemeListener();
});
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body {
  font-family: 'Inter', system-ui, sans-serif;
}
</style> 