from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

DIST = Path('dist')


def walk(path: Path):
    for p in path.iterdir():
        yield p
        if p.is_dir():
            yield from walk(p)


def main():
    DIST.mkdir(exist_ok=True)

    for path in Path('').iterdir():
        if path.name.startswith(('_', '.')) or not path.is_dir() or not (path / 'pack.mcmeta').exists():
            continue

        pack_name = path.name
        print(f'zipping {pack_name}...', end='')

        z = ZipFile(DIST / f'axa_{pack_name}.zip', 'w', ZIP_DEFLATED)
        for p in walk(path):
            zip_path = p.relative_to(path)
            z.write(p, zip_path)

        print('\b\b\b DONE')


if __name__ == '__main__':
    main()
