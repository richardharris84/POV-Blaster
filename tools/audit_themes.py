"""Audit theme image assets against the project's Default theme baseline.

Usage:
    py -3 tools/audit_themes.py
    py -3 tools/audit_themes.py --themes-dir resources --output build/theme_audit.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageStat

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
DEFAULT_THEME = "default"
REQUIRED_UI_SIZES = {
    "textures/blood_screen.png": [1600, 900],
    "textures/game_over.png": [1600, 900],
    "textures/sky.png": [1200, 400],
    "textures/win.png": [1920, 1080],
}
REQUIRED_ANIMATIONS = {"idle": 1, "walk": 4, "attack": 2, "pain": 2, "death": 6}


def analyze_image(filepath: Path) -> dict:
    with Image.open(filepath) as image:
        rgba = image.convert("RGBA")
        stat = ImageStat.Stat(rgba)
        red, green, blue, _ = stat.mean
        brightness = 0.299 * red + 0.587 * green + 0.114 * blue
        alpha = rgba.getchannel("A")
        alpha_extrema = alpha.getextrema()
        return {
            "size": list(image.size),
            "aspect_ratio": round(image.size[0] / image.size[1], 2),
            "colors_count": len(image.convert("RGB").getcolors(maxcolors=100000) or []),
            "has_alpha": "A" in image.mode,
            "alpha_extrema": list(alpha_extrema),
            "avg_brightness": round(brightness, 2),
            "bbox": list(rgba.getbbox()) if rgba.getbbox() else None,
            "sha256": hashlib.sha256(filepath.read_bytes()).hexdigest(),
        }


def collect_theme(theme_path: Path) -> dict[str, dict]:
    assets = {}
    for filepath in sorted(theme_path.rglob("*")):
        if filepath.is_file() and filepath.suffix.lower() in IMAGE_SUFFIXES:
            assets[str(filepath.relative_to(theme_path)).replace("\\", "/")] = analyze_image(filepath)
    return assets


def build_comparison(report: dict[str, dict[str, dict]], default_theme: str) -> dict:
    baseline = report.get(default_theme, {})
    comparisons = {}
    for theme, assets in report.items():
        if theme == default_theme:
            continue
        missing = sorted(set(baseline) - set(assets))
        extra = sorted(set(assets) - set(baseline))
        size_mismatches = []
        brightness_outliers = []
        for relative_path in sorted(set(baseline) & set(assets)):
            expected = baseline[relative_path]
            actual = assets[relative_path]
            if actual["size"] != expected["size"]:
                size_mismatches.append({"path": relative_path, "default": expected["size"], "theme": actual["size"]})
            if abs(actual["avg_brightness"] - expected["avg_brightness"]) > 100:
                brightness_outliers.append({"path": relative_path, "default": expected["avg_brightness"], "theme": actual["avg_brightness"]})
        comparisons[theme] = {
            "missing_assets": missing,
            "extra_assets": extra,
            "size_mismatches": size_mismatches,
            "brightness_outliers": brightness_outliers,
        }
    return comparisons


def build_quality_checks(report: dict[str, dict[str, dict]]) -> dict:
    checks = {}
    for theme, assets in report.items():
        duplicate_animation_frames = []
        blank_assets = []
        for relative_path, metadata in assets.items():
            if metadata["bbox"] is None:
                blank_assets.append(relative_path)
        animation_groups = defaultdict(list)
        for relative_path, metadata in assets.items():
            path = Path(relative_path)
            if path.parent.name in {"idle", "walk", "attack", "pain", "death"}:
                animation_groups[str(path.parent)].append((relative_path, metadata["sha256"]))
        for animation_path, frames in animation_groups.items():
            hashes = defaultdict(list)
            for relative_path, image_hash in frames:
                hashes[image_hash].append(relative_path)
            for duplicate_frames in hashes.values():
                if len(duplicate_frames) > 1:
                    duplicate_animation_frames.append(duplicate_frames)
        checks[theme] = {
            "image_count": len(assets),
            "blank_assets": sorted(blank_assets),
            "duplicate_animation_frames": sorted(duplicate_animation_frames),
        }
    return checks


def build_required_asset_checks(themes_dir: Path, report: dict[str, dict[str, dict]]) -> dict:
    checks = {}
    for theme, assets in report.items():
        theme_root = themes_dir / theme
        missing_assets = []
        invalid_dimensions = []
        blank_assets = []
        clipped_assets = []
        missing_animation_folders = []

        required_paths = list(REQUIRED_UI_SIZES) + [f"textures/{index}.png" for index in range(1, 6)]
        required_paths += [f"textures/digits/{index}.png" for index in range(11)]
        for required_path in required_paths:
            if required_path not in assets:
                missing_assets.append(required_path)

        for relative_path, expected_size in REQUIRED_UI_SIZES.items():
            metadata = assets.get(relative_path)
            if metadata and metadata["size"] != expected_size:
                invalid_dimensions.append({"path": relative_path, "expected": expected_size, "actual": metadata["size"]})

        for relative_path, metadata in assets.items():
            if metadata["bbox"] is None:
                blank_assets.append(relative_path)
            width, height = metadata["size"]
            bbox = metadata["bbox"]
            if bbox and (bbox[0] <= 0 or bbox[1] <= 0 or bbox[2] >= width or bbox[3] >= height):
                if "/npc/" in f"/{relative_path}" and "/death/" not in relative_path:
                    clipped_assets.append(relative_path)

        npc_root = theme_root / "sprites" / "npc"
        if npc_root.is_dir():
            for npc_dir in sorted(path for path in npc_root.iterdir() if path.is_dir()):
                for animation, minimum in REQUIRED_ANIMATIONS.items():
                    animation_dir = npc_dir / animation
                    frames = sorted(animation_dir.glob("*.png")) if animation_dir.is_dir() else []
                    if len(frames) < minimum:
                        missing_animation_folders.append({
                            "npc": npc_dir.name,
                            "animation": animation,
                            "minimum_frames": minimum,
                            "actual_frames": len(frames),
                        })
        else:
            missing_animation_folders.append({"npc_root": "sprites/npc"})

        checks[theme] = {
            "missing_assets": sorted(missing_assets),
            "invalid_dimensions": invalid_dimensions,
            "blank_assets": sorted(blank_assets),
            "clipped_assets": sorted(clipped_assets),
            "missing_animation_folders": missing_animation_folders,
        }
    return checks


def generate_report(themes_dir: Path, default_theme: str) -> dict:
    report = {}
    for theme_path in sorted(themes_dir.iterdir()):
        if theme_path.is_dir():
            report[theme_path.name] = collect_theme(theme_path)
    required_asset_checks = build_required_asset_checks(themes_dir, report)
    quality_checks = build_quality_checks(report)
    theme_status = {}
    for theme in report:
        quality = quality_checks[theme]
        required = required_asset_checks[theme]
        theme_status[theme] = {
            "passed": not quality["blank_assets"] and not quality["duplicate_animation_frames"] and not any(required.values()),
            "required_asset_checks": required,
            "quality_checks": {
                "blank_assets": quality["blank_assets"],
                "duplicate_animation_frames": quality["duplicate_animation_frames"],
            },
        }
    return {
        "themes_dir": str(themes_dir),
        "default_theme": default_theme,
        "themes": report,
        "quality_checks": quality_checks,
        "required_asset_checks": required_asset_checks,
        "theme_status": theme_status,
        "comparisons_to_default": build_comparison(report, default_theme),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--themes-dir", type=Path, default=Path(__file__).resolve().parents[1] / "resources")
    parser.add_argument("--default-theme", default=DEFAULT_THEME)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "build" / "theme_audit.json")
    parser.add_argument("--check", action="store_true", help="exit nonzero when blank assets or duplicate animation frames are found")
    args = parser.parse_args()

    if not args.themes_dir.is_dir():
        parser.error(f"Theme directory does not exist: {args.themes_dir}")

    report = generate_report(args.themes_dir, args.default_theme)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Theme audit generated: {args.output}")
    for theme, result in report["quality_checks"].items():
        print(f"{theme}: {result['image_count']} images, {len(result['blank_assets'])} blank, {len(result['duplicate_animation_frames'])} duplicate animation groups")
    if args.check:
        failures = []
        for theme, result in report["quality_checks"].items():
            if theme == args.default_theme:
                continue
            required = report["required_asset_checks"][theme]
            if result["blank_assets"] or result["duplicate_animation_frames"] or any(required.values()):
                failures.append(
                    f"{theme}: blank={len(result['blank_assets'])}, "
                    f"duplicate_animation_groups={len(result['duplicate_animation_frames'])}, "
                    f"required_failures={sum(len(value) for value in required.values())}"
                )
        if failures:
            print("Theme audit failed:")
            print("\n".join(failures))
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
