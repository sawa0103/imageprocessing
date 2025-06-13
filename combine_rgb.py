"""Simple script to combine RedEdge band images into an RGB preview.

This example does not rely on the :mod:`micasense` package. Instead it loads
each monochrome band image with Pillow, normalizes the pixel values and
produces an RGB JPEG file using only ``numpy`` and ``Pillow``.
"""

import numpy as np
from PIL import Image

# Paths to the individual band images
BAND_FILES = [
    "data/REDEDGE-MX/IMG_0001_1.tif",
    "data/REDEDGE-MX/IMG_0001_2.tif",
    "data/REDEDGE-MX/IMG_0001_3.tif",
]

# Output RGB filename
OUTPUT_FILE = "IMG_0001_RGB.jpg"


def load_band(path: str) -> np.ndarray:
    """Load a single band image and normalize values to ``[0, 1]``."""
    with Image.open(path) as img:
        arr = np.array(img, dtype=np.float32)
    arr -= arr.min()
    if arr.max() > 0:
        arr /= arr.max()
    return arr


def main():
    # Load bands (assumed order: B, G, R)
    bands = [load_band(f) for f in BAND_FILES]

    # Stack bands into an RGB array (R, G, B)
    rgb = np.stack([bands[2], bands[1], bands[0]], axis=-1)

    # Apply a basic gamma correction so the image looks more natural
    gamma = 1.4
    rgb_gamma = np.clip(rgb, 0, 1) ** (1 / gamma)

    # Convert to 8‑bit and save using Pillow
    rgb_uint8 = (rgb_gamma * 255).astype(np.uint8)
    Image.fromarray(rgb_uint8).save(OUTPUT_FILE)
    print(f"Saved RGB image to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
