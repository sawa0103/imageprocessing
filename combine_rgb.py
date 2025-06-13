"""Combine individual MicaSense band images into an RGB preview.

This standalone example does **not** depend on :mod:`micasense.capture` and
instead loads each band using :mod:`PIL.Image`.  Pixel values are normalised
to the ``[0, 1]`` range before being stacked into an RGB array which is then
gamma corrected and saved.  The script can be invoked from the command line
passing the three band filenames (blue, green and red).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

DEFAULT_BANDS = [
    Path("data/REDEDGE-MX/IMG_0001_1.tif"),
    Path("data/REDEDGE-MX/IMG_0001_2.tif"),
    Path("data/REDEDGE-MX/IMG_0001_3.tif"),
]


def load_band(path: Path) -> np.ndarray:
    """Load a single band image and normalise values to ``[0, 1]``."""
    with Image.open(path) as img:
        arr = np.array(img, dtype=np.float32)
    arr -= arr.min()
    if arr.max() > 0:
        arr /= arr.max()
    return arr


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "bands",
        metavar="BAND",
        nargs="*",
        type=Path,
        help="Paths to the blue, green and red band images",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("RGB_preview.jpg"),
        help="Output JPEG filename",
    )
    parser.add_argument(
        "--gamma",
        type=float,
        default=1.4,
        help="Gamma correction exponent",
    )
    args = parser.parse_args()
    if args.bands:
        if len(args.bands) != 3:
            parser.error("Specify exactly three band files (B, G, R)")
    else:
        args.bands = DEFAULT_BANDS
    return args


def main() -> None:
    args = parse_args()

    # Load bands in B, G, R order
    bands = [load_band(f) for f in args.bands]

    # Stack bands into an RGB array (R, G, B)
    rgb = np.stack([bands[2], bands[1], bands[0]], axis=-1)

    rgb_gamma = np.clip(rgb, 0, 1) ** (1 / args.gamma)

    rgb_uint8 = (rgb_gamma * 255).astype(np.uint8)
    Image.fromarray(rgb_uint8).save(args.output)
    print(f"Saved RGB image to {args.output}")


if __name__ == "__main__":
    main()
