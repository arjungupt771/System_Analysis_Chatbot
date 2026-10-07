from utils.safety import get_action_policy
from utils.tool_registry import get_tool


class ToolExecutionResult:
    def __init__(
        self,
        success,
        result=None,
        error=None,
        requires_confirmation=False,
        risk="low",
    ):
        self.success = success
        self.result = result
        self.error = error
        self.requires_confirmation = requires_confirmation
        self.risk = risk

    def to_dict(self):
        return {
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "requires_confirmation": self.requires_confirmation,
            "risk": self.risk,
        }


def execute_tool(routed_command, confirmed=False):
    if routed_command is None:
        return ToolExecutionResult(
            success=False,
            error="No command was provided.",
        )

    intent = routed_command.intent.value

    tool = get_tool(routed_command.intent)

    if tool is None:
        return ToolExecutionResult(
            success=False,
            error=f"No tool is registered for intent '{intent}'.",
        )

    policy = get_action_policy(intent)

    requires_approval = (
        policy.requires_confirmation
        or routed_command.requires_confirmation
        or tool.get("requires_confirmation", False)
    )

    if requires_approval and not confirmed:
        return ToolExecutionResult(
            success=False,
            error=(
                f"Confirmation is required before executing "
                f"'{tool['name']}'."
            ),
            requires_confirmation=True,
            risk=policy.risk.value,
        )

    function = tool.get("function")

    if not callable(function):
        return ToolExecutionResult(
            success=False,
            error=f"Tool '{tool['name']}' has no executable function.",
            risk=policy.risk.value,
        )

    try:
        command = routed_command.command.strip()

        if intent == "software_install":
            software_key = command

            if software_key.lower().startswith("install "):
                software_key = software_key[8:].strip()

            result = function(software_key)

        elif intent == "open_url":
            url = command

            if url.lower().startswith("open "):
                url = url[5:].strip()

            result = function(url)

        elif intent == "launch_application":
            application = command

            if application.lower().startswith("open "):
                application = application[5:].strip()
            elif application.lower().startswith("launch "):
                application = application[7:].strip()

            # Keep this action behind the safety layer.
            result = function(application)

        else:
            result = function()

        return ToolExecutionResult(
            success=True,
            result=result,
            risk=policy.risk.value,
        )

    except Exception as exc:
        return ToolExecutionResult(
            success=False,
            error=str(exc),
            risk=policy.risk.value,
        )