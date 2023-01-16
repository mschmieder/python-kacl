import os
from pathlib import Path


def snapshot_directory(snapshot, directory_path, dir_excludes=[".git"], file_excludes=[], sanitize_callbacks={}):
    snapshot_dir = {}

    for root, dirs, files in os.walk(directory_path, topdown=True):
        dirs[:] = [d for d in dirs if d not in dir_excludes]

        for file in files:
            if file in file_excludes:
                continue
            current = snapshot_dir
            parts = Path(root).relative_to(directory_path).parts
            for part in parts:
                current = current.setdefault(part, {})

            file_path = os.path.join(root, f"{file}")
            if __is_binary(file_path):
                content = open(file_path, "rb").read()
            else:
                content = open(file_path, "r").read()

            if file in sanitize_callbacks:
                callback = sanitize_callbacks[file]
                content = callback(content)

            current[f"{file}.snap"] = content

    snapshot.assert_match_dir(snapshot_dir, "snapshots")


def __is_binary(file_path):
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F})
    return bool(open(file_path, "rb").read(1024).translate(None, textchars))
