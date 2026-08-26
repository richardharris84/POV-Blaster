#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from urllib.request import urlretrieve
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
ENTRY_POINT = PROJECT_ROOT / 'main.py'
SRC_DIR = PROJECT_ROOT / 'src'
WEB_ENTRY_POINT = SRC_DIR / 'application' / 'web_main.py'
BUILD_DIR = PROJECT_ROOT / 'build'
WORK_DIR = BUILD_DIR / 'pyinstaller-work'
SPEC_DIR = BUILD_DIR / 'pyinstaller-spec'


def parse_args():
    parser = argparse.ArgumentParser(
        description='Build or deploy POV-Blaster for the current platform.'
    )
    target = parser.add_mutually_exclusive_group()
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
    parser.add_argument(
        '-d',
        '--deploy',
        action='store_true',
        help='deploy the browser build to the GitHub Pages gh-pages branch',
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

    assets = PROJECT_ROOT / 'assets'
    if not assets.is_dir():
        raise FileNotFoundError(f'Asset directory not found: {assets}')

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
        '--paths', str(SRC_DIR),
        '--add-data', f'{assets}{separator}assets',
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
        'background-color: #000000;',
        'set the page background to black',
    )
    html = _require_replace(
        html,
        'platform.document.body.style.background = "#7f7f7f"',
        'platform.document.body.style.background = "#000000"',
        'set the runtime page background to black',
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
        '            width: 100%;\n            height: 100%;\n            object-fit: fill;\n            z-index: 5;',
        'fill the browser viewport edge to edge',
    )
    html = _set_html_title(html, 'POV Blaster')
    if '</body>' in html:
        if 'document.title = "POV Blaster"' not in html:
            title_script = (
                '\n<script>\n'
                '  document.title = "POV Blaster";\n'
                '</script>\n'
            )
            html = html.replace('</body>', f'{title_script}</body>', 1)
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
        ignored = {'build', '.git', '.pytest_cache', '__pycache__', 'data', 'logs',
               'docs', 'screenshots', 'tests', 'tools'}
        return ignored.intersection(names)

    shutil.copytree(
        PROJECT_ROOT,
        web_source,
        ignore=ignore_web_files,
    )
    web_settings = web_source / 'src' / 'infrastructure' / 'settings.py'
    configured_api_url = repr(os.environ.get('POV_BLASTER_API_URL', '').rstrip('/'))
    settings_text = web_settings.read_text(encoding='utf-8')
    settings_text = settings_text.replace(
        "SCORE_API_URL = os.environ.get('POV_BLASTER_API_URL', '').rstrip('/')",
        f'SCORE_API_URL = {configured_api_url}',
    )
    web_settings.write_text(settings_text, encoding='utf-8')
    upgrade_web_audio(web_source)
    (web_source / 'main.py').write_text(
        # pygbag statically scans this file's text for 'import pygame' to know which
        # WASM packages to preload, so keep that import literal even though unused here.
        "import asyncio\nimport sys\nfrom pathlib import Path\n\nimport pygame  # noqa: F401\n\nsrc = Path(__file__).resolve().parent / 'src'\nif str(src) not in sys.path:\n    sys.path.insert(0, str(src))\n\nfrom application.web_main import main\n\nasyncio.run(main())\n",
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
    staged_browserfs = generated_web_dir / 'browserfs.min.js'
    urlretrieve('https://cdn.jsdelivr.net/npm/browserfs@1.4.3/dist/browserfs.min.js', staged_browserfs)
    shutil.copy2(PROJECT_ROOT / 'assets' / 'icon.png', generated_web_dir / 'favicon.png')
    if generated_web_dir.exists() and generated_web_dir != web_dir:
        if web_dir.exists():
            shutil.rmtree(web_dir)
        shutil.copytree(generated_web_dir, web_dir)
    browserfs = web_dir / 'browserfs.min.js'
    if not browserfs.exists():
        shutil.copy2(staged_browserfs, browserfs)
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
    shutil.copy2(PROJECT_ROOT / 'privacy.html', web_dir / 'privacy.html')
    print(f'Created web build: {web_dir}')
    print('Serve with: python -m pygbag build/web-source')


def deploy_to_github_pages(source_dir: Path | None = None):
    source_dir = source_dir or (BUILD_DIR / 'web')
    if not source_dir.exists():
        raise FileNotFoundError(
            'No browser build was found at build/web. Run "py build.py -bd" to build and deploy it.'
        )

    remote_url = subprocess.run(
        ['git', 'remote', 'get-url', 'origin'],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    branch = 'gh-pages'

    with tempfile.TemporaryDirectory(prefix='pov-blaster-pages-') as temporary_dir:
        deploy_dir = Path(temporary_dir) / 'site'
        clone = subprocess.run(
            ['git', 'clone', '--quiet', '--branch', branch, remote_url, str(deploy_dir)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        if clone.returncode != 0:
            subprocess.run(['git', 'clone', '--quiet', remote_url, str(deploy_dir)], cwd=PROJECT_ROOT, check=True)
            subprocess.run(['git', 'switch', '--orphan', branch], cwd=deploy_dir, check=True, stdout=subprocess.DEVNULL)

        for child in deploy_dir.iterdir():
            if child.name == '.git':
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

        for child in source_dir.iterdir():
            destination = deploy_dir / child.name
            if child.is_dir():
                shutil.copytree(child, destination)
            else:
                shutil.copy2(child, destination)

        (deploy_dir / '.nojekyll').write_text('', encoding='utf-8')
        subprocess.run(['git', 'add', '--all'], cwd=deploy_dir, check=True)
        subprocess.run(['git', 'commit', '-m', 'Deploy GitHub Pages'], cwd=deploy_dir, check=True)
        subprocess.run(['git', 'push', '--force', 'origin', branch], cwd=deploy_dir, check=True)
    print(f'Published {source_dir} to GitHub Pages via the {branch} branch.')


def main():
    args = parse_args()
    if not any([args.windows, args.linux, args.macos, args.web]) and not args.deploy:
        raise SystemExit('No build target specified. Use -w, -l, -m, -b, or -d.')

    if args.web:
        build('web')

    if args.deploy:
        deploy_to_github_pages(BUILD_DIR / 'web' if (BUILD_DIR / 'web').exists() else None)

    if args.windows:
        build('windows')
    elif args.linux:
        build('linux')
    elif args.macos:
        build('macos')


if __name__ == '__main__':
    main()

