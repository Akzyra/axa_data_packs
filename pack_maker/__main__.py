import pack_maker

if not pack_maker.JAR_FILES.exists():
    raise FileNotFoundError("Missing unpacked JAR folder")

print("Packs:")
for entry in pack_maker.PACKS_FOLDER.iterdir():
    if entry.is_dir():
        print(f" - {entry.name}")
