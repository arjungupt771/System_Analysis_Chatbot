import os
import platform
from typing import Any, Dict, List


DEFAULT_ROOT = r"C:\\"
DEFAULT_MAX_FILES = 20
DEFAULT_MAX_DEPTH = 5

# Directories that can contain huge numbers of files or sensitive/system data.
SKIP_DIRECTORIES = {
    "$recycle.bin",
    "system volume information",
    "windows\\winsxs",
    "windows\\softwaredistribution",
    "windows\\temp",
}


def _should_skip_directory(path: str) -> bool:
    normalized = os.path.normcase(path).rstrip("\\/")
    lowered = normalized.lower()

    for skipped in SKIP_DIRECTORIES:
        if (
            lowered.endswith("\\" + skipped)
            or lowered.endswith("/" + skipped)
            or lowered == skipped
        ):
            return True

    return False


def _directory_depth(path: str, root: str) -> int:
    try:
        relative = os.path.relpath(path, root)

        if relative in (".", ""):
            return 0

        return len(relative.split(os.sep))
    except ValueError:
        return 0


def get_storage_analysis(
    root: str = DEFAULT_ROOT,
    max_files: int = DEFAULT_MAX_FILES,
    max_depth: int = DEFAULT_MAX_DEPTH,
) -> Dict[str, Any]:
    """
    Find the largest files on a Windows drive.

    The scan is intentionally bounded so that an AI command cannot
    accidentally trigger an unrestricted filesystem crawl.
    """

    if platform.system() != "Windows":
        return {
            "success": False,
            "error": "Storage analysis is currently supported on Windows only.",
            "files": [],
        }

    root = os.path.abspath(root)

    if not os.path.exists(root):
        return {
            "success": False,
            "error": f"Storage root does not exist: {root}",
            "files": [],
        }

    max_files = max(1, min(max_files, 100))
    max_depth = max(1, min(max_depth, 10))

    largest_files: List[Dict[str, Any]] = []
    scanned_files = 0
    skipped_files = 0

    for current_root, directories, filenames in os.walk(
        root,
        topdown=True,
    ):
        if _directory_depth(current_root, root) >= max_depth:
            directories[:] = []

        directories[:] = [
            directory
            for directory in directories
            if not _should_skip_directory(
                os.path.join(current_root, directory)
            )
        ]

        for filename in filenames:
            file_path = os.path.join(current_root, filename)

            try:
                size_bytes = os.path.getsize(file_path)
                scanned_files += 1

                largest_files.append(
                    {
                        "File": filename,
                        "Path": file_path,
                        "Size (MB)": round(
                            size_bytes / (1024 * 1024),
                            2,
                        ),
                        "Size (GB)": round(
                            size_bytes / (1024 * 1024 * 1024),
                            3,
                        ),
                    }
                )

            except (
                PermissionError,
                FileNotFoundError,
                OSError,
            ):
                skipped_files += 1

    largest_files.sort(
        key=lambda item: item["Size (MB)"],
        reverse=True,
    )

    largest_files = largest_files[:max_files]

    return {
        "success": True,
        "platform": "Windows",
        "root": root,
        "max_depth": max_depth,
        "scanned_files": scanned_files,
        "skipped_files": skipped_files,
        "showing": len(largest_files),
        "files": largest_files,
    }
