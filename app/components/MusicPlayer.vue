<template>
  <div class="bg-[#051a30] text-white p-6 rounded-lg shadow-xl max-w-md w-full">
    <h1 class="text-3xl font-bold mb-6 text-[#239eb1]">Music Player</h1>

    <!-- All Songs Section -->
    <div v-if="!currentPlaylist">
      <h2 class="text-xl mt-6 text-[#15616d]">All Songs</h2>
      <div v-if="songs.length" class="mt-2 space-y-1 flex flex-col">
        <NuxtLink
          v-for="song in songs"
          :key="song.id"
          :to="{
            path: '/songs/SongPlayer',
            query: { id: song.id }
          }"
          class="px-2 py-1 hover:bg-[#003566] truncate border border-[#cfcfcf] cursor-pointer rounded-lg transition-all duration-200"
        >
          <span>{{ song.title }}</span>
        </NuxtLink>
      </div>
      <span v-else>No songs added yet</span>
    </div>

    <!-- Playlist Songs Section -->
    <div v-else-if="currentPlaylist.songs.length">
      <button @click="goBackToSongs" class="p-2 bg-[#15616d] text-[#001d3d] mb-4 rounded-lg shadow-md hover:bg-[#14515a] transition-all">Back to All Songs</button>
      <h3 class="text-xl text-[#15616d]">Songs in {{ currentPlaylist.name }}</h3>
      <ul class="mt-2 space-y-2">
        <NuxtLink
          v-for="song in currentPlaylist.songs"
          :key="song.id"
          :to="{
            path: '/songs/SongPlayer',
            query: { id: song.id }
          }"
          class="p-2 hover:bg-[#003566] border border-[#cfcfcf] cursor-pointer rounded-lg transition-all duration-200 ease-in-out flex justify-between"
        > 
          <span class="truncate">{{ song.title }}</span>
          <button
            @click="removeSongFromPlaylist(song.id)"
            class="ml-2 p-1 border border-[#b82727] text-white font-bold text-sm rounded-lg hover:bg-[#003566] transition-all"
          >
            <TrashIcon class="w-4 h-4 text-[#b82727]" />
          </button>
        </NuxtLink>
      </ul>
    </div>

    <!-- No Songs in Playlist Section -->
    <div v-else>
      <button @click="goBackToSongs" class="p-2 bg-[#15616d] text-[#001d3d] mb-4 rounded-lg shadow-md hover:bg-[#14515a] transition-all">Back to All Songs</button>
      <h3 class="text-xl text-[#15616d]">No songs in {{ currentPlaylist.name }}</h3>
    </div>

    <!-- Current Song Section -->
    <div v-if="currentSong">
      <h2 class="text-xl mt-6 text-[#15616d]">{{ currentSong.title }}</h2>
      <audio :src="currentSong.file_path" controls class="w-full mt-4 rounded-lg shadow-lg border-2 border-[#003566]"></audio>
    </div>

    <!-- Playlist Creation Section -->
    <div class="mt-2 space-y-1">
      <input v-model="playlistName" placeholder="Enter Playlist Name" class="px-3 py-2 text-[#cfcfcf] outline-none font-semibold rounded-lg shadow-md w-full bg-[#003566] placeholder:text-[#cfcfcf]" />
      <button @click="createPlaylist" class="p-2 bg-[#2298aa] text-[#001d3d] rounded-lg shadow-md hover:bg-[#247e8b] transition-all duration-300">Create Playlist</button>
    </div>

    <!-- Playlists Section -->
    <h2 class="text-xl mt-6 text-[#15616d]">Playlists</h2>
    <ul class="mt-2 space-y-1">
      <li
        v-for="playlist in playlists"
        :key="playlist.id"
        @click="loadPlaylist(playlist.id)"
        class="p-2 truncate hover:bg-[#003566] border border-[#cfcfcf] cursor-pointer rounded-lg transition-all duration-200 ease-in-out"
      >
        <span>{{ playlist.name }}</span>
      </li>
    </ul>

    <!-- YouTube URL Section -->
    <div class="mt-2 space-y-1">
      <input v-model="youtubeUrl" placeholder="Enter YouTube URL" class="px-3 py-2 outline-none font-semibold text-[#cfcfcf] rounded-lg shadow-md w-full bg-[#003566] placeholder:text-[#cfcfcf]" />
      <button @click="convertAndAddSong" class="p-2 bg-[#2298aa] text-[#001d3d] rounded-lg shadow-md hover:bg-[#247e8b] transition-all duration-300">Convert</button>
    </div>

    <!-- Modal for Add to Playlist -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div class="bg-white p-6 rounded-lg shadow-xl max-w-md w-full">
        <h2 class="text-xl text-[#03045e] font-semibold">Choose a Playlist</h2>
        <ul class="mt-2 space-y-2">
          <li
            v-for="playlist in availablePlaylists"
            :key="playlist.id"
            @click="addSongToPlaylist(currentSong!.id, playlist.id)"
            class="p-2 hover:bg-[#003566] border font-semibold border-[#15616d] hover:text-[#cfcfcf] text-[#15616d] cursor-pointer rounded-lg transition-all duration-300"
          >
            <span>{{ playlist.name }}</span>
          </li>
        </ul>
        <button @click="closeModal" class="mt-4 p-2 bg-[#15616d] text-white rounded-lg hover:bg-[#003566] transition-all duration-300">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Song, Playlist } from '../../types/index';
import { TrashIcon } from '@heroicons/vue/24/solid';

const songs = ref<Song[]>([]);
const playlists = ref<Playlist[]>([]);
const currentSong = ref<Song | null>(null);
const currentPlaylist = ref<Playlist | null>(null);
const youtubeUrl = ref('');
const playlistName = ref('');
const showModal = ref(false);
const availablePlaylists = ref<Playlist[]>([]);

onMounted(async() => {
  await fetchSongs();
  await fetchPlaylists();
});

// Fetch all songs
const fetchSongs = async() => {
  const response = await fetch('http://localhost:5000/songs');
  const data = await response.json();
  songs.value = data;
};

// Fetch all playlists
const fetchPlaylists = async() => {
  const response = await fetch('http://localhost:5000/playlists');
  const data = await response.json();
  playlists.value = data;
};

// Create a playlist
const createPlaylist = async() => {
  if (!playlistName.value) {
    alert('Please enter a playlist name');
    return;
  }

  try {
    const response = await fetch('http://localhost:5000/playlists', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: playlistName.value }),
    });

    if (!response.ok) {
      throw new Error('Failed to create playlist');
    }

    const playlist = await response.json();
    playlists.value.push(playlist);
    playlistName.value = '';  // Clear the input
  } catch (error) {
    alert('Error creating playlist');
  }
};

// Load a specific playlist
const loadPlaylist = async(playlistId: number) => {
  try {
    const response = await fetch(`http://localhost:5000/playlists/${playlistId}`);
    const playlist = await response.json();
    currentPlaylist.value = playlist;
    currentSong.value = null;
  } catch (error) {
    alert('Error loading playlist');
  }
};

// Go back to all songs view
const goBackToSongs = () => {
  currentPlaylist.value = null;
};

// Play a song
const playSong = (song: Song) => {
  currentSong.value = song;
};

const getPlaylistsWithoutSong = async(songId: number) => {
  try {
    const response = await fetch(`http://localhost:5000/playlists/without_song?song_id=${songId}`);
    const data = await response.json();
    return data;  // Returns playlists that do not contain the song
  } catch (error) {
    console.error('Error fetching playlists without song:', error);
    return [];
  }
};

// Show modal to add song to playlist
const showAddToPlaylistModal = async(song: Song) => {
  currentSong.value = song;
  showModal.value = true;
  availablePlaylists.value = await getPlaylistsWithoutSong(song.id);
};

// Close modal
const closeModal = () => {
  showModal.value = false;
};

// Add song to playlist
const addSongToPlaylist = async(songId: number, playlistId: number) => {
  try {
    const response = await fetch(`http://localhost:5000/playlists/${playlistId}/add`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ song_id: songId }),
    });

    if (response.ok) {
      alert('Song added to playlist');
      closeModal();
      loadPlaylist(playlistId);
    } else {
      throw new Error('Failed to add song to playlist');
    }
  } catch (error: any) {
    alert(error.message);
  }
};

// Remove song from playlist
const removeSongFromPlaylist = async(songId: number) => {
  if (!currentPlaylist.value) return;
  try {
    const response = await fetch(`http://localhost:5000/playlists/${currentPlaylist.value.id}/remove`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ song_id: songId }),
    });

    if (response.ok) {
      alert('Song removed from playlist');
      loadPlaylist(currentPlaylist.value.id);  // Reload the playlist
    } else {
      throw new Error('Failed to remove song from playlist');
    }
  } catch (error: any) {
    alert(error.message);
  }
};

// Convert YouTube URL to song
const convertAndAddSong = async() => {
  if (!youtubeUrl.value) {
    alert('Please enter a YouTube URL');
    return;
  }

  try {
    const response = await fetch('http://localhost:5000/songs/youtube', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ youtube_url: youtubeUrl.value }),
    });

    if (!response.ok) {
      throw new Error('Failed to convert and add song');
    }

    const song = await response.json();
    songs.value.push(song);
    youtubeUrl.value = '';  // Clear the input
  } catch (error) {
    alert('Error adding song');
  }
};
</script>
