import yt_dlp

def download(url, fmt):
    ydl_opts = {
        'format': fmt,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
