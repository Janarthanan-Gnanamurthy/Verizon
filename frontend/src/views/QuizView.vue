<template>
  <div class="py-8">
    <div class="max-w-4xl mx-auto px-4">
      <!-- Summary Card -->
      <div class="card bg-base-100 shadow-xl mb-8">
        <div class="card-body">
          <h2 class="card-title text-2xl flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-primary">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
            </svg>
            Session Summary
          </h2>
          <div v-if="summary" class="mt-4">
            <div v-html="formattedSummary"></div>
          </div>
          <div v-else class="alert alert-info">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span>Loading session summary...</span>
          </div>
        </div>
      </div>

      <!-- Quiz Card -->
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-2xl flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-secondary">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" />
            </svg>
            Knowledge Check
          </h2>
          
          <div v-if="loading" class="flex justify-center my-8">
            <span class="loading loading-spinner loading-lg text-primary"></span>
          </div>
          
          <div v-else-if="error" class="alert alert-error">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span>{{ error }}</span>
          </div>
          
          <div v-else-if="quizCompleted" class="my-8">
            <div class="text-center">
              <div class="stat-value text-4xl mb-4">{{ score }}/{{ questions.length }}</div>
              <p class="text-xl mb-6">You've completed the quiz!</p>
              <div class="flex justify-center space-x-2">
                <button @click="retakeQuiz" class="btn btn-outline btn-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-1">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
                  </svg>
                  Retake Quiz
                </button>
                <button @click="goHome" class="btn btn-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-1">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                  </svg>
                  Go Home
                </button>
              </div>
            </div>
          </div>
          
          <div v-else-if="questions.length > 0" class="mt-4">
            <div class="flex justify-between items-center mb-4">
              <div class="badge badge-lg">Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}</div>
              <div class="text-sm">Score: {{ score }}</div>
            </div>
            
            <div class="card bg-base-200">
              <div class="card-body">
                <h3 class="text-xl font-medium mb-4">{{ currentQuestion.question }}</h3>
                
                <div class="space-y-3">
                  <div 
                    v-for="(option, index) in currentQuestion.options" 
                    :key="index"
                    class="form-control"
                  >
                    <label 
                      :class="[
                        'cursor-pointer label border rounded-lg p-4 hover:bg-base-300 transition-colors',
                        answered && index === currentQuestion.correctOptionIndex ? 'bg-success/20 border-success' : '',
                        answered && selectedOption === index && index !== currentQuestion.correctOptionIndex ? 'bg-error/20 border-error' : '',
                        selectedOption === index && !answered ? 'bg-primary/10 border-primary' : ''
                      ]"
                    >
                      <div class="flex items-center gap-3">
                        <input 
                          type="radio" 
                          :name="'question-' + currentQuestionIndex" 
                          :value="index" 
                          v-model="selectedOption"
                          class="radio"
                          :class="answered ? 'pointer-events-none' : ''"
                          :disabled="answered"
                        />
                        <span class="label-text">{{ option }}</span>
                      </div>
                    </label>
                  </div>
                </div>
                
                <div v-if="answered" class="alert mt-4" :class="isCorrect ? 'alert-success' : 'alert-error'">
                  <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  <span>{{ isCorrect ? 'Correct!' : 'Incorrect. The correct answer is: ' + currentQuestion.options[currentQuestion.correctOptionIndex] }}</span>
                </div>
                
                <div class="card-actions justify-end mt-6">
                  <button 
                    v-if="!answered" 
                    class="btn btn-primary" 
                    @click="checkAnswer" 
                    :disabled="selectedOption === null"
                  >
                    Submit Answer
                  </button>
                  <button 
                    v-else
                    class="btn btn-accent" 
                    @click="nextQuestion"
                  >
                    {{ isLastQuestion ? 'Finish Quiz' : 'Next Question' }}
                    <svg v-if="!isLastQuestion" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 ml-1">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="alert alert-info">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span>No questions available for this session.</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

// Set the base URL for API requests
axios.defaults.baseURL = 'http://192.168.72.220:8000';

// Component state
const route = useRoute();
const router = useRouter();
const roomId = route.params.roomId;
const summary = ref('');
const questions = ref([]);
const currentQuestionIndex = ref(0);
const selectedOption = ref(null);
const answered = ref(false);
const score = ref(0);
const quizCompleted = ref(false);
const loading = ref(true);
const error = ref(null);

// Computed properties
const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value] || {};
});

const isLastQuestion = computed(() => {
  return currentQuestionIndex.value === questions.value.length - 1;
});

const isCorrect = computed(() => {
  if (selectedOption.value === null) return false;
  return selectedOption.value === currentQuestion.value.correctOptionIndex;
});

const formattedSummary = computed(() => {
  if (!summary.value) return '';
  // Convert bullet points to HTML
  return summary.value.replace(/•/g, '<br>•').replace(/\n/g, '<br>');
});

// Functions
async function fetchQuizData() {
  try {
    loading.value = true;
    error.value = null;
    console.log(`Fetching quiz data for room: ${roomId}`);
    
    const response = await axios.get(`/rooms/${roomId}/quiz`);
    console.log('Quiz API response:', response.data);
    
    if (response.data.questions) {
      questions.value = response.data.questions;
      console.log(`Loaded ${questions.value.length} questions successfully`);
    } else {
      console.warn('Response does not contain questions array:', response.data);
      error.value = 'Quiz data is not in the expected format.';
    }
    
    // Get the last AI summary from localStorage
    summary.value = localStorage.getItem(`room_${roomId}_summary`) || '';
    console.log('Summary from localStorage:', summary.value ? 'Found' : 'Not found');
    
    loading.value = false;
  } catch (err) {
    console.error('Failed to fetch quiz data:', err);
    
    // More detailed error info
    if (err.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Error response:', err.response.data);
      console.error('Status code:', err.response.status);
      
      if (err.response.status === 404) {
        error.value = 'No quiz has been generated for this session yet. Try ending the session again.';
      } else {
        error.value = `Server error: ${err.response.status}. ${err.response.data?.detail || ''}`;
      }
    } else if (err.request) {
      // The request was made but no response was received
      console.error('No response received from server');
      error.value = 'Could not connect to the server. Please check your network connection.';
    } else {
      // Something happened in setting up the request that triggered an Error
      error.value = 'Failed to load quiz questions: ' + err.message;
    }
    
    loading.value = false;
  }
}

function checkAnswer() {
  if (selectedOption.value === null) return;
  
  answered.value = true;
  if (isCorrect.value) {
    score.value++;
  }
}

function nextQuestion() {
  if (isLastQuestion.value) {
    quizCompleted.value = true;
    return;
  }
  
  currentQuestionIndex.value++;
  selectedOption.value = null;
  answered.value = false;
}

function retakeQuiz() {
  currentQuestionIndex.value = 0;
  selectedOption.value = null;
  answered.value = false;
  score.value = 0;
  quizCompleted.value = false;
}

function goHome() {
  router.push('/');
}

// Initialize component
onMounted(() => {
  fetchQuizData();
});
</script> 