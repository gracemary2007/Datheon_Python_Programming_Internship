"""Task 3: Automated File Organizer & Cleanup Utility.

Usage:
    python organizer.py <folder>            # organize the folder
    python organizer.py <folder> --dry-run  # preview only, move nothing
"""
import argparse
import logging
import shutil
from pathlib import Path

CATEGORIES = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv", ".md"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".wmv"},
    "Audio": {".mp3", ".wav", ".aac", ".flac"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".json", ".sql"},
}


def category_for(ext):
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return "Others"


def unique_path(dest):
    """If dest exists, return 'name (1).ext', 'name (2).ext', ..."""
    if not dest.exists():
        return dest
    i = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({i}){dest.suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def organize(folder, dry_run=False):
    moved = 0
    errors = 0
    counts = {}
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name == Path(__file__).name:
            continue
        category = category_for(item.suffix.lower())
        target_dir = folder / category
        try:
            dest = unique_path(target_dir / item.name)
            if dry_run:
                logging.info("[DRY RUN] %s -> %s/%s", item.name, category, dest.name)
            else:
                target_dir.mkdir(exist_ok=True)
                shutil.move(str(item), str(dest))
                logging.info("Moved %s -> %s/%s", item.name, category, dest.name)
            moved += 1
            counts[category] = counts.get(category, 0) + 1
        except PermissionError:
            logging.error("Permission denied: %s", item.name)
            errors += 1
        except (FileExistsError, OSError) as e:
            logging.error("Could not move %s: %s", item.name, e)
            errors += 1
    return moved, errors, counts


def main():
    parser = argparse.ArgumentParser(description="Organize files into category folders.")
    parser.add_argument("folder", help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving files")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        raise SystemExit(f"Error: '{folder}' is not a valid folder.")

    moved, errors, counts = organize(folder, args.dry_run)
    print("\n===== SUMMARY =====")
    print(f"Folder: {folder}")
    print(f"Files {'to move' if args.dry_run else 'moved'}: {moved}")
    for cat, n in sorted(counts.items()):
        print(f"  {cat}: {n}")
    print(f"Errors: {errors}")


if __name__ == "__main__":
    main()
