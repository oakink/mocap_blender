import importlib
import os
from figo_common import path

dir = path.STARTUP_PATH

for f in os.listdir(dir):
    path = os.path.join(dir, f)
    if os.path.isdir(path):
        importlib.import_module(f)