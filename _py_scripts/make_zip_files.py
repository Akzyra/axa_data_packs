from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

DIST = Path('../dist')


def walk(path: Path):
    for p in path.iterdir():
        yield p
        if p.is_dir():
            yield from walk(p)


if __name__ == '__main__':
    DIST.mkdir(exist_ok=True)

    for path in Path('..').iterdir():
        if path.name.startswith(('_', '.')) or not path.is_dir() or not (path / 'pack.mcmeta').exists():
            continue

        print(f'zipping {path.name}...', end='')

        pack_name = path.name
        z = ZipFile(DIST / f'{pack_name}.zip', 'w', ZIP_DEFLATED)
        for p in walk(path):
            zip_path = p.relative_to(path)
            z.write(p, zip_path)

        print('\b\b\b DONE')
