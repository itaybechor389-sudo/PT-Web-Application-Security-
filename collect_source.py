#!/usr/bin/env python3
"""Collect an allowlisted source snapshot for private review, not automatic publication."""
import argparse
from pathlib import Path
import zipfile


def collect(source, output):
    source = source.resolve(strict=True)
    if output.exists():
        raise FileExistsError(f'Refusing to overwrite: {output}')
    files = []
    for name in ('app.py', 'auth.py', 'db.py', 'wsgi.py', 'requirements.txt', 'pyproject.toml'):
        candidate = source / name
        if candidate.is_file() and not candidate.is_symlink():
            files.append(candidate)
    for dirname, extensions in [('templates', {'.html'}), ('static', {'.css', '.js'})]:
        directory = source / dirname
        if directory.is_dir() and not directory.is_symlink():
            for candidate in directory.rglob('*'):
                relative = candidate.relative_to(source)
                if any((source.joinpath(*relative.parts[:n])).is_symlink()
                       for n in range(1, len(relative.parts) + 1)):
                    continue
                if candidate.is_file() and candidate.suffix.lower() in extensions:
                    files.append(candidate)
    if not files:
        raise ValueError('No allowlisted source files found')
    for candidate in files:
        if candidate.stat().st_size > 2 * 1024 * 1024:
            raise ValueError(f'Unexpectedly large source file: {candidate.name}')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', zipfile.ZIP_DEFLATED) as archive:
        for candidate in sorted(files):
            archive.write(candidate, candidate.relative_to(source).as_posix())
    print(f'Created: {output}')
    print('Included:')
    for candidate in sorted(files):
        print('  ' + candidate.relative_to(source).as_posix())
    print('Review code for hardcoded credentials before publication. This tool does not sanitize code.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Application folder on Kali')
    parser.add_argument('--output', type=Path, default=Path.home() / 'pt-web-lab-source-review.zip')
    args = parser.parse_args()
    collect(args.source, args.output)
