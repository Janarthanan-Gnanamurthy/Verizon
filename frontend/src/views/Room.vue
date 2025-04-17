<template>
  <div class="h-[calc(100vh-11rem)]">
    <!-- Loading Overlay -->
    <div v-if="!roomLoaded" class="fixed inset-0 bg-base-300 bg-opacity-75 flex items-center justify-center z-50">
      <div class="text-center p-8 max-w-md">
        <span class="loading loading-spinner loading-lg text-primary"></span>
        <p class="mt-4 text-lg font-medium">Setting up your room...</p>
        <p class="text-sm opacity-70">Please allow camera and microphone access when prompted</p>
      </div>
    </div>

    <!-- Main Room Content -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 h-full">
      <!-- Video Section -->
      <div class="lg:col-span-2 flex flex-col">
        <div class="card bg-base-100 shadow-xl h-full">
          <div class="card-body flex flex-col p-4">
            <div class="flex justify-between items-center mb-4">
              <h2 class="card-title flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
                </svg>
                Video Conference
              </h2>
              
              <div class="badge badge-primary gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
                </svg>
                <span>{{ peers.length + 1 }} participants</span>
              </div>
            </div>
            
            <!-- Video Grid with Glassmorphism Effect -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 flex-grow overflow-y-auto p-2 rounded-box">
              <!-- Local Video -->
              <div class="relative rounded-box bg-gradient-to-br from-base-300/70 to-base-300/30 backdrop-blur-sm shadow-lg overflow-hidden border border-base-content/10">
                <video ref="localVideo" autoplay muted class="w-full h-full object-cover"></video>
                <div class="absolute bottom-3 left-3 px-3 py-1.5 rounded-full bg-black/40 backdrop-blur-sm text-white flex items-center gap-2 text-sm">
                  <div class="w-2 h-2 rounded-full bg-success animate-pulse"></div>
                  You ({{ username }})
                </div>
                <div class="absolute top-3 right-3" v-if="isMuted || isVideoOff">
                  <div v-if="isMuted" class="badge badge-sm badge-error gap-1 mr-1">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 9.75L19.5 12m0 0l2.25 2.25M19.5 12l2.25-2.25M19.5 12l-2.25 2.25m-10.5-6l4.72-4.72a.75.75 0 011.28.531V19.94a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.506-1.938-1.354A9.01 9.01 0 012.25 12c0-.83.112-1.633.322-2.395C2.806 8.757 3.63 8.25 4.51 8.25H6.75z" />
                    </svg>
                  </div>
                  <div v-if="isVideoOff" class="badge badge-sm badge-error gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M12 18.75H4.5a2.25 2.25 0 01-2.25-2.25V9m12.841 9.091L16.5 19.5m-1.409-1.409c.407-.407.659-.97.659-1.591v-9a2.25 2.25 0 00-2.25-2.25h-9c-.621 0-1.184.252-1.591.659m12.182 12.182L2.909 5.909M1.5 4.5l1.409 1.409" />
                    </svg>
                  </div>
                </div>
              </div>
              
              <!-- Remote Videos -->
              <div v-for="peer in peers" :key="peer.id" class="relative rounded-box bg-gradient-to-br from-base-300/70 to-base-300/30 backdrop-blur-sm shadow-lg overflow-hidden border border-base-content/10">
                <video 
                  :ref="el => addVideoElement(peer.id, el)" 
                  autoplay 
                  playsinline
                  class="w-full h-full object-cover"
                  @loadedmetadata="console.log(`Video loaded for ${peer.id}`)"
                  @playing="console.log(`Video playing for ${peer.id}`)"
                  @error="e => console.error(`Video error for ${peer.id}:`, e)"
                ></video>
                <div class="absolute bottom-3 left-3 px-3 py-1.5 rounded-full bg-black/40 backdrop-blur-sm text-white flex items-center gap-2 text-sm">
                  <div class="w-2 h-2 rounded-full bg-info animate-pulse"></div>
                  {{ peer.name }}
                </div>
              </div>
            </div>
            
            <!-- Controls with Modern Design -->
            <div class="flex justify-center items-center gap-3 mt-4 pt-2 border-t border-base-300">
              <!-- Microphone Control -->
              <button @click="toggleMute" class="btn btn-circle" :class="isMuted ? 'btn-outline btn-error' : 'btn-success'">
                <svg v-if="isMuted" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
                </svg>
              </button>
              
              <!-- Camera Control -->
              <button @click="toggleVideo" class="btn btn-circle" :class="isVideoOff ? 'btn-outline btn-error' : 'btn-success'">
                <svg v-if="isVideoOff" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M12 18.75H4.5a2.25 2.25 0 01-2.25-2.25V9m12.841 9.091L16.5 19.5m-1.409-1.409c.407-.407.659-.97.659-1.591v-9a2.25 2.25 0 00-2.25-2.25h-9c-.621 0-1.184.252-1.591.659m12.182 12.182L2.909 5.909M1.5 4.5l1.409 1.409" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
                </svg>
              </button>
              
              <!-- Transcription Control -->
              <div class="dropdown dropdown-top">
                <button @click="toggleTranscription" :class="isTranscribing ? 'btn-primary' : 'btn-info'" class="btn btn-circle">
                  <svg v-if="isTranscribing" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </button>
                <div v-if="isTranscribing" class="dropdown-content z-[1] p-2 shadow-xl bg-base-200 rounded-box w-52 -translate-y-2">
                  <div class="px-2 py-1 font-medium text-sm">Transcription Active</div>
                  <div class="text-xs px-2 pb-2 opacity-70">Speech is being recognized</div>
                </div>
              </div>
              
              <!-- Share Screen (placeholder) -->
              <button class="btn btn-circle btn-outline">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M7.217 10.907a2.25 2.25 0 100 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186l9.566-5.314m-9.566 7.5l9.566 5.314m0 0a2.25 2.25 0 103.935 2.186 2.25 2.25 0 00-3.935-2.186zm0-12.814a2.25 2.25 0 103.933-2.185 2.25 2.25 0 00-3.933 2.185z" />
                </svg>
              </button>
              
              <!-- Leave Room -->
              <button @click="leaveRoom" class="btn btn-circle btn-error">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Communication Section -->
      <div class="card bg-base-100 shadow-xl h-full">
        <div class="card-body flex flex-col p-0">
          <!-- Tabs -->
          <div class="tabs tabs-boxed bg-base-200 rounded-t-box gap-1 p-1 m-2">
            <a 
              @click="activeTab = 'chat'" 
              :class="{ 'tab-active': activeTab === 'chat' }"
              class="tab flex-1 gap-1"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Chat
            </a>
            <a 
              @click="activeTab = 'transcription'" 
              :class="{ 'tab-active': activeTab === 'transcription' }"
              class="tab flex-1 gap-1"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
              </svg>
              Transcript
            </a>
            <a 
              @click="activeTab = 'ai-summary'" 
              :class="{ 'tab-active': activeTab === 'ai-summary' }"
              class="tab flex-1 gap-1"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
              </svg>
              AI Summary
            </a>
          </div>
          
          <!-- Tab Content -->
          <div class="flex-grow overflow-hidden relative px-2 pb-2">
            <!-- Chat Tab -->
            <div v-if="activeTab === 'chat'" class="h-full flex flex-col">
              <div class="overflow-y-auto flex-grow mb-2 px-2 space-y-2">
                <div 
                  v-for="(message, index) in chatMessages" 
                  :key="index" 
                  class="chat" 
                  :class="message.user === username ? 'chat-end' : (message.user === 'System' ? 'chat-start opacity-70' : 'chat-start')"
                >
                  <div class="chat-header opacity-80">
                    {{ message.user }}
                    <time class="text-xs opacity-50 ml-1">{{ formatTime(message.timestamp) }}</time>
                  </div>
                  <div 
                    class="chat-bubble" 
                    :class="{
                      'chat-bubble-primary': message.user === username,
                      'chat-bubble-accent': message.user !== username && message.user !== 'System',
                      'chat-bubble-secondary': message.user === 'System'
                    }"
                  >
                    {{ message.content }}
                  </div>
                </div>
              </div>
              <div class="flex gap-2 p-2 bg-base-200 rounded-box">
                <input 
                  type="text" 
                  v-model="newMessage" 
                  @keyup.enter="sendMessage" 
                  placeholder="Type a message..." 
                  class="input input-bordered flex-grow"
                />
                <button @click="sendMessage" class="btn btn-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Transcription Tab -->
            <div v-if="activeTab === 'transcription'" class="h-full flex flex-col px-2">
              <div class="bg-base-200 rounded-box p-3 mb-3 flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="badge badge-primary" :class="isTranscribing ? 'badge-primary' : 'badge-outline'">Status</div>
                  <span class="text-sm font-medium">{{ isTranscribing ? 'Transcription Active' : 'Transcription Inactive' }}</span>
                </div>
                <button 
                  @click="toggleTranscription" 
                  class="btn btn-sm" 
                  :class="isTranscribing ? 'btn-error' : 'btn-success'"
                >
                  {{ isTranscribing ? 'Stop' : 'Start' }}
                </button>
              </div>
              
              <div class="overflow-y-auto flex-grow space-y-3">
                <div v-for="(entry, index) in transcription" :key="index" class="card bg-base-100 mb-3">
                  <div class="card-body p-3">
                    <div class="flex justify-between items-center">
                      <div class="font-medium">{{ entry.user }}</div>
                      <div class="text-xs opacity-60">{{ formatTime(entry.timestamp) }}</div>
                    </div>
                    <div class="mt-1 pl-3 border-l-2 border-primary">{{ entry.content }}</div>
                  </div>
                </div>
                
                <div v-if="isTranscribing && currentTranscription" class="alert alert-info shadow-md">
                  <div class="flex items-start">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-info shrink-0 w-6 h-6 mt-1"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <div>
                      <div class="font-bold">Listening...</div>
                      <div class="text-sm opacity-90">{{ currentTranscription }}</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="!isTranscribing" class="alert alert-warning shadow-md mt-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                <div>
                  <h3 class="font-bold">Transcription Off</h3>
                  <div class="text-xs">Click the microphone button or the Start button to enable</div>
                </div>
              </div>
            </div>
            
            <!-- AI Summary Tab -->
            <div v-if="activeTab === 'ai-summary'" class="h-full flex flex-col px-2">
              <div class="overflow-y-auto flex-grow space-y-4">
                <div v-for="(summary, index) in aiSummaries" :key="index" class="card bg-gradient-to-br from-base-100 to-base-200 shadow-lg mb-4">
                  <div class="card-body p-4">
                    <div class="flex justify-between items-center">
                      <h3 class="card-title text-sm font-medium">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-primary">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                        </svg>
                        AI Summary
                      </h3>
                      <span class="text-xs opacity-60">{{ formatTime(summary.timestamp) }}</span>
                    </div>
                    <div class="divider my-1"></div>
                    <div class="whitespace-pre-wrap prose max-w-full text-base-content prose-sm">{{ summary.content }}</div>
                  </div>
                </div>
                
                <div v-if="aiSummaries.length === 0" class="flex flex-col items-center justify-center h-full text-center p-8">
                  <div class="bg-base-200 p-6 rounded-box shadow-md max-w-sm">
                    <div class="text-5xl mb-4">🤖</div>
                    <h3 class="text-xl font-bold mb-2">No AI Summaries Yet</h3>
                    <p class="opacity-75 mb-4">Start transcription and speak for a while to generate AI-powered summaries.</p>
                    <button 
                      @click="startTranscriptionAndSwitchTab" 
                      class="btn btn-primary btn-sm gap-2"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
                      </svg>
                      Start Transcription
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

axios.defaults.baseURL = 'http://172.17.2.29:8000';

// Router and route setup
const route = useRoute();
const router = useRouter();
const roomId = computed(() => route.params.roomId);

// WebRTC references
const localVideo = ref(null);
const localStream = ref(null);
const peerConnections = ref({});
const peers = ref([]);
const websocket = ref(null);

// State variables
const username = ref(localStorage.getItem('username') || 'Guest' + Math.floor(Math.random() * 1000));
const isMuted = ref(false);
const isVideoOff = ref(false);
const isTranscribing = ref(false);
const activeTab = ref('chat');
const roomLoaded = ref(false);

// Content variables
const chatMessages = ref([]);
const newMessage = ref('');
const transcription = ref([]);
const currentTranscription = ref('');
const aiSummaries = ref([]);
const recognition = ref(null);
const transcriptionTimer = ref(null);

// Helper function to switch to transcription tab and start it
function startTranscriptionAndSwitchTab() {
  if (!isTranscribing.value) {
    toggleTranscription();
  }
  activeTab.value = 'transcription';
}

// Save username to localStorage
watch(username, (newValue) => {
  localStorage.setItem('username', newValue);
});

// Auto-scroll chat when new messages arrive
watch(chatMessages, () => {
  nextTick(() => {
    const container = document.querySelector('.chat-tab .overflow-y-auto');
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  });
}, { deep: true });

// Initialize room and WebRTC
onMounted(async () => {
  try {
    // Fetch room details
    const response = await axios.get(`/rooms/${roomId.value}`);
    if (response.data.error) {
      alert('Room not found');
      router.push('/');
      return;
    }
    
    // Setup WebRTC
    await setupMediaDevices();
    connectToWebSocket();
    
    // Add system message
    chatMessages.value.push({
      user: 'System',
      content: 'Connected to the room. Welcome!',
      timestamp: Date.now()
    });
    
    // Mark room as loaded
    roomLoaded.value = true;
    
    // Immediately clean up any potential stale peers
    cleanupStalePeers();
    
    // Set up periodic refresh and cleanup
    const videoRefreshInterval = setInterval(() => {
      refreshVideoElements();
    }, 5000);
    
    // Store the interval to clear it on unmount
    onBeforeUnmount(() => {
      // Clean up all peer connections
      console.log('Cleaning up all peer connections');
      Object.values(peerConnections.value).forEach(pc => {
        if (pc) pc.close();
      });
      peerConnections.value = {};
      peers.value = [];
      
      clearInterval(videoRefreshInterval);
      console.log('Cleared video refresh interval');
    });
  } catch (error) {
    console.error('Failed to initialize room:', error);
    alert('Failed to connect to the room');
    router.push('/');
  }
});

// Clean up on component unmount
onBeforeUnmount(() => {
  // Close all peer connections
  Object.values(peerConnections.value).forEach(pc => pc.close());
  
  // Stop local media streams
  if (localStream.value) {
    localStream.value.getTracks().forEach(track => track.stop());
  }
  
  // Close WebSocket connection
  if (websocket.value && websocket.value.readyState === WebSocket.OPEN) {
    websocket.value.close();
  }
  
  // Stop speech recognition
  stopTranscription();
});

// Setup media devices (camera and microphone)
async function setupMediaDevices() {
  try {
    // First try to get video and audio
    try {
      localStream.value = await navigator.mediaDevices.getUserMedia({ 
        video: true, 
        audio: true 
      });
      console.log('Successfully got both video and audio access');
    } catch (err) {
      console.warn('Failed to get both video and audio, trying audio only:', err);
      
      // If that fails, try audio only
      try {
        localStream.value = await navigator.mediaDevices.getUserMedia({ 
          video: false, 
          audio: true 
        });
        isVideoOff.value = true; // Mark video as off
        console.log('Successfully got audio-only access');
      } catch (audioErr) {
        console.error('Failed to get audio access too:', audioErr);
        alert('Could not access your camera or microphone. Please check your device settings and permissions.');
        
        // Create empty stream as fallback
        localStream.value = new MediaStream();
        isMuted.value = true;
        isVideoOff.value = true;
      }
    }
    
    // Assign stream to video element
    if (localVideo.value) {
      localVideo.value.srcObject = localStream.value;
      console.log('Assigned local stream to video element');
    } else {
      console.warn('Local video element not found');
    }
  } catch (error) {
    console.error('Unexpected error setting up media devices:', error);
    alert('An unexpected error occurred when setting up your media devices.');
  }
}

// Connect to the WebSocket server for signaling
function connectToWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = '172.17.2.29:8000';
  websocket.value = new WebSocket(`${protocol}//${host}/ws/${roomId.value}`);
  
  websocket.value.onopen = () => {
    console.log('Connected to WebSocket server');
    // Send join message with clear username
    sendToServer({
      type: 'signal',
      user: username.value,
      content: {
        type: 'join',
        username: username.value
      }
    });
  };
  
  websocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data);
    handleWebSocketMessage(data);
  };
  
  websocket.value.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  
  websocket.value.onclose = () => {
    console.log('WebSocket connection closed');
  };
}

// Handle incoming WebSocket messages
function handleWebSocketMessage(data) {
  switch (data.type) {
    case 'chat':
      chatMessages.value.push(data);
      break;
      
    case 'signal':
      handleSignalingData(data);
      break;
      
    case 'ai_summary':
      aiSummaries.value.push(data);
      // Notify user about new summary
      chatMessages.value.push({
        user: 'System',
        content: 'New AI summary available in the "AI Summary" tab',
        timestamp: Date.now()
      });
      break;
      
    case 'system':
      console.log('Received system message:', data.content);
      
      // Extract username from the system message
      let affectedUser = '';
      if (data.content.includes('has joined the room')) {
        affectedUser = data.content.split(' ')[0];
        console.log(`User ${affectedUser} has joined the room`);
        
        // Don't create a connection to ourselves
        if (affectedUser !== username.value) {
          console.log(`Creating connection with new user: ${affectedUser}`);
          // Create peer connection if it doesn't exist
          if (!peerConnections.value[affectedUser]) {
            createPeerConnection(affectedUser);
            // Send offer to the new user
            createAndSendOffer(affectedUser);
          }
        }
      } 
      else if (data.content.includes('has left the room')) {
        affectedUser = data.content.split(' ')[0];
        console.log(`User ${affectedUser} has left, cleaning up their connection`);
        
        // Clean up their peer connection if it exists
        if (peerConnections.value[affectedUser]) {
          peerConnections.value[affectedUser].close();
          delete peerConnections.value[affectedUser];
          
          // Remove them from the peers list
          const peerIndex = peers.value.findIndex(p => p.id === affectedUser);
          if (peerIndex !== -1) {
            peers.value.splice(peerIndex, 1);
          }
          
          console.log(`Removed peer connection for ${affectedUser}`);
        }
      }
      
      // Add the system message
      chatMessages.value.push({
        user: 'System',
        content: data.content,
        timestamp: Date.now()
      });
      break;
      
    case 'room_info':
      // Process room participants info
      if (data.participants && data.participants.length > 0) {
        console.log('Room participants:', data.participants);
        
        // Clear peers list to avoid duplicates
        peers.value = [];
        
        // Create connections with all existing participants in the room
        data.participants.forEach(participantId => {
          // Skip ourselves
          if (participantId !== username.value) {
            console.log(`Adding participant: ${participantId}`);
            // Create peer connection if it doesn't exist
            if (!peerConnections.value[participantId]) {
              createPeerConnection(participantId);
              // Send offer to this existing participant
              createAndSendOffer(participantId);
            }
          }
        });
      }
      break;
  }
}

// WebRTC signaling handler
function handleSignalingData(data) {
  const { user, content } = data;
  
  // Skip processing our own messages
  if (user === username.value) return;
  
  console.log(`Received signal of type ${content.type} from ${user}`);
  
  if (content.type === 'join') {
    console.log(`${user} joined with join signal, creating connection`);
    // New user joined, create peer connection
    const pc = createPeerConnection(user);
    // Send offer to the new user
    createAndSendOffer(user);
  }
  else if (content.type === 'offer') {
    console.log(`Processing offer from ${user}`);
    // Get or create peer connection
    const pc = peerConnections.value[user] || createPeerConnection(user);
    
    // Set remote description and create answer
    pc.setRemoteDescription(new RTCSessionDescription(content.sdp))
      .then(() => {
        console.log(`Set remote description from ${user}, creating answer`);
        return pc.createAnswer();
      })
      .then(answer => {
        console.log(`Setting local description (answer) for ${user}`);
        return pc.setLocalDescription(answer);
      })
      .then(() => {
        console.log(`Sending answer to ${user}`);
        sendToServer({
          type: 'signal',
          user: username.value,
          content: {
            type: 'answer',
            target: user,
            sdp: pc.localDescription
          }
        });
      })
      .catch(error => console.error(`Error handling offer from ${user}:`, error));
  }
  else if (content.type === 'answer' && content.target === username.value) {
    console.log(`Processing answer from ${user}`);
    // Get peer connection
    const pc = peerConnections.value[user];
    if (pc) {
      pc.setRemoteDescription(new RTCSessionDescription(content.sdp))
        .then(() => console.log(`Set remote description (answer) from ${user}`))
        .catch(error => console.error(`Error setting remote description from ${user}:`, error));
    } else {
      console.warn(`Received answer from ${user} but no connection exists`);
    }
  }
  else if (content.type === 'ice-candidate' && content.target === username.value) {
    console.log(`Processing ICE candidate from ${user}`);
    // Get peer connection
    const pc = peerConnections.value[user];
    if (pc) {
      pc.addIceCandidate(new RTCIceCandidate(content.candidate))
        .then(() => console.log(`Added ICE candidate from ${user}`))
        .catch(error => console.error(`Error adding ICE candidate from ${user}:`, error));
    } else {
      console.warn(`Received ICE candidate from ${user} but no connection exists`);
    }
  }
}

// Create a new WebRTC peer connection
function createPeerConnection(peerId) {
  // Check if connection already exists
  if (peerConnections.value[peerId]) {
    console.log(`Peer connection for ${peerId} already exists, reusing`);
    return peerConnections.value[peerId];
  }
  
  console.log(`Creating new peer connection for ${peerId}`);
  
  // STUN servers for NAT traversal
  const configuration = {
    iceServers: [
      { urls: 'stun:stun.l.google.com:19302' },
      { urls: 'stun:stun1.l.google.com:19302' },
      { urls: 'stun:stun2.l.google.com:19302' },
      { urls: 'stun:stun3.l.google.com:19302' }
    ]
  };
  
  try {
    // Create the connection
    const pc = new RTCPeerConnection(configuration);
    peerConnections.value[peerId] = pc;
    
    // Add peer to the list if not already there
    const existingPeerIndex = peers.value.findIndex(p => p.id === peerId);
    if (existingPeerIndex === -1) {
      console.log(`Adding new peer ${peerId} to peers list`);
      peers.value.push({
        id: peerId,
        name: peerId,
        videoEl: null
      });
    } else {
      console.log(`Peer ${peerId} already in list, reusing`);
    }
    
    // Add local tracks to the connection
    if (localStream.value) {
      const localTracks = localStream.value.getTracks();
      console.log(`Adding ${localTracks.length} local tracks to connection with ${peerId}`);
      localTracks.forEach(track => {
        try {
          pc.addTrack(track, localStream.value);
          console.log(`Added local ${track.kind} track to peer connection for ${peerId}`);
        } catch (error) {
          console.error(`Error adding track to connection with ${peerId}:`, error);
        }
      });
    } else {
      console.warn('No local stream available when creating peer connection');
    }
    
    // Handle ICE candidates
    pc.onicecandidate = (event) => {
      if (event.candidate) {
        console.log(`Sending ICE candidate to ${peerId}`);
        sendToServer({
          type: 'signal',
          user: username.value,
          content: {
            type: 'ice-candidate',
            target: peerId,
            candidate: event.candidate
          }
        });
      }
    };
    
    // Handle ICE connection state changes
    pc.oniceconnectionstatechange = () => {
      console.log(`ICE connection state for ${peerId}: ${pc.iceConnectionState}`);
      if (pc.iceConnectionState === 'failed' || pc.iceConnectionState === 'disconnected') {
        console.warn(`ICE connection with ${peerId} failed or disconnected. Attempting to restart.`);
        // Attempt to restart ICE connection
        createAndSendOffer(peerId, true);
      }
    };
    
    // Handle connection state changes
    pc.onconnectionstatechange = () => {
      console.log(`Connection state for ${peerId}: ${pc.connectionState}`);
      if (pc.connectionState === 'failed' || pc.connectionState === 'closed') {
        console.warn(`Connection with ${peerId} failed or closed. Cleaning up.`);
        // Remove peer from list
        const peerIndex = peers.value.findIndex(p => p.id === peerId);
        if (peerIndex !== -1) {
          peers.value.splice(peerIndex, 1);
        }
        // Clean up peer connection
        if (peerConnections.value[peerId]) {
          delete peerConnections.value[peerId];
        }
      }
    };
    
    // Handle incoming tracks
    pc.ontrack = (event) => {
      console.log(`Received track from ${peerId}:`, event.track.kind);
      console.log(`Track enabled: ${event.track.enabled}, muted: ${event.track.muted}`);
      
      // Make sure the peer exists in our list
      const peerIndex = peers.value.findIndex(p => p.id === peerId);
      if (peerIndex !== -1 && peers.value[peerIndex].videoEl) {
        peers.value[peerIndex].videoEl.srcObject = event.streams[0];
        peers.value[peerIndex].videoEl.play().catch(() => {
          peers.value[peerIndex].videoEl.muted = true;
          peers.value[peerIndex].videoEl.play();
        });
      }
      
      // Ensure we add both audio and video tracks to the same stream
      const attachRemoteStream = () => {
        const peerIndex = peers.value.findIndex(p => p.id === peerId);
        if (peerIndex === -1) return false;
        
        const videoEl = peers.value[peerIndex].videoEl;
        if (!videoEl) {
          console.log(`Video element for ${peerId} not ready yet`);
          return false;
        }
        
        try {
          if (!event.streams || event.streams.length === 0) {
            console.warn(`No streams in track event for ${peerId}`);
            return false;
          }
          
          // Use the first stream
          const stream = event.streams[0];
          
          // If videoEl already has a srcObject, make sure it's the same stream
          if (videoEl.srcObject) {
            // Check if we're adding to an existing stream or replacing it
            if (videoEl.srcObject.id !== stream.id) {
              console.log(`Replacing stream for ${peerId}`);
              videoEl.srcObject = stream;
            } else {
              console.log(`Using existing stream for ${peerId}`);
            }
          } else {
            console.log(`Setting new stream for ${peerId}`);
            videoEl.srcObject = stream;
          }
          
          // Ensure the video plays
          videoEl.play().catch(err => {
            console.warn(`Error playing video for ${peerId}:`, err);
            // Try again with muted to work around autoplay policy
            videoEl.muted = true;
            videoEl.play().catch(e => console.error(`Still can't play:`, e));
          });
          
          console.log(`Successfully attached stream for ${peerId}`);
          return true;
        } catch (err) {
          console.error(`Error attaching stream for ${peerId}:`, err);
          return false;
        }
      };
      
      // Try to attach immediately
      if (!attachRemoteStream()) {
        // Retry a few times
        let attempts = 0;
        const retryAttach = setInterval(() => {
          attempts++;
          if (attachRemoteStream() || attempts >= 5) {
            clearInterval(retryAttach);
            if (attempts >= 5) {
              console.error(`Failed to attach stream for ${peerId} after multiple attempts`);
            }
          }
        }, 1000);
      }
    };
    
    return pc;
  } catch (error) {
    console.error(`Error creating peer connection for ${peerId}:`, error);
    return null;
  }
}

// Create and send WebRTC offer
function createAndSendOffer(peerId, isRestart = false) {
  const pc = peerConnections.value[peerId];
  if (!pc) {
    console.warn(`Can't create offer - no connection for ${peerId}`);
    return;
  }
  
  const offerOptions = isRestart ? { iceRestart: true } : undefined;
  
  pc.createOffer(offerOptions)
    .then(offer => {
      console.log(`Created offer for ${peerId}, setting local description`);
      return pc.setLocalDescription(offer);
    })
    .then(() => {
      console.log(`Sending offer to ${peerId}`);
      sendToServer({
        type: 'signal',
        user: username.value,
        content: {
          type: 'offer',
          target: peerId,
          sdp: pc.localDescription
        }
      });
    })
    .catch(error => console.error(`Error creating/sending offer to ${peerId}:`, error));
}

// Send message to WebSocket server
function sendToServer(message) {
  if (websocket.value && websocket.value.readyState === WebSocket.OPEN) {
    websocket.value.send(JSON.stringify(message));
  }
}

// Send chat message
function sendMessage() {
  if (!newMessage.value.trim()) return;
  
  const message = {
    type: 'chat',
    user: username.value,
    content: newMessage.value,
    timestamp: Date.now()
  };
  
  sendToServer(message);
  chatMessages.value.push(message);
  newMessage.value = '';
}

// Toggle microphone
function toggleMute() {
  if (localStream.value) {
    const audioTracks = localStream.value.getAudioTracks();
    audioTracks.forEach(track => {
      track.enabled = isMuted.value;
    });
    isMuted.value = !isMuted.value;
    
    // Stop transcription if muting
    if (isMuted.value && isTranscribing.value) {
      toggleTranscription();
    }
  }
}

// Toggle camera
function toggleVideo() {
  if (localStream.value) {
    const videoTracks = localStream.value.getVideoTracks();
    videoTracks.forEach(track => {
      track.enabled = isVideoOff.value;
    });
    isVideoOff.value = !isVideoOff.value;

    // Renegotiate with all peers if video is toggled
    Object.keys(peerConnections.value).forEach(peerId => {
      createAndSendOffer(peerId, true);
    });
  }
}

// Transcription functionality
function toggleTranscription() {
  isTranscribing.value = !isTranscribing.value;
  
  if (isTranscribing.value) {
    // Can't transcribe if muted
    if (isMuted.value) {
      toggleMute();
    }
    startTranscription();
  } else {
    stopTranscription();
  }
}

// Start speech recognition
function startTranscription() {
  // Check if browser supports SpeechRecognition
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  
  if (!SpeechRecognition) {
    alert('Your browser does not support speech recognition. Try Chrome or Edge.');
    isTranscribing.value = false;
    return;
  }

  // Initialize recognition
  recognition.value = new SpeechRecognition();
  recognition.value.continuous = true;
  recognition.value.interimResults = true;
  
  // Handle results
  recognition.value.onresult = (event) => {
    let interimTranscript = '';
    let finalTranscript = '';
    
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        finalTranscript += event.results[i][0].transcript;
      } else {
        interimTranscript += event.results[i][0].transcript;
      }
    }
    
    if (finalTranscript) {
      // Add to transcription list
      const transcriptionEntry = {
        user: username.value,
        content: finalTranscript,
        timestamp: Date.now()
      };
      
      transcription.value.push(transcriptionEntry);
      currentTranscription.value = '';
      
      // Send to server for AI processing
      sendToServer({
        type: 'transcription',
        user: username.value,
        content: finalTranscript,
        timestamp: transcriptionEntry.timestamp
      });
      
      // Switch to the transcription tab
      activeTab.value = 'transcription';
    } else if (interimTranscript) {
      currentTranscription.value = interimTranscript;
    }
  };
  
  // Handle errors
  recognition.value.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    if (event.error === 'no-speech') {
      // No speech detected, restart after a short delay
      setTimeout(() => {
        if (isTranscribing.value && recognition.value) {
          try {
            recognition.value.start();
          } catch (e) {
            console.log('Recognition already started:', e);
          }
        }
      }, 1000);
    } else {
      isTranscribing.value = false;
      alert(`Speech recognition error: ${event.error}`);
    }
  };
  
  // Start recognition
  try {
    recognition.value.start();
    console.log('Speech recognition started');
    
    // Set up a periodic check to ensure transcription is working
    transcriptionTimer.value = setInterval(() => {
      if (isTranscribing.value) {
        try {
          recognition.value.start();
        } catch (e) {
          // Recognition already started, that's fine
          console.log('Recognition already started (periodic check)');
        }
      }
    }, 10000); // Check every 10 seconds
  } catch (error) {
    console.error('Error starting speech recognition:', error);
  }
}

// Stop speech recognition
function stopTranscription() {
  if (recognition.value) {
    try {
      recognition.value.stop();
      recognition.value = null;
    } catch (error) {
      console.error('Error stopping speech recognition:', error);
    }
  }
  
  if (transcriptionTimer.value) {
    clearInterval(transcriptionTimer.value);
    transcriptionTimer.value = null;
  }
  
  currentTranscription.value = '';
  isTranscribing.value = false;
}

// Leave the room
function leaveRoom() {
  router.push('/');
}

// Helper to format timestamps
function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Function to restart a peer connection if needed
async function restartPeerConnection(peerId) {
  console.log(`Attempting to restart peer connection with ${peerId}`);
  
  // Close the old connection
  if (peerConnections.value[peerId]) {
    peerConnections.value[peerId].close();
    delete peerConnections.value[peerId];
  }
  
  // Create a new connection
  const pc = createPeerConnection(peerId);
  
  // Create and send a new offer
  try {
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    
    sendToServer({
      type: 'signal',
      user: username.value,
      content: {
        type: 'offer',
        target: peerId,
        sdp: offer
      }
    });
    
    console.log(`Successfully restarted connection with ${peerId}`);
  } catch (err) {
    console.error(`Failed to restart connection with ${peerId}:`, err);
  }
}

// Add this function to manually clean up stale peers
function cleanupStalePeers() {
  console.log("Cleaning up stale peers...");
  
  // Check each peer connection
  for (const peerId in peerConnections.value) {
    const pc = peerConnections.value[peerId];
    
    // Check if connection is closed, failed, or doesn't have a video track
    if (!pc || 
        pc.connectionState === 'closed' || 
        pc.connectionState === 'failed' ||
        pc.iceConnectionState === 'disconnected' ||
        pc.iceConnectionState === 'failed') {
      
      console.log(`Removing stale peer connection: ${peerId}`);
      
      // Close the connection if it exists
      if (pc) {
        pc.close();
      }
      
      // Remove from peerConnections
      delete peerConnections.value[peerId];
      
      // Remove from peers list
      const peerIndex = peers.value.findIndex(p => p.id === peerId);
      if (peerIndex !== -1) {
        peers.value.splice(peerIndex, 1);
      }
    }
  }
}

// Update the ref handler for remote video elements
function addVideoElement(peerId, element) {
  if (!element) return;

  const peerIndex = peers.value.findIndex(p => p.id === peerId);
  if (peerIndex !== -1) {
    peers.value[peerIndex].videoEl = element;

    // Try to get the remote stream from the peer connection
    const pc = peerConnections.value[peerId];
    if (pc) {
      // Collect all remote tracks and create a MediaStream
      const remoteTracks = [];
      pc.getReceivers().forEach(receiver => {
        if (receiver.track && receiver.track.kind === "video") {
          remoteTracks.push(receiver.track);
        }
      });
      if (remoteTracks.length > 0) {
        const remoteStream = new MediaStream(remoteTracks);
        element.srcObject = remoteStream;
        element.play().catch(() => {
          element.muted = true;
          element.play();
        });
      }
    }
  }
}

// Add a helper function to update and refresh video elements
function refreshVideoElements() {
  // First clean up any stale peers
  cleanupStalePeers();
  
  // Then refresh video elements
  nextTick(() => {
    peers.value.forEach(peer => {
      if (peer.videoEl) {
        // Check if video element is playing correctly
        if (!peer.videoEl.srcObject || 
            peer.videoEl.srcObject.getVideoTracks().length === 0 ||
            peer.videoEl.srcObject.getVideoTracks()[0].readyState !== 'live') {
          
          console.log(`Refreshing video for peer ${peer.id}`);
          const pc = peerConnections.value[peer.id];
          
          if (pc) {
            // Get all streams from this connection
            const receivers = pc.getReceivers();
            const videoReceivers = receivers.filter(r => 
              r.track && 
              r.track.kind === 'video' && 
              r.track.readyState === 'live' &&
              r.track.enabled
            );
            
            if (videoReceivers.length > 0) {
              // Use the first available stream
              const stream = videoReceivers[0].streams && videoReceivers[0].streams.length > 0
                ? videoReceivers[0].streams[0]
                : new MediaStream([videoReceivers[0].track]);
              
              console.log(`Refreshing stream for ${peer.id}`);
              peer.videoEl.srcObject = stream;
              peer.videoEl.play().catch(e => {
                console.warn(`Error playing refreshed video:`, e);
                peer.videoEl.muted = true;
                peer.videoEl.play().catch(err => console.error(`Still can't play:`, err));
              });
            } else {
              console.log(`No video tracks available for ${peer.id}`);
            }
          }
        }
      }
    });
  });
}
</script> 