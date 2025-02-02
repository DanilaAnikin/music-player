<template>
  <div class="w-svw flex justify-center h-svh items-center">
    <div v-if="currentSong" class="bg-[#001d3d] text-white py-6 px-10 rounded-lg shadow-xl max-w-3xl w-full flex flex-col justify-between">
      <!-- Song Title and Artist -->
      <div class="flex flex-col text-center mb-6">
        <NuxtLink to="/">
          <ChevronLeftIcon class="w-16 h-16 text-[#ffd60a] hover:bg-[#001d3d] rounded-full p-3 transition-all duration-500 cursor-pointer" />
        </NuxtLink>
        <h2 class="text-4xl font-bold text-[#ffd60a] mb-2">{{ currentSong.title }}</h2>
      </div>
  
      <!-- Audio Controls -->
      <div class="flex flex-col items-center space-y-4">
        <audio ref="audioElement" :src="currentSong.file_path" @timeupdate="updateProgress" @loadedmetadata="initializeAudio" controls class="hidden"></audio>
        <div class="flex items-center space-x-4 w-full justify-center">
          <!-- Previous Button -->
          <button @click="currentSong = prevSong()" class="text-[#ffd60a] p-3 hover:bg-[#003566] rounded-full transition duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
    
          <!-- Play/Pause Button -->
          <button @click="togglePlayPause" class="bg-[#ffd60a] text-[#001d3d] p-4 rounded-full hover:bg-[#ffc300] transition duration-200">
            <PlayIcon v-if="!isPlaying" class="w-6 h-6" />
            <PauseIcon v-else class="w-6 h-6" />
          </button>
    
          <!-- Next Button -->
          <button @click="currentSong = nextSong()" class="text-[#ffd60a] p-3 hover:bg-[#003566] rounded-full transition duration-200">
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
  </div>
</template>
  
<script setup lang="ts">
import type { Song } from "../../../types/index";
import { PlayIcon, PauseIcon, ChevronLeftIcon } from '@heroicons/vue/24/solid';

const songs = ref<Song[]>([]);

const isPlaying = ref(false);
const progress = ref(0);
const duration = ref(0);
const currentTime = ref(0);

const route = useRoute();
const currentSong = ref<Song | null>(null);

// Audio element reference
const fetchSongs = async() => {
  const response = await fetch('http://localhost:5000/songs');
  const data = await response.json();
  songs.value = data;
  currentSong.value = songs.value.find(s => s.id == route.query.id);
}
const audioElement = ref<HTMLAudioElement | null>(null);

const prevSong = () => {
  const targetId = currentSong.value.id-1;
  let foundSong = songs.value.find(s => s.id == targetId);

  if(!foundSong) {
    const smallerSongs = songs.value.filter(s => s.id < targetId);

    if(!smallerSongs) {
      foundSong = songs.value.reduce((maxSong, currSong) => {
        return currSong.id > maxSong.id ? currSong : maxSong
      });
    } else {
      foundSong = smallerSongs.reduce((maxSmallerSong, currSong) => {
        return currSong.id > maxSmallerSong.id ? currSong : maxSmallerSong;
      });
    }
  }

  return foundSong;
}

const nextSong = () => {
  const targetId = currentSong.value.id+1;
  let foundSong = songs.value.find(s => s.id == targetId);

  if(!foundSong) {
    const largerSongs = songs.value.filter(s => s.id > targetId);

    if(!largerSongs) {
      foundSong = songs.value.reduce((minSong, currSong) => {
        return currSong.id < minSong.id ? currSong : minSong;
      });
    } else {
      foundSong = largerSongs.reduce((minLargerSong, currSong) => {
        return currSong.id < minLargerSong.id ? currSong : minLargerSong;
      });
    }
  }

  return foundSong;
}

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

// Play the song once the component is mounted
onMounted(() => {
  fetchSongs();
});
</script>
