import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from common import RATE, ffmpeg_export, load_project

audio, output = load_project("build")

# 640x360 video at 15 fps: a scrolling spectrogram above the waveform, with
# AAC audio
WIDTH, HEIGHT, FPS = 640, 360, 15
AUDIO_KBPS = 96
# the video bitrate is capped so the file stays under about this many MB,
# though never below VIDEO_KBPS_MIN, so very long projects grow beyond it
MAX_MB = 4.5
VIDEO_KBPS_MIN, VIDEO_KBPS_MAX = 100, 1000

seconds = len(audio) / RATE
video_kbps = MAX_MB * 8000 / seconds - AUDIO_KBPS
video_kbps = round(min(max(video_kbps, VIDEO_KBPS_MIN), VIDEO_KBPS_MAX))

spectrum = HEIGHT * 2 // 3
video = (
    "[0:a]asplit[a][s];"
    "[s]asplit[s1][s2];"
    f"[s1]showspectrum=s={WIDTH}x{spectrum}:slide=scroll:mode=combined"
    ":color=magma:scale=log:drange=60:fscale=log:win_func=hann:overlap=0.75"
    f",fps={FPS}[spec];"
    f"[s2]showwaves=s={WIDTH}x{HEIGHT - spectrum}:mode=cline:rate={FPS}"
    ":split_channels=1:colors=0x00e5ff|0xff2bd6:draw=full[wave];"
    "[spec][wave]vstack,format=yuv420p[v]"
)

ffmpeg_export(
    audio, output + ".mp4",
    "-filter_complex", video, "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-tune", "animation",
    "-maxrate", f"{video_kbps}k", "-bufsize", f"{video_kbps}k",
    "-c:a", "aac", "-b:a", f"{AUDIO_KBPS}k", "-movflags", "+faststart",
    "-shortest",
)
