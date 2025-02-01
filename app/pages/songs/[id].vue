<template>
    <div class="bg-[#001d3d] text-white p-6 rounded-lg shadow-xl max-w-md w-full">
      <!-- Song Title and Artist -->
      <div class="flex flex-col items-center mb-6">
        <h2 class="text-3xl font-bold text-[#ffd60a] mb-2">{{ currentSong.title }}</h2>
        <h3 class="text-xl text-[#cfcfcf]">{{ currentSong.artist || 'Unknown Artist' }}</h3>
      </div>
  
      <!-- Audio Controls -->
      <div class="flex flex-col items-center space-y-4">
        <audio ref="audioElement" :src="currentSong.file_path" @timeupdate="updateProgress" @loadedmetadata="initializeAudio" controls class="hidden"></audio>
        <div class="flex items-center space-x-4 w-full justify-center">
          <!-- Previous Button -->
          <button @click="prevSong" class="text-[#ffd60a] p-3 hover:bg-[#003566] rounded-full transition duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
  
          <!-- Play/Pause Button -->
          <button @click="togglePlayPause" class="bg-[#ffd60a] text-[#001d3d] p-4 rounded-full hover:bg-[#ffc300] transition duration-200">
            <svg v-if="!isPlaying" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v18l15-9-15-9z"></path>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
  
          <!-- Next Button -->
          <button @click="nextSong" class="text-[#ffd60a] p-3 hover:bg-[#003566] rounded-full transition duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>
  
        <!-- Progress Bar -->
        <div class="w-full mt-4">
          <input
            type="range"
            v-model="progress"
            :max="duration"
            @input="setAudioProgress"
            class="w-full bg-[#003566] rounded-lg"
          />
          <div class="flex justify-between text-xs mt-2">
            <span>{{ formatTime(currentTime) }}</span>
            <span>{{ formatTime(duration) }}</span>
          </div>
        </div>
      </div>
    </div>
</template>
  
<script setup lang="ts">
import type { Song } from "../../../types/index";

// Internal state for audio control
const isPlaying = ref(false);
const progress = ref(0);
const duration = ref(0);
const currentTime = ref(0);

// Audio element reference
const audioElement = ref<HTMLAudioElement | null>(null);

// Method to play or pause the audio
const togglePlayPause = () => {
    if (isPlaying.value) {
        audioElement.value?.pause();
    } else {
        audioElement.value?.play();
    }
    isPlaying.value = !isPlaying.value;
};

// Method to update progress on timeupdate
const updateProgress = () => {
    if (audioElement.value) {
        progress.value = audioElement.value.currentTime;
        currentTime.value = audioElement.value.currentTime;
    }
};

// Method to initialize audio settings
const initializeAudio = () => {
    if (audioElement.value) {
        duration.value = audioElement.value.duration;
    }
};

// Method to set progress via range input
const setAudioProgress = () => {
    if (audioElement.value) {
        audioElement.value.currentTime = progress.value;
    }
};

// Method to format time (in seconds) into a readable format
const formatTime = (time: number): string => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
};

// Skip to next song (for future use)
const nextSong = () => {
// Logic to load next song
};

// Skip to previous song (for future use)
const prevSong = () => {
// Logic to load previous song
};

// Play the song once the component is mounted
onMounted(() => {
    nextTick(() => {
        togglePlayPause(); // Start playing immediately after mount
    });
});
</script>
