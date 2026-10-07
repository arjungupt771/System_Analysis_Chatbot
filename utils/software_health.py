from collections import Counter


def _safe_text(value):
    """Return a normalized text representation."""
    if value is None:
        return ""

    return str(value).strip()


def analyze_software_health(
    system_apps=None,
    downloaded_apps=None,
):
    """
    Analyze Windows application inventory without modifying the system.

    Returns deterministic findings that can later be passed to the AI
    diagnosis layer.
    """

    system_apps = system_apps or []
    downloaded_apps = downloaded_apps or []

    all_apps = []

    for app in system_apps:
        if isinstance(app, dict):
            item = dict(app)
            item["InventorySource"] = "Microsoft Store"
            all_apps.append(item)

    for app in downloaded_apps:
        if isinstance(app, dict):
            item = dict(app)
            item["InventorySource"] = "Windows Registry"
            all_apps.append(item)

    findings = []

    # ---------------------------------------------------------
    # Basic statistics
    # ---------------------------------------------------------

    total_apps = len(all_apps)

    store_apps = len(system_apps)
    win32_apps = len(downloaded_apps)

    # ---------------------------------------------------------
    # Missing installation locations
    # ---------------------------------------------------------

    missing_install_locations = []

    for app in all_apps:
        path = _safe_text(app.get("InstallLocation"))

        if not path or path.upper() == "N/A":
            missing_install_locations.append(
                app.get("App", "Unknown")
            )

    if missing_install_locations:
        findings.append(
            {
                "type": "missing_install_location",
                "severity": "low",
                "count": len(missing_install_locations),
                "apps": missing_install_locations[:20],
                "message": (
                    f"{len(missing_install_locations)} application(s) "
                    "do not expose a valid installation location."
                ),
            }
        )

    # ---------------------------------------------------------
    # Missing metadata
    # ---------------------------------------------------------

    missing_versions = []
    missing_publishers = []

    for app in all_apps:
        name = app.get("App", "Unknown")

        version = _safe_text(app.get("Version"))
        publisher = _safe_text(app.get("Publisher"))

        if not version or version.lower() == "unknown":
            missing_versions.append(name)

        if not publisher or publisher.lower() == "unknown":
            missing_publishers.append(name)

    if missing_versions:
        findings.append(
            {
                "type": "missing_version",
                "severity": "info",
                "count": len(missing_versions),
                "apps": missing_versions[:20],
                "message": (
                    f"{len(missing_versions)} application(s) "
                    "do not expose version information."
                ),
            }
        )

    if missing_publishers:
        findings.append(
            {
                "type": "missing_publisher",
                "severity": "info",
                "count": len(missing_publishers),
                "apps": missing_publishers[:20],
                "message": (
                    f"{len(missing_publishers)} application(s) "
                    "do not expose publisher information."
                ),
            }
        )

    # ---------------------------------------------------------
    # Duplicate applications
    # ---------------------------------------------------------

    name_counter = Counter()

    for app in all_apps:
        name = _safe_text(app.get("App"))

        if name:
            name_counter[name.lower()] += 1

    duplicate_apps = [
        name
        for name, count in name_counter.items()
        if count > 1
    ]

    if duplicate_apps:
        findings.append(
            {
                "type": "duplicate_application",
                "severity": "info",
                "count": len(duplicate_apps),
                "apps": duplicate_apps[:20],
                "message": (
                    f"{len(duplicate_apps)} application name(s) "
                    "appear multiple times in the inventory."
                ),
            }
        )

    # ---------------------------------------------------------
    # Large applications
    # ---------------------------------------------------------

    large_apps = []

    for app in all_apps:
        size_text = _safe_text(app.get("Size(MB)"))

        try:
            size_mb = float(size_text)
        except (ValueError, TypeError):
            continue

        # 2 GB threshold
        if size_mb >= 2048:
            large_apps.append(
                {
                    "name": app.get("App", "Unknown"),
                    "size_mb": round(size_mb, 2),
                }
            )

    large_apps.sort(
        key=lambda item: item["size_mb"],
        reverse=True,
    )

    if large_apps:
        findings.append(
            {
                "type": "large_application",
                "severity": "medium",
                "count": len(large_apps),
                "apps": large_apps[:20],
                "message": (
                    f"{len(large_apps)} application(s) use "
                    "more than 2 GB of storage."
                ),
            }
        )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    severity_counts = Counter(
        finding["severity"]
        for finding in findings
    )

    return {
        "summary": {
            "total_applications": total_apps,
            "microsoft_store_applications": store_apps,
            "win32_applications": win32_apps,
            "findings": len(findings),
            "high": severity_counts.get("high", 0),
            "medium": severity_counts.get("medium", 0),
            "low": severity_counts.get("low", 0),
            "info": severity_counts.get("info", 0),
        },
        "findings": findings,
    }