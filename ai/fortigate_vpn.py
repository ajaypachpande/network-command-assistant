import json
from pathlib import Path


# ==========================================================
# LOAD FORTIGATE VPN WORKFLOW
# ==========================================================

WORKFLOW_FILE = (
    Path(__file__).parent.parent
    / "knowledge"
    / "fortigate"
    / "vpn_workflows.json"
)


with WORKFLOW_FILE.open(
    "r",
    encoding="utf-8"
) as file:

    VPN_DATA = json.load(file)


# ==========================================================
# GET ENTRY POINT
# ==========================================================

def get_entry_point(symptom):
    """
    Return the first troubleshooting step
    for a known FortiGate VPN symptom.
    """

    entry_points = VPN_DATA["entry_points"]

    if symptom not in entry_points:
        return None

    return entry_points[symptom]["first_step"]


# ==========================================================
# GET TROUBLESHOOTING STEP
# ==========================================================

def get_step(step_id):
    """
    Return a troubleshooting step from
    the JSON knowledge graph.
    """

    return VPN_DATA["steps"].get(step_id)


# ==========================================================
# FORMAT A STEP FOR THE WEB UI
# ==========================================================

def format_step(step_id, step):
    """
    Convert a raw JSON node into the
    structure expected by the Jinja template.
    """

    return {
        "step_id": step_id,

        "title": step.get(
            "title"
        ),

        "purpose": step.get(
            "purpose"
        ),

        "risk": step.get(
            "risk"
        ),

        "likely_causes": step.get(
            "likely_causes",
            []
        ),

        "recommended_checks": step.get(
            "recommended_checks",
            []
        ),

        "warning": step.get(
            "warning"
        ),

        "commands": step.get(
            "commands",
            []
        ),

        "cleanup_commands": step.get(
            "cleanup_commands",
            []
        ),

        "decision": step.get(
            "decision",
            {}
        )
    }


# ==========================================================
# START WORKFLOW
# ==========================================================

def start_vpn_troubleshooting(symptom):
    """
    Start FortiGate VPN troubleshooting from
    a symptom such as:

        tunnel_down
        tunnel_up_no_traffic
    """

    first_step_id = get_entry_point(symptom)

    if not first_step_id:
        return {
            "error": "Unknown FortiGate VPN symptom."
        }

    step = get_step(first_step_id)

    if not step:
        return {
            "error": (
                f"Workflow step '{first_step_id}' "
                "was not found."
            )
        }

    result = format_step(
        first_step_id,
        step
    )

    result["symptom"] = symptom

    return result


# ==========================================================
# FOLLOW A DECISION
# ==========================================================

def get_next_step(
    current_step_id,
    decision_result
):
    """
    Given the current node and what the engineer
    observed, return the next graph node.
    """

    current_step = get_step(
        current_step_id
    )

    if not current_step:
        return {
            "error": (
                f"Current step '{current_step_id}' "
                "was not found."
            )
        }

    decisions = current_step.get(
        "decision",
        {}
    )

    next_step_id = decisions.get(
        decision_result
    )

    if not next_step_id:
        return {
            "error": (
                f"Decision '{decision_result}' "
                f"is not valid for step "
                f"'{current_step_id}'."
            )
        }

    next_step = get_step(
        next_step_id
    )

    # Some decision targets intentionally have not
    # been built yet. Show a controlled endpoint
    # rather than crashing.
    if not next_step:
        return {
            "step_id": next_step_id,

            "status":
                "terminal_or_not_yet_defined",

            "message": (
                f"Workflow points to "
                f"'{next_step_id}', but that "
                "step has not been defined yet."
            )
        }

    return format_step(
        next_step_id,
        next_step
    )


# ==========================================================
# LOCAL ENGINE TEST
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=== START WORKFLOW ===\n"
    )

    start = start_vpn_troubleshooting(
        "tunnel_up_no_traffic"
    )

    print(
        json.dumps(
            start,
            indent=2
        )
    )


    print(
        "\n=== DECISION: "
        "NO COUNTER CHANGE ===\n"
    )

    next_step = get_next_step(
        "check_ipsec_counters",
        "no_counter_change"
    )

    print(
        json.dumps(
            next_step,
            indent=2
        )
    )
