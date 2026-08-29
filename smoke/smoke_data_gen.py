"""
smoke_data_gen.py
-----------------
Creates a tiny fake Caltech-256-style dataset under ./smoke_data/
for CPU smoke-testing the PoisonSpot pipeline without a GPU.

Layout:
    smoke_data/
        000.class_a/  (30 random 128x128 JPEG images)
        001.class_b/
        002.class_c/
        003.class_d/
        004.class_e/

Run once:
    python smoke_data_gen.py
"""

import os
import random
import numpy as np
from PIL import Image

OUT_DIR    = "./smoke_data"
N_CLASSES  = 5
N_IMAGES   = 30   # per class  (150 total → 120 train / 30 test after 80/20 split)
IMG_SIZE   = 128  # pixels — larger than img_size=32 in config so resize doesn't upscale

random.seed(0)
np.random.seed(0)

class_names = [f"{i:03d}.class_{chr(ord('a') + i)}" for i in range(N_CLASSES)]

for cls in class_names:
    cls_dir = os.path.join(OUT_DIR, cls)
    os.makedirs(cls_dir, exist_ok=True)
    for j in range(N_IMAGES):
        arr = np.random.randint(0, 256, (IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8)
        img = Image.fromarray(arr, "RGB")
        img.save(os.path.join(cls_dir, f"img_{j:04d}.jpg"))

print(f"Created {N_CLASSES} classes × {N_IMAGES} images = {N_CLASSES * N_IMAGES} total")
print(f"Dataset root: {os.path.abspath(OUT_DIR)}")
