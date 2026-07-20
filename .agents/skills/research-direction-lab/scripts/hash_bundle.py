from hashlib import sha256
from pathlib import Path
from typing import Sequence


def hash_bundle(root: Path, paths: Sequence[Path]) -> dict[str, str]:
    try:
        resolved_root = Path(root).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ValueError("invalid root") from exc
    if not resolved_root.is_dir():
        raise ValueError("root must be a directory")

    files: dict[str, Path] = {}
    for supplied in paths:
        candidate = Path(supplied)
        if ".." in candidate.parts:
            raise ValueError("path traversal is not allowed")
        target = candidate if candidate.is_absolute() else resolved_root / candidate
        try:
            resolved_target = target.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise ValueError("path does not resolve to a file") from exc
        if not resolved_target.is_relative_to(resolved_root):
            raise ValueError("path escapes root")
        if not resolved_target.is_file():
            raise ValueError("path must be a regular file")

        relative = resolved_target.relative_to(resolved_root).as_posix()
        if relative in files:
            raise ValueError("duplicate resolved path")
        files[relative] = resolved_target

    return {
        relative: sha256(files[relative].read_bytes()).hexdigest()
        for relative in sorted(files)
    }
