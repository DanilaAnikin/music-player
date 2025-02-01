import sys
import yt_dlp as youtube_dl

ydl_opts_mp3 = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "320",
    }],
    "outtmpl": "music/%(title)s.%(ext)s",
}

def download_video(url):
    with youtube_dl.YoutubeDL(ydl_opts_mp3) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert.py <youtube_url>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    download_video(youtube_url)