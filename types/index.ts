export interface Song {
    id: number;
    title: string;
    artist: string;
    file_path: string;
}
  
export interface Playlist {
    id: number;
    name: string;
    songs: Song[];
}