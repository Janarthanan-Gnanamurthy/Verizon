<template>
  <div>
    <!-- Hero Section -->
    <div class="hero bg-base-200 rounded-box my-8 overflow-hidden shadow-xl">
      <div class="hero-content flex-col lg:flex-row-reverse p-0">
        <img src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80" 
             class="lg:max-w-md rounded-r-box h-full object-cover" alt="Learning with technology" />
        <div class="p-8 lg:p-12">
          <div class="badge badge-accent mb-2">Live Learning</div>
          <h1 class="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text">
            Interactive Education Platform
          </h1>
          <p class="py-6 text-lg">
            Connect with teachers and peers in real-time. Experience AI-enhanced learning with 
            live transcriptions, smart summaries, and seamless video conferencing.
          </p>
          
          <div class="flex flex-wrap gap-4 items-center">
            <div class="tooltip" data-tip="Video Calls">
              <div class="badge badge-lg p-4 gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
                </svg>
              </div>
            </div>
            <div class="tooltip" data-tip="AI Summaries">
              <div class="badge badge-lg p-4 gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                </svg>
              </div>
            </div>
            <div class="tooltip" data-tip="Live Transcription">
              <div class="badge badge-lg p-4 gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Session Creation Card -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 my-8">
      <div class="card bg-base-100 shadow-xl overflow-hidden">
        <div class="card-body">
          <div class="flex items-center gap-3 mb-4">
            <div class="avatar placeholder">
              <div class="bg-primary text-primary-content rounded-full w-12">
                <span class="text-2xl">➕</span>
              </div>
            </div>
            <h2 class="card-title text-2xl text-black">Create New Session</h2>
          </div>
          <form @submit.prevent="createRoom" class="space-y-4">
            <div class="form-control">
              <label class="label">
                <span class="label-text font-medium text-black">Session Name</span>
              </label>
              <input 
                type="text" 
                v-model="roomName" 
                placeholder="Enter a name for your session" 
                class="input input-bordered w-full" 
                required
              />
              <label class="label">
                <span class="label-text-alt text-base-content/60">Choose a descriptive name for your learning session</span>
              </label>
            </div>

            <div class="form-control">
              <label class="label">
                <span class="label-text font-medium text-black">Your Name</span>
              </label>
              <input 
                type="text" 
                v-model="hostName" 
                placeholder="Enter your name" 
                class="input input-bordered w-full" 
                required
              />
              <label class="label">
                <span class="label-text-alt text-base-content/60">This is how others will identify you</span>
              </label>
            </div>

            <div class="form-control mt-6">
              <button type="submit" class="btn btn-primary">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                </svg>
                Start New Session
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Join Existing Session Card -->
      <div class="card bg-base-100 shadow-xl overflow-hidden">
        <div class="card-body">
          <div class="flex items-center gap-3 mb-2">
            <div class="avatar placeholder">
              <div class="bg-secondary text-secondary-content rounded-full w-12">
                <span class="text-2xl">🔍</span>
              </div>
            </div>
            <h2 class="card-title text-2xl">Join Existing Sessions</h2>
          </div>
          
          <div v-if="rooms.length > 0" class="overflow-x-auto mt-2">
            <table class="table table-zebra">
              <thead>
                <tr>
                  <th>Session</th>
                  <th>Host</th>
                  <th class="text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="room in rooms" :key="room.id" class="hover">
                  <td class="font-medium">{{ room.name }}</td>
                  <td>{{ room.host_id }}</td>
                  <td class="text-right">
                    <button @click="joinRoom(room.id)" class="btn btn-secondary btn-sm">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-1">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
                      </svg>
                      Join
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-else class="alert alert-info shadow-lg my-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current flex-shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <div>
              <h3 class="font-bold">No Active Sessions</h3>
              <div class="text-xs">Create a new session to get started!</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="my-12">
      <h2 class="text-2xl font-bold text-center mb-8">Platform Features</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Feature 1 -->
        <div class="card bg-base-100 shadow-lg hover:shadow-xl transition-all">
          <div class="card-body">
            <div class="flex justify-center mb-4">
              <div class="rounded-full bg-primary/10 p-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10 text-primary">
                  <path stroke-linecap="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
                </svg>
              </div>
            </div>
            <h2 class="card-title justify-center">HD Video Conferencing</h2>
            <p class="text-center">Connect face-to-face with crystal clear video and audio quality for an immersive learning experience.</p>
          </div>
        </div>
        
        <!-- Feature 2 -->
        <div class="card bg-base-100 shadow-lg hover:shadow-xl transition-all">
          <div class="card-body">
            <div class="flex justify-center mb-4">
              <div class="rounded-full bg-secondary/10 p-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10 text-secondary">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
                </svg>
              </div>
            </div>
            <h2 class="card-title justify-center">Live Transcription</h2>
            <p class="text-center">Never miss a word with our real-time speech-to-text technology, making content more accessible.</p>
          </div>
        </div>
        
        <!-- Feature 3 -->
        <div class="card bg-base-100 shadow-lg hover:shadow-xl transition-all">
          <div class="card-body">
            <div class="flex justify-center mb-4">
              <div class="rounded-full bg-accent/10 p-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10 text-accent">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                </svg>
              </div>
            </div>
            <h2 class="card-title justify-center">AI-Powered Summaries</h2>
            <p class="text-center">Instantly generate intelligent summaries of discussions, highlighting key points and concepts.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const roomName = ref('');
const hostName = ref('');
const rooms = ref([]);

// Load saved username if available
onMounted(() => {
  const savedName = localStorage.getItem('username');
  if (savedName) {
    hostName.value = savedName;
  }
  
  loadRooms();
});

async function loadRooms() {
  try {
    const response = await axios.get('/api/rooms/');
    rooms.value = response.data.rooms;
  } catch (error) {
    console.error('Failed to fetch rooms:', error);
  }
}

async function createRoom() {
  try {
    // Save username to localStorage
    localStorage.setItem('username', hostName.value);
    
    const response = await axios.post('/api/rooms/', {
      name: roomName.value,
      host_id: hostName.value
    });
    
    const roomId = response.data.room_id;
    router.push(`/room/${roomId}`);
  } catch (error) {
    console.error('Failed to create room:', error);
  }
}

function joinRoom(roomId) {
  // Save username before joining
  if (hostName.value) {
    localStorage.setItem('username', hostName.value);
  }
  router.push(`/room/${roomId}`);
}
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-secondary {
  background-color: #2ecc71;
  color: white;
}

.room-list {
  list-style: none;
}

.room-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.room-info {
  display: flex;
  flex-direction: column;
}
</style> 