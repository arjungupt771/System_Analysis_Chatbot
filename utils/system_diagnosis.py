import json


def build_system_snapshot(
    hardware_details,
    system_apps,
    downloaded_apps,
    system_total,
    downloaded_total,
):
    """
    Build a structured snapshot of the system for AI analysis.
    """

    return {
        "hardware": hardware_details,
        "software": {
            "system_app_count": len(system_apps),
            "downloaded_app_count": len(downloaded_apps),
            "system_app_storage_bytes": system_total,
            "downloaded_app_storage_bytes": downloaded_total,
        },
        "applications": {
            "system_apps": system_apps,
            "downloaded_apps": downloaded_apps,
        },
    }


def _classify_cpu_usage(cpu_usage):
    """Classify CPU utilization."""

    if not isinstance(cpu_usage, (int, float)):
        return {
            "value": None,
            "status": "unknown",
            "reason": "CPU usage data unavailable.",
        }

    if cpu_usage < 50:
        status = "healthy"
    elif cpu_usage < 80:
        status = "elevated"
    else:
        status = "high"

    return {
        "value": round(cpu_usage, 1),
        "status": status,
    }


def _classify_ram_usage(ram_usage):
    """Classify RAM utilization."""

    if not isinstance(ram_usage, (int, float)):
        return {
            "value": None,
            "status": "unknown",
            "reason": "RAM usage data unavailable.",
        }

    if ram_usage < 70:
        status = "healthy"
    elif ram_usage < 85:
        status = "elevated"
    else:
        status = "high"

    return {
        "value": round(ram_usage, 1),
        "status": status,
    }


def _classify_disk_usage(disk_usage):
    """Classify disk utilization."""

    if not isinstance(disk_usage, (int, float)):
        return {
            "value": None,
            "status": "unknown",
            "reason": "Disk usage data unavailable.",
        }

    if disk_usage < 70:
        status = "healthy"
    elif disk_usage < 85:
        status = "elevated"
    elif disk_usage < 95:
        status = "high"
    else:
        status = "critical"

    return {
        "value": round(disk_usage, 1),
        "status": status,
    }


def analyze_health_metrics(hardware_details):
    """
    Perform deterministic health analysis.

    Gemini should explain these results rather than
    independently inventing severity levels.
    """

    cpu_usage = hardware_details.get(
        "cpu_usage_percent"
    )

    ram_usage = hardware_details.get(
        "ram_percent_used"
    )

    disk_total = hardware_details.get(
        "disk_c_total_gb"
    )

    disk_used = hardware_details.get(
        "disk_c_used_gb"
    )

    disk_usage = None

    if (
        isinstance(disk_total, (int, float))
        and disk_total > 0
        and isinstance(disk_used, (int, float))
    ):
        disk_usage = (
            disk_used / disk_total
        ) * 100

    cpu = _classify_cpu_usage(cpu_usage)
    ram = _classify_ram_usage(ram_usage)
    disk = _classify_disk_usage(disk_usage)

    return {
        "cpu": cpu,
        "ram": ram,
        "system_drive": disk,
    }


def calculate_health_score(health_metrics):
    """
    Calculate a deterministic health score from 0-100.

    Unknown metrics do not directly penalize the score.
    """

    score = 100

    deductions = {
        "healthy": 0,
        "elevated": 10,
        "high": 20,
        "critical": 35,
        "unknown": 0,
    }

    for metric in health_metrics.values():
        status = metric.get(
            "status",
            "unknown",
        )

        score -= deductions.get(
            status,
            0,
        )

    return max(
        0,
        min(100, score),
    )


def build_system_snapshot(
    hardware_details,
    system_apps,
    downloaded_apps,
    system_total,
    downloaded_total,
):
    """
    Build a complete structured snapshot including
    deterministic health analysis.
    """

    health_metrics = analyze_health_metrics(
        hardware_details
    )

    health_score = calculate_health_score(
        health_metrics
    )

    return {
        "hardware": hardware_details,
        "health_analysis": {
            "score": health_score,
            "metrics": health_metrics,
        },
        "software": {
            "system_app_count": len(system_apps),
            "downloaded_app_count": len(downloaded_apps),
            "system_app_storage_bytes": system_total,
            "downloaded_app_storage_bytes": downloaded_total,
        },
        "applications": {
            "system_apps": system_apps,
            "downloaded_apps": downloaded_apps,
        },
    }


def build_diagnosis_prompt(snapshot):
    """
    Convert the structured system snapshot into a
    Gemini diagnosis prompt.
    """

    snapshot_json = json.dumps(
        snapshot,
        indent=2,
        default=str,
    )

    return f"""
You are a Windows System Analysis AI.

Analyze the following system snapshot.

SYSTEM SNAPSHOT:
{snapshot_json}

The health score and metric classifications in
"health_analysis" were calculated locally using
deterministic rules.

Treat those values as authoritative.

Your job is to explain the system condition based ONLY
on the information provided above.

Return your response using exactly these sections:

## Overall Health
State the provided health score and explain the
main factors affecting it.

## Critical Issues
List issues that require immediate attention.
If there are none, write "None detected."

## Warnings
List elevated or high-severity issues.
If there are none, write "None detected."

## Recommendations
Give practical recommendations ordered from highest
priority to lowest priority.

## Software Observations
Discuss the available software inventory.
Identify unusually large, potentially unnecessary,
or duplicate applications only when the provided
data supports that conclusion.

Do NOT claim that software is malicious unless the
provided data actually supports that conclusion.

## Hardware Observations
Explain notable CPU, RAM, storage, operating system,
and disk information.

## Summary
Give a concise final assessment.

Important rules:
- Do not change the provided health score.
- Do not invent hardware specifications.
- Do not invent installed software.
- Do not claim malware based only on an application name.
- Do not treat missing telemetry as a hardware problem.
- Clearly distinguish facts from recommendations.
- If information is missing, say so.
"""