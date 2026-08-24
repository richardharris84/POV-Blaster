"""Compare two image assets using the local Pixel-Harmony metrics."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from skimage.metrics import structural_similarity


def load_grayscale(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Unable to read image: {path}")
    return image


def compare(first: Path, second: Path) -> dict[str, float]:
    image_a = load_grayscale(first)
    image_b = load_grayscale(second)
    image_b = cv2.resize(image_b, (image_a.shape[1], image_a.shape[0]), interpolation=cv2.INTER_NEAREST)
    difference = image_a.astype(np.float64) - image_b.astype(np.float64)
    mse = float(np.mean(difference**2))
    return {
        "ssim": float(structural_similarity(image_a, image_b, data_range=255)),
        "mae": float(np.mean(np.abs(difference))),
        "rmse": float(np.sqrt(mse)),
        "psnr": float("inf") if mse == 0 else float(20 * np.log10(255 / np.sqrt(mse))),
        "histogram_correlation": float(cv2.compareHist(
            cv2.calcHist([image_a], [0], None, [256], [0, 256]),
            cv2.calcHist([image_b], [0], None, [256], [0, 256]),
            cv2.HISTCMP_CORREL,
        )),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    args = parser.parse_args()
    print(compare(args.first, args.second))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())