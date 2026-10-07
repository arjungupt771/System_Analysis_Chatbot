import os
import platform
from typing import Any, Dict, List

import psutil


def _safe_username(process) -> str:
    try:
        return process.username()
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return "N/A"


def _safe_memory(process) -> float:
    try:
        return round(process.memory_info().rss / (1024 * 1024), 2)
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return 0.0


def _safe_status(process) -> str:
    try:
        return process.status()
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return "unknown"


def get_process_analysis(
    limit: int = 10,
    sort_by: str = "cpu",
) -> Dict[str, Any]:
    """
    Analyze currently running Windows processes.

    Args:
        limit: Maximum number of processes to return.
        sort_by: "cpu" or "memory".

    Returns:
        Dictionary containing process information and summary data.
    """

    if platform.system() != "Windows":
        return {
            "success": False,
            "error": "Process analysis is currently supported on Windows only.",
            "processes": [],
        }

    limit = max(1, min(limit, 50))

    processes: List[Dict[str, Any]] = []

    for process in psutil.process_iter(
        ["pid", "name", "status"]
    ):
        try:
            # Take a short CPU sample.
            cpu_percent = process.cpu_percent(interval=0.1)

            memory_mb = _safe_memory(process)

            process_data = {
                "Name": process.info.get("name") or "Unknown",
                "PID": process.info.get("pid"),
                "CPU %": round(cpu_percent, 2),
                "Memory (MB)": memory_mb,
                "Status": _safe_status(process),
                "User": _safe_username(process),
            }

            processes.append(process_data)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    if sort_by.lower() == "memory":
        processes.sort(
            key=lambda item: item["Memory (MB)"],
            reverse=True,
        )
    else:
        processes.sort(
            key=lambda item: item["CPU %"],
            reverse=True,
        )

    selected_processes = processes[:limit]

    return {
        "success": True,
        "platform": "Windows",
        "total_processes": len(processes),
        "showing": len(selected_processes),
        "sort_by": sort_by.lower(),
        "processes": selected_processes,
    }


def get_top_cpu_processes(limit: int = 10) -> Dict[str, Any]:
    """Return processes consuming the most CPU."""

    return get_process_analysis(
        limit=limit,
        sort_by="cpu",
    )


def get_top_memory_processes(limit: int = 10) -> Dict[str, Any]:
    """Return processes consuming the most memory."""

    return get_process_analysis(
        limit=limit,
        sort_by="memory",
    )
