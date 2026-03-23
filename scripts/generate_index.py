"""Generate dist/index.json for Blender's extension repository format."""

import hashlib
import json
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = REPO_ROOT / "blender_manifest.toml"
DIST_DIR = REPO_ROOT / "dist"
INDEX_PATH = DIST_DIR / "index.json"


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    with MANIFEST_PATH.open("rb") as f:
        manifest = tomllib.load(f)

    ext_id = manifest["id"]
    version = manifest["version"]
    zip_name = f"{ext_id}-{version}.zip"
    zip_path = DIST_DIR / zip_name

    if not zip_path.exists():
        print(f"ERROR: expected zip not found: {zip_path}", file=sys.stderr)
        sys.exit(1)

    archive_hash = f"sha256:{sha256_of_file(zip_path)}"

    entry = {
        "id": ext_id,
        "name": manifest["name"],
        "tagline": manifest["tagline"],
        "version": version,
        "type": manifest["type"],
        "archive_url": f"./{zip_name}",
        "archive_hash": archive_hash,
        "blender_version_min": manifest["blender_version_min"],
        "license": manifest["license"],
        "platforms": manifest.get("platforms", []),
        "maintainer": manifest["maintainer"],
    }

    if INDEX_PATH.exists():
        with INDEX_PATH.open() as f:
            index = json.load(f)
    else:
        index = {"version": "v1", "blocklist": [], "data": []}

    data = index.setdefault("data", [])
    for i, item in enumerate(data):
        if item.get("id") == ext_id:
            data[i] = entry
            break
    else:
        data.append(entry)

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with INDEX_PATH.open("w") as f:
        json.dump(index, f, indent=2)
        f.write("\n")

    print(f"Wrote {INDEX_PATH}")


if __name__ == "__main__":
    main()
