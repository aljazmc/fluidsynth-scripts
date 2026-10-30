import os
import sys

import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from common import load_project

audio, output = load_project("npy")

np.save(output + ".npy", audio)
