import sys
import difflib
from pathlib import Path


def main() -> None:
    # Expect: makepatch.py OLD_FILE NEW_FILE PATCH_FILE
    if len(sys.argv) != 4:
        print("Usage: makepatch.py OLD_FILE NEW_FILE PATCH_FILE")
        sys.exit(1)

    old_path = Path(sys.argv[1])
    new_path = Path(sys.argv[2])
    patch_path = Path(sys.argv[3])

    old_lines = old_path.read_text(encoding="utf-8").splitlines(keepends=True)
    new_lines = new_path.read_text(encoding="utf-8").splitlines(keepends=True)

    diff_lines = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"a/{old_path.name}",
        tofile=f"b/{new_path.name}",
        n=3,
    )

    normalized = []
    for line in diff_lines:
        if not line.endswith("\n"):
            line = line + "\n"
        normalized.append(line)

    patch_text = "".join(normalized)

    patch_path.write_text(patch_text, encoding="utf-8", newline="\r\n")


if __name__ == "__main__":
    main()


