import os
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

img = Image.open(INP).convert("RGBA")

w, h = img.size

crop = (
    int(w * 0.24),
    int(h * 0.22),
    int(w * 0.76),
    int(h * 0.88)
)

img = img.crop(crop)

cut = remove(img)

rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1])

gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

clahe = cv2.createCLAHE(
    clipLimit=3.2,
    tileGridSize=(8, 8)
)

gray = clahe.apply(gray)

gray = cv2.convertScaleAbs(
    gray,
    alpha=1.15,
    beta=25
)

gray = cv2.detailEnhance(
    cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR),
    sigma_s=12,
    sigma_r=0.15
)

gray = cv2.cvtColor(
    gray,
    cv2.COLOR_BGR2GRAY
)

mask = alpha.astype(np.float32) / 255.0
mask = cv2.GaussianBlur(mask, (0, 0), 1.5)

out = gray.astype(np.float32) * mask + 255 * (1 - mask)

out = np.clip(out, 0, 255).astype(np.uint8)

Image.fromarray(out).save(OUT)

print("saved", OUT)