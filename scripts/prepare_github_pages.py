"""Validate static output and preserve literal legacy .html addresses for Pages."""
from pathlib import Path
import argparse
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]


def prepare(output: Path, source: Path = ROOT):
    if not (output / 'index.html').is_file():
        raise ValueError('Missing prerendered homepage; deployment refused.')
    if not (output / 'ads.txt').is_file():
        raise ValueError('Missing ads.txt; deployment refused.')
    if not (output / 'local-media').is_dir():
        raise ValueError('Use the standalone export with local media before deploying.')
    for path in output.rglob('*'):
        if path.is_file() and path.suffix in {'.html', '.js', '.css', '.json', '.webmanifest'}:
            if '/__l5e/assets-v1/' in path.read_text():
                raise ValueError(f'Unresolved Lovable media in {path}; deployment refused.')
    paths = set()
    for name in ('resource-manifest.json', 'legacy/manifest.json'):
        paths.update(json.loads((source / 'src/data' / name).read_text()))
    for path in sorted(paths):
        if not path.endswith('.html') or path == 'index.html':
            continue
        target = output / path
        if target.is_dir():
            html = (target / 'index.html').read_bytes()
            shutil.rmtree(target)
            target.write_bytes(html)
        elif not target.is_file():
            raise ValueError(f'Missing legacy page: {path}')
    # GitHub Pages serves this for unenumerated client routes (HTTP 404, not 200).
    shell = output / '_shell' / 'index.html'
    if not shell.is_file():
        raise ValueError('Missing TanStack SPA shell; deployment refused.')
    shutil.copyfile(shell, output / '404.html')
    (output / '.nojekyll').touch()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('dist/client'))
    args = parser.parse_args()
    prepare(args.output)
    print('Validated local media, ads.txt, legacy HTML pages, and client-route fallback.')