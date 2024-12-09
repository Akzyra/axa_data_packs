import shutil

import pack_maker
import pack_maker.uncraft_stairs_slabs
import pack_maker.uncraft_storage_blocks

PREFIX = "az_"


def main():
    assets = pack_maker.JAR_FILES / "assets"
    data = pack_maker.JAR_FILES / "data"
    if not assets.exists() or not data.exists():
        raise FileNotFoundError(
            f"Missing unpacked JAR folder {pack_maker.JAR_FILES.absolute()}"
        )

    # regen packs
    pack_maker.uncraft_stairs_slabs.generate_pack()
    pack_maker.uncraft_storage_blocks.generate_pack()

    # create ZIP files
    pack_maker.DIST_FOLDER.mkdir(exist_ok=True)

    print("Packs:")
    for pack_dir in pack_maker.PACKS_FOLDER.iterdir():
        if (
            pack_dir.name.startswith(("_", "."))
            or not pack_dir.is_dir()
            or not (pack_dir / "pack.mcmeta").exists()
        ):
            continue

        file_path = pack_maker.DIST_FOLDER / f"{PREFIX}{pack_dir.name}"
        shutil.make_archive(file_path, format="zip", root_dir=pack_dir)
        print(f" - {pack_dir.name}")


main()
