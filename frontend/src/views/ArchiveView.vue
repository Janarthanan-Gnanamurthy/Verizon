<template>
  <div class="container mx-auto p-4">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold mb-2">Archived Sessions</h1>
      <p class="text-gray-600">View past session recordings stored with Fluvio</p>
    </div>

    <!-- Room selection -->
    <div class="mb-8">
      <div class="form-control w-full max-w-md mx-auto">
        <label class="label">
          <span class="label-text">Select a room</span>
        </label>
        <select class="select select-bordered" v-model="selectedRoomId" @change="loadArchiveData">
          <option disabled value="">Select a room</option>
          <option v-for="room in rooms" :key="room.id" :value="room.id">
            {{ room.name }} ({{ formatDate(room.created_at) }})
          </option>
        </select>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center my-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else-if="selectedRoomId">
      <!-- Tabs for transcriptions and video -->
      <div class="tabs tabs-boxed justify-center mb-6">
        <a class="tab" :class="{ 'tab-active': activeTab === 'transcriptions' }" @click="activeTab = 'transcriptions'">
          Transcriptions
        </a>
        <a class="tab" :class="{ 'tab-active': activeTab === 'video' }" @click="activeTab = 'video'">
          Video Frames
        </a>
        <a class="tab" :class="{ 'tab-active': activeTab === 'quiz' }" @click="activeTab = 'quiz'">
          Quiz Results
        </a>
      </div>

      <!-- Transcriptions tab -->
      <div v-if="activeTab === 'transcriptions' && transcriptions.length > 0" class="mb-8">
        <div class="bg-base-200 p-4 rounded-lg mb-4">
          <h2 class="text-xl font-bold mb-4">Transcriptions</h2>
          <div class="space-y-4">
            <div v-for="(item, index) in transcriptions" :key="index" class="card bg-base-100 shadow-sm">
              <div class="card-body">
                <div class="flex justify-between items-start mb-2">
                  <span class="text-sm text-gray-500">{{ formatDateTime(item.metadata.timestamp) }}</span>
                  <span class="badge">User: {{ item.metadata.user_id }}</span>
                </div>
                <p>{{ item.frame_data }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- AI Summary -->
        <div v-if="aiSummary" class="card bg-primary text-primary-content">
          <div class="card-body">
            <h3 class="card-title">AI Summary</h3>
            <div v-html="formatSummary(aiSummary)"></div>
          </div>
        </div>
      </div>

      <!-- Video frames tab -->
      <div v-else-if="activeTab === 'video' && videoFrames.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="(frame, index) in videoFrames" :key="index" class="card bg-base-100 shadow-md">
          <figure class="px-4 pt-4">
            <img :src="frame.frame_data" alt="Video frame" class="rounded-lg" />
          </figure>
          <div class="card-body pt-2">
            <p class="text-sm text-gray-500">{{ formatDateTime(frame.metadata.timestamp) }}</p>
            <p class="text-sm">User: {{ frame.metadata.user_id }}</p>
          </div>
        </div>
      </div>

      <!-- Quiz results tab -->
      <div v-else-if="activeTab === 'quiz' && quiz">
        <div class="card bg-base-100 shadow-lg">
          <div class="card-body">
            <h2 class="card-title">Quiz Questions</h2>
            
            <div v-for="(question, qIndex) in quiz.questions" :key="qIndex" class="mb-6">
              <div class="font-medium mb-2">{{ qIndex + 1 }}. {{ question.question }}</div>
              
              <div class="space-y-2 ml-4">
                <div 
                  v-for="(option, oIndex) in question.options" 
                  :key="oIndex"
                  class="flex items-start"
                >
                  <div 
                    class="w-6 h-6 flex items-center justify-center rounded-full mr-2"
                    :class="{
                      'bg-success text-success-content': oIndex === question.correctOptionIndex,
                      'bg-base-300': oIndex !== question.correctOptionIndex
                    }"
                  >
                    {{ String.fromCharCode(65 + oIndex) }}
                  </div>
                  <div>{{ option }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No data states -->
      <div v-else-if="activeTab === 'transcriptions' && transcriptions.length === 0" class="alert alert-info">
        No transcriptions found for this session.
      </div>
      
      <div v-else-if="activeTab === 'video' && videoFrames.length === 0" class="alert alert-info">
        No video frames found for this session.
      </div>
      
      <div v-else-if="activeTab === 'quiz' && !quiz" class="alert alert-info">
        No quiz data found for this session.
      </div>
    </div>

    <div v-else class="alert alert-info">
      Please select a room to view archived data.
    </div>
  </div>
</template>

<script>
export default {
  name: 'ArchiveView',
  data() {
    return {
      rooms: [],
      selectedRoomId: '',
      transcriptions: [],
      videoFrames: [],
      quiz: null,
      aiSummary: '',
      loading: false,
      activeTab: 'transcriptions'
    }
  },
  async created() {
    await this.loadRooms()
  },
  methods: {
    async loadRooms() {
      try {
        const response = await fetch('/api/rooms/')
        const data = await response.json()
        this.rooms = data.rooms || []
      } catch (error) {
        console.error('Error loading rooms:', error)
      }
    },
    async loadArchiveData() {
      if (!this.selectedRoomId) return
      
      this.loading = true
      
      try {
        // Load transcriptions
        await this.loadTranscriptions()
        
        // Load video frames
        await this.loadVideoFrames()
        
        // Load quiz data
        await this.loadQuizData()
        
        // Generate AI summary if we have transcriptions
        if (this.transcriptions.length > 0) {
          await this.generateSummary()
        }
      } catch (error) {
        console.error('Error loading archive data:', error)
      } finally {
        this.loading = false
      }
    },
    async loadTranscriptions() {
      try {
        const response = await fetch(`/api/rooms/${this.selectedRoomId}/transcriptions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            limit: 50
          })
        })
        
        const data = await response.json()
        this.transcriptions = data.data || []
        
        // Sort by timestamp
        this.transcriptions.sort((a, b) => a.metadata.timestamp - b.metadata.timestamp)
      } catch (error) {
        console.error('Error loading transcriptions:', error)
        this.transcriptions = []
      }
    },
    async loadVideoFrames() {
      try {
        const response = await fetch(`/api/rooms/${this.selectedRoomId}/video-data`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            limit: 30
          })
        })
        
        const data = await response.json()
        this.videoFrames = data.data || []
        
        // Sort by timestamp
        this.videoFrames.sort((a, b) => a.metadata.timestamp - b.metadata.timestamp)
      } catch (error) {
        console.error('Error loading video frames:', error)
        this.videoFrames = []
      }
    },
    async loadQuizData() {
      try {
        const response = await fetch(`/api/rooms/${this.selectedRoomId}/quiz`)
        const data = await response.json()
        this.quiz = data.quiz_data || null
      } catch (error) {
        console.error('Error loading quiz data:', error)
        this.quiz = null
      }
    },
    async generateSummary() {
      // Combine all transcriptions into one text
      const allText = this.transcriptions
        .map(t => t.frame_data)
        .join(' ')
      
      try {
        const response = await fetch('/api/generate-quiz/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            content: allText,
            num_questions: 0  // We just want the summary, not questions
          })
        })
        
        const data = await response.json()
        this.aiSummary = data.summary || ''
      } catch (error) {
        console.error('Error generating summary:', error)
        this.aiSummary = ''
      }
    },
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleDateString()
    },
    formatDateTime(timestamp) {
      return new Date(timestamp).toLocaleString()
    },
    formatSummary(text) {
      // Convert bullet points to HTML
      return text
        .replace(/\n/g, '<br>')
        .replace(/•/g, '<br>• ')
        .replace(/-/g, '<br>- ')
    }
  }
}
</script>

<style scoped>
.card-body {
  padding: 1.5rem;
}
</style> 