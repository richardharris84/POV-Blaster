#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import PyInstaller.__main__


PROJECT_ROOT = Path(__file__).resolve().parent
ENTRY_POINT = PROJECT_ROOT / 'main.py'
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
    return parser.parse_args()


def build(target):
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
        '--windowed',
        '--clean',
        '--noconfirm',
        '--distpath', str(BUILD_DIR),
        '--workpath', str(WORK_DIR),
        '--specpath', str(SPEC_DIR),
        '--add-data', f'{resources}{separator}resources',
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


def main():
    args = parse_args()
    target = 'windows' if args.windows else 'linux' if args.linux else 'macos'
    build(target)


if __name__ == '__main__':
    main()
