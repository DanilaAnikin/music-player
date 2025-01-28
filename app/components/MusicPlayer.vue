<template>
    <div class="bg-gray-800 text-white p-6 rounded-lg shadow-lg">
      <h1 class="text-2xl font-bold mb-4">Music Player</h1>
      <div v-if="currentSong">
        <h2 class="text-xl">{{ currentSong.title }}</h2>
        <p class="text-gray-400">{{ currentSong.artist }}</p>
        <audio :src="currentSong.file_path" controls class="w-full mt-4"></audio>
      </div>
      <ul class="mt-6">
        <li
          v-for="song in songs"
          :key="song.id"
          @click="playSong(song)"
          class="p-2 hover:bg-gray-700 cursor-pointer"
        >
          {{ song.title }} - {{ song.artist }}
        </li>
      </ul>
    </div>
</template>
  
<script setup lang="ts">
const songs = ref([]);
const currentSong = ref(null);

onMounted(async () => {
    const data = await $fetch('/api/songs');
    songs.value = data;
    console.log(songs.value);
});

const playSong = (song) => {
    currentSong.value = song;
};

</script>