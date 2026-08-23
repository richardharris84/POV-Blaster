#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from urllib.request import urlretrieve
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
ENTRY_POINT = PROJECT_ROOT / 'main.py'
WEB_ENTRY_POINT = PROJECT_ROOT / 'web_main.py'
BUILD_DIR = PROJECT_ROOT / 'build'
WORK_DIR = BUILD_DIR / 'pyinstaller-work'
SPEC_DIR = BUILD_DIR / 'pyinstaller-spec'


def parse_args():
    parser = argparse.ArgumentParser(
        description='Build a POV-Blaster executable for the current platform.'
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument(
        '-w',
        '--windows',
        action='store_true',
        help='create a Windows-named executable: POV-Blaster_win.exe',
    )
    target.add_argument(
        '-l',
        '--linux',
        action='store_true',
        help='create a Linux-named executable: POV-Blaster_lin',
    )
    target.add_argument(
        '-m',
        '--macos',
        action='store_true',
        help='create a macOS application bundle: POV-Blaster_mac.app',
    )
    target.add_argument(
        '-b',
        '--web',
        action='store_true',
        help='build the browser version with Pygbag in build/web',
    )
    return parser.parse_args()


def build(target):
    if target == 'web':
        build_web()
        return

    import PyInstaller.__main__

    if target == 'windows' and sys.platform != 'win32':
        raise RuntimeError('The Windows build must run on Windows.')
    if target == 'linux' and sys.platform != 'linux':
        raise RuntimeError('The Linux build must run on Linux.')
    if target == 'macos' and sys.platform != 'darwin':
        raise RuntimeError('The macOS build must run on macOS.')

    if not ENTRY_POINT.is_file():
        raise FileNotFoundError(f'Entry point not found: {ENTRY_POINT}')

    resources = PROJECT_ROOT / 'resources'
    if not resources.is_dir():
        raise FileNotFoundError(f'Resource directory not found: {resources}')
    maps = PROJECT_ROOT / 'maps'
    if not maps.is_dir():
        raise FileNotFoundError(f'Map directory not found: {maps}')
    content = PROJECT_ROOT / 'content'
    if not content.is_dir():
        raise FileNotFoundError(f'Content directory not found: {content}')

    BUILD_DIR.mkdir(exist_ok=True)
    target_names = {
        'windows': 'POV-Blaster_win',
        'linux': 'POV-Blaster_lin',
        'macos': 'POV-Blaster_mac',
    }
    target_name = target_names[target]
    separator = ';' if sys.platform == 'win32' else ':'

    for directory in (WORK_DIR, SPEC_DIR):
        if directory.exists():
            shutil.rmtree(directory)

    PyInstaller.__main__.run([
        str(ENTRY_POINT),
        '--name', target_name,
        '--onefile',
        # not --windowed: main.py's CLI flow (player name prompt, theme menu, and
        # returning to the console after each round) needs a real console attached,
        # or input() raises "lost sys.stdin" in a --windowed/noconsole build.
        '--clean',
        '--noconfirm',
        '--distpath', str(BUILD_DIR),
        '--workpath', str(WORK_DIR),
        '--specpath', str(SPEC_DIR),
        '--add-data', f'{resources}{separator}resources',
        '--add-data', f'{maps}{separator}maps',
        '--add-data', f'{content}{separator}content',
    ])

    if target == 'windows':
        executable = BUILD_DIR / f'{target_name}.exe'
    elif target == 'macos':
        executable = BUILD_DIR / f'{target_name}.app'
    else:
        executable = BUILD_DIR / target_name
    print(f'Created: {executable}')
    print(f'Requested target: {target}')
    print(f'Build host: {sys.platform}')


def upgrade_web_audio(web_source):
    """WAV/MP3 playback is unreliable on pygbag/WASM: transcode to OGG Vorbis, which
    is the format the browser audio backend supports consistently. Keep each file's
    original channel count and sample rate at high quality; forcing everything down
    to mono/22000Hz (pygbag's own default) audibly degraded the higher-quality shotgun
    sound while leaving the already-low-quality effects unaffected."""
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as error:
        raise RuntimeError(
            "The 'imageio-ffmpeg' package is required to build the web target "
            "(pip install imageio-ffmpeg)."
        ) from error

    for audio_path in list(web_source.rglob('*.wav')) + list(web_source.rglob('*.mp3')):
        ogg_path = audio_path.with_suffix('.ogg')
        subprocess.run(
            [ffmpeg, '-y', '-i', str(audio_path), '-q:a', '8', str(ogg_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        audio_path.unlink()


def _require_replace(html, old, new, description):
    """str.replace() silently no-ops if `old` isn't found, which would let a Pygbag
    template change silently undo one of these fixes with no error and no test to
    catch it. Fail loudly instead."""
    if old not in html:
        raise RuntimeError(
            f"Web HTML patch failed: {description} -- expected substring not found. "
            "Pygbag's generated template may have changed; update apply_web_html_patches()."
        )
    return html.replace(old, new)


def _set_html_title(html, title):
    start = html.find('<title>')
    end = html.find('</title>')
    if start != -1 and end != -1 and end >= start:
        start += len('<title>')
        return html[:start] + title + html[end:]

    head_open = '<head>'
    head_index = html.find(head_open)
    if head_index != -1:
        insert_at = head_index + len(head_open)
        return html[:insert_at] + f'\n    <title>{title}</title>' + html[insert_at:]

    # Some tests intentionally use a minimal CSS-only template snippet with no
    # <head>/<title>; keep style patches working there while full generated HTML
    # still gets a deterministic browser title.
    return html


def apply_web_html_patches(html):
    """Pygbag's default template styling: recolor the loading box/background, and
    make the game canvas fill the whole browser window while preserving aspect ratio
    (letterboxed via object-fit) instead of stretching or being cropped."""
    html = _require_replace(
        html,
        '#infobox {\n            position: fixed; /* center relative to viewport */\n            background: green;\n            color: blue;',
        '#infobox {\n            position: fixed; /* center relative to viewport */\n            background: black;\n            color: white;',
        'recolor the loading box',
    )
    html = _require_replace(
        html,
        'background-color:powderblue;',
        'background-color: #d3d3d3;',
        'recolor the page background',
    )
    html = _require_replace(
        html,
        'body {\n            font-family: arial;\n            margin: 0;\n            padding: none;',
        'html {\n            width: 100%;\n            height: 100%;\n        }\n\n'
        '        body {\n            font-family: arial;\n            margin: 0;\n            padding: none;\n'
        '            width: 100%;\n            height: 100%;\n            overflow: hidden;',
        'make html/body fill the viewport',
    )
    html = _require_replace(
        html,
        '            width: 100%;\n            height: 100%;\n            z-index: 5;',
        '            width: 100%;\n            height: 100%;\n            object-fit: contain;\n            z-index: 5;',
        'preserve canvas aspect ratio via object-fit',
    )
    html = _set_html_title(html, 'POV Blaster')
    if 'Built by: Richard Harris' not in html and '</body>' in html:
        footer = (
            '\n<div style="position: fixed; bottom: 8px; right: 8px; '
            'z-index: 2147483647; font-family: Arial, sans-serif; font-size: 12px; '
            'background: rgba(0, 0, 0, 0.65); color: #fff; padding: 4px 8px; border-radius: 4px;">'
            'Built by: <a href="https://github.com/richardharris84/POV-Blaster" '
            'target="_blank" rel="noopener noreferrer" style="color: #fff; text-decoration: underline;">'
            'Richard Harris</a></div>\n'
        )
        html = _require_replace(
            html,
            '</body>',
            f'{footer}</body>',
            'inject built-by footer',
        )
    return html


def build_web():
    if not WEB_ENTRY_POINT.is_file():
        raise FileNotFoundError(f'Web entry point not found: {WEB_ENTRY_POINT}')

    web_dir = BUILD_DIR / 'web'
    web_dir.mkdir(parents=True, exist_ok=True)
    web_source = BUILD_DIR / 'web-source'
    if web_source.exists():
        shutil.rmtree(web_source)

    def ignore_web_files(directory, names):
        relative = Path(directory).relative_to(PROJECT_ROOT)
        ignored = {'build', '.git', '.pytest_cache', '__pycache__', 'scores.xml',
                   'docs', 'screenshots', 'tests', 'tools', 'generate_themes.ps1'}
        if relative == Path('.'):
            ignored.update({'resources/candy_kingdom', 'resources/space', 'resources/graveyard'})
        if relative == Path('resources'):
            ignored.update({'candy_kingdom', 'space', 'graveyard'})
        return ignored.intersection(names)

    shutil.copytree(
        PROJECT_ROOT,
        web_source,
        ignore=ignore_web_files,
    )
    upgrade_web_audio(web_source)
    (web_source / 'main.py').write_text(
        # pygbag statically scans this file's text for 'import pygame' to know which
        # WASM packages to preload, so keep that import literal even though unused here.
        "import asyncio\n\nimport pygame  # noqa: F401\n\nfrom web_main import main\n\nasyncio.run(main())\n",
        encoding='utf-8',
    )
    subprocess.run([
        sys.executable,
        '-m',
        'pygbag',
        '--build',
        '--ume_block=0',
        '--disable-sound-format-error',
        str(web_source),
    ], cwd=PROJECT_ROOT, check=True)
    # pygbag caches the html template and reuses it (without re-running build.py) whenever
    # `python -m pygbag build/web-source` is started as a dev server, so patch the cache
    # itself or the html fixes below won't survive a dev server restart.
    for cached_template in (web_source / 'build' / 'web-cache').glob('*.tmpl'):
        cached_template.write_text(
            apply_web_html_patches(cached_template.read_text(encoding='utf-8')),
            encoding='utf-8',
        )
    generated_web_dir = web_source / 'build' / 'web'
    if generated_web_dir.exists() and generated_web_dir != web_dir:
        if web_dir.exists():
            shutil.rmtree(web_dir)
        shutil.copytree(generated_web_dir, web_dir)
    browserfs = web_dir / 'browserfs.min.js'
    urlretrieve('https://cdn.jsdelivr.net/npm/browserfs@1.4.3/dist/browserfs.min.js', browserfs)
    index = web_dir / 'index.html'
    embedded_index = web_dir / 'web-source.html'
    if embedded_index.exists():
        shutil.copy2(embedded_index, index)
    index_html = index.read_text(encoding='utf-8').replace(
        'https://pygame-web.github.io/cdn/0.9.3//browserfs.min.js',
        'browserfs.min.js',
    )
    runtime_script = '<script src="https://pygame-web.github.io/cdn/0.9.3/pythons.js"'
    if not index_html.startswith('<script src="browserfs.min.js"></script>'):
        index_html = index_html.replace(
            runtime_script,
            '<script src="browserfs.min.js"></script>' + runtime_script,
            1,
        )
    index_html = apply_web_html_patches(index_html)
    index.write_text(index_html, encoding='utf-8')
    print(f'Created web build: {web_dir}')
    print('Serve with: python -m pygbag build/web-source')


def main():
    args = parse_args()
    target = (
        'windows' if args.windows else
        'linux' if args.linux else
        'macos' if args.macos else
        'web'
    )
    build(target)


if __name__ == '__main__':
    main()
