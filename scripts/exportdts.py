import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from common import ffmpeg_export, load_project

audio, output = load_project("build")

ffmpeg_export(audio, output + ".dts", "-c:a", "dca", "-strict", "experimental", "-b:a", "1509k")
