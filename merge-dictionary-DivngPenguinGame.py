import json
import string
from pathlib import Path

# Folder containing dictionary-A.json ... dictionary-Z.json
INPUT_FOLDER = Path(".")

# Output file
OUTPUT_FILE = Path("dictionary.json")

merged = {}

for letter in string.ascii_uppercase:
    filename = INPUT_FOLDER / f"dictionary-{letter}.json"

    if not filename.exists():
        print(f"[SKIP] {filename} not found")
        continue

    print(f"[LOAD] {filename}")

    try:
        with filename.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print(f"[ERROR] {filename} does not contain a JSON object")
            continue

        # Detect duplicate words
        duplicates = set(merged) & set(data)

        if duplicates:
            print(
                f"[WARNING] {filename} contains "
                f"{len(duplicates)} duplicate key(s)"
            )

        # Later files overwrite duplicate keys from earlier files
        merged.update(data)

    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in {filename}: {e}")

    except OSError as e:
        print(f"[ERROR] Could not read {filename}: {e}")


# Write combined dictionary
with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(
        merged,
        f,
        ensure_ascii=False,
        indent=2
    )

print()
print(f"Done!")
print(f"Total dictionary entries: {len(merged):,}")
print(f"Output: {OUTPUT_FILE.resolve()}")
