import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createPinia } from 'pinia';
import App from './App.vue';
import Home from './views/Home.vue';
import Room from './views/Room.vue';
import QuizView from './views/QuizView.vue';
import ArchiveView from './views/ArchiveView.vue';
import './assets/tailwind.css';

// Create router
const routes = [
  { path: '/', component: Home },
  { path: '/room/:roomId', component: Room },
  { path: '/quiz/:roomId', component: QuizView },
  { path: '/archives', component: ArchiveView }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Create pinia store
const pinia = createPinia();

// Create and mount the app
const app = createApp(App);
app.use(router);
app.use(pinia);
app.mount('#app'); 