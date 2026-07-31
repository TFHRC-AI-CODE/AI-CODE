"""Verify the integrity of the public native model artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "src" / "flr_model" / "models"
MANIFEST_PATH = MODEL_DIR / "model_manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    failed = False
    for binder, details in manifest["models"].items():
        path = MODEL_DIR / details["file"]
        actual = sha256(path)
        expected = details["sha256"]
        status = "OK" if actual == expected else "FAILED"
        print(f"{status}: {binder} — {path.name}")
        if actual != expected:
            failed = True
            print(f"  expected: {expected}")
            print(f"  actual:   {actual}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

