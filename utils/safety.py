from enum import Enum
from typing import Any, Dict


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ActionPolicy:
    def __init__(
        self,
        risk: RiskLevel,
        requires_confirmation: bool,
        description: str,
    ):
        self.risk = risk
        self.requires_confirmation = requires_confirmation
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk": self.risk.value,
            "requires_confirmation": self.requires_confirmation,
            "description": self.description,
        }


ACTION_POLICIES = {
    "system_info": ActionPolicy(
        risk=RiskLevel.LOW,
        requires_confirmation=False,
        description="Read system information.",
    ),

    "software_scan": ActionPolicy(
        risk=RiskLevel.LOW,
        requires_confirmation=False,
        description="Scan installed software.",
    ),

    "process_analysis": ActionPolicy(
        risk=RiskLevel.LOW,
        requires_confirmation=False,
        description="Analyze running processes.",
    ),

    "startup_analysis": ActionPolicy(
        risk=RiskLevel.LOW,
        requires_confirmation=False,
        description="Analyze Windows startup applications.",
    ),

    "storage_analysis": ActionPolicy(
        risk=RiskLevel.LOW,
        requires_confirmation=False,
        description="Analyze storage usage.",
    ),

    "open_url": ActionPolicy(
        risk=RiskLevel.LOW,
        requires_confirmation=False,
        description="Open a URL in the default browser.",
    ),

    "launch_application": ActionPolicy(
        risk=RiskLevel.MEDIUM,
        requires_confirmation=True,
        description="Launch a Windows application.",
    ),

    "software_install": ActionPolicy(
        risk=RiskLevel.HIGH,
        requires_confirmation=True,
        description="Download and install software.",
    ),
}


def get_action_policy(intent: str) -> ActionPolicy:
    """
    Return the safety policy associated with a command intent.

    Unknown actions are treated conservatively.
    """

    return ACTION_POLICIES.get(
        intent,
        ActionPolicy(
            risk=RiskLevel.HIGH,
            requires_confirmation=True,
            description="Unknown or unclassified action.",
        ),
    )


def requires_confirmation(intent: str) -> bool:
    """Return whether an action requires explicit user approval."""

    return get_action_policy(intent).requires_confirmation
