import json
from pathlib import Path


# ==========================================================
# LOAD AWS NETWORK WORKFLOW
# ==========================================================

WORKFLOW_FILE = (
    Path(__file__).parent.parent
    / "knowledge"
    / "aws"
    / "network_workflows.json"
)


with WORKFLOW_FILE.open(
    "r",
    encoding="utf-8"
) as file:

    AWS_DATA = json.load(file)


# ==========================================================
# GET WORKFLOW INFORMATION
# ==========================================================

def get_workflow_info():
    """
    Return general information about the
    AWS Network troubleshooting workflow.
    """

    return AWS_DATA.get(
        "workflow",
        {}
    )


# ==========================================================
# GET ALL ENTRY POINTS
# ==========================================================

def get_entry_points():
    """
    Return all supported AWS Network
    troubleshooting entry points.
    """

    return AWS_DATA.get(
        "entry_points",
        {}
    )


# ==========================================================
# GET ENTRY POINT
# ==========================================================

def get_entry_point(symptom):
    """
    Return the first troubleshooting step
    for a known AWS network symptom.
    """

    entry_points = get_entry_points()


    if symptom not in entry_points:

        return None


    return entry_points[
        symptom
    ].get(
        "first_step"
    )


# ==========================================================
# GET TROUBLESHOOTING STEP
# ==========================================================

def get_step(step_id):
    """
    Return one AWS troubleshooting node
    from the JSON knowledge graph.
    """

    steps = AWS_DATA.get(
        "steps",
        {}
    )


    return steps.get(
        step_id
    )


# ==========================================================
# FORMAT STEP FOR FLASK / JINJA
# ==========================================================

def format_step(
    step_id,
    step
):
    """
    Convert a raw AWS JSON node into a
    predictable dictionary that Flask
    and Jinja can safely render.
    """

    return {

        "step_id":
            step_id,

        "title":
            step.get(
                "title"
            ),

        "purpose":
            step.get(
                "purpose"
            ),

        "risk":
            step.get(
                "risk",
                "safe"
            ),

        "likely_causes":
            step.get(
                "likely_causes",
                []
            ),

        "recommended_checks":
            step.get(
                "recommended_checks",
                []
            ),

        "commands":
            step.get(
                "commands",
                []
            ),

        "warning":
            step.get(
                "warning"
            ),

        "cleanup_commands":
            step.get(
                "cleanup_commands",
                []
            ),

        "decision":
            step.get(
                "decision",
                {}
            )

    }


# ==========================================================
# START AWS TROUBLESHOOTING
# ==========================================================

def start_aws_troubleshooting(
    symptom
):
    """
    Start AWS Network troubleshooting
    from one of the supported symptoms.

    Examples:

    ec2_no_internet

    cannot_connect_ec2

    vpc_to_vpc_failure

    onprem_to_aws_failure
    """

    first_step_id = get_entry_point(
        symptom
    )


    # ------------------------------------------------------
    # UNKNOWN SYMPTOM
    # ------------------------------------------------------

    if not first_step_id:

        return {

            "error":
                "Unknown AWS network symptom."

        }


    first_step = get_step(
        first_step_id
    )


    # ------------------------------------------------------
    # ENTRY POINT REFERENCES UNKNOWN NODE
    # ------------------------------------------------------

    if not first_step:

        return {

            "error":
                (
                    f"AWS entry point references "
                    f"unknown step "
                    f"'{first_step_id}'."
                )

        }


    result = format_step(
        first_step_id,
        first_step
    )


    result[
        "symptom"
    ] = symptom


    result[
        "workflow"
    ] = get_workflow_info()


    return result


# ==========================================================
# FOLLOW A DECISION
# ==========================================================

def get_next_step(
    current_step_id,
    decision_result
):
    """
    Given the current AWS graph node and
    the engineer's observation, return
    the next troubleshooting node.
    """

    current_step = get_step(
        current_step_id
    )


    # ------------------------------------------------------
    # UNKNOWN CURRENT NODE
    # ------------------------------------------------------

    if not current_step:

        return {

            "error":
                (
                    f"Current AWS step "
                    f"'{current_step_id}' "
                    f"was not found."
                )

        }


    decisions = current_step.get(
        "decision",
        {}
    )


    # ------------------------------------------------------
    # TERMINAL NODE
    # ------------------------------------------------------

    if not decisions:

        result = format_step(
            current_step_id,
            current_step
        )


        result[
            "status"
        ] = "terminal"


        result[
            "message"
        ] = (
            "This AWS troubleshooting "
            "branch has reached an endpoint."
        )


        return result


    # ------------------------------------------------------
    # FIND NEXT NODE
    # ------------------------------------------------------

    next_step_id = decisions.get(
        decision_result
    )


    if not next_step_id:

        return {

            "error":
                (
                    f"Decision "
                    f"'{decision_result}' "
                    f"is not valid for AWS step "
                    f"'{current_step_id}'."
                )

        }


    next_step = get_step(
        next_step_id
    )


    # ------------------------------------------------------
    # CONTROLLED UNDEFINED NODE
    # ------------------------------------------------------

    if not next_step:

        return {

            "step_id":
                next_step_id,

            "status":
                "terminal_or_not_yet_defined",

            "message":
                (
                    f"AWS workflow points to "
                    f"'{next_step_id}', but that "
                    f"step has not been defined yet."
                )

        }


    # ------------------------------------------------------
    # NORMAL NEXT STEP
    # ------------------------------------------------------

    return format_step(
        next_step_id,
        next_step
    )


# ==========================================================
# VALIDATE GRAPH RELATIONSHIPS
# ==========================================================

def validate_graph():
    """
    Check the AWS knowledge graph for:

    - missing entry-point nodes
    - decision targets that do not exist

    Return a list of problems.
    """

    problems = []


    entry_points = get_entry_points()

    steps = AWS_DATA.get(
        "steps",
        {}
    )


    # ------------------------------------------------------
    # CHECK ENTRY POINTS
    # ------------------------------------------------------

    for symptom, entry in entry_points.items():

        first_step = entry.get(
            "first_step"
        )


        if first_step not in steps:

            problems.append(
                (
                    f"Entry point '{symptom}' "
                    f"references missing step "
                    f"'{first_step}'."
                )
            )


    # ------------------------------------------------------
    # CHECK DECISION TARGETS
    # ------------------------------------------------------

    for step_id, step in steps.items():

        decisions = step.get(
            "decision",
            {}
        )


        for decision, target in decisions.items():

            if target not in steps:

                problems.append(
                    (
                        f"Step '{step_id}' "
                        f"decision '{decision}' "
                        f"references missing step "
                        f"'{target}'."
                    )
                )


    return problems


# ==========================================================
# LOCAL ENGINE TEST
# ==========================================================

if __name__ == "__main__":

    print(
        "\n"
        "======================================"
    )

    print(
        "AWS NETWORK AI v0.1"
    )

    print(
        "======================================"
    )


    print(
        "\nSUPPORTED ENTRY POINTS:\n"
    )


    for symptom, entry in get_entry_points().items():

        print(
            f"{symptom}: "
            f"{entry.get('title')}"
        )


    # ------------------------------------------------------
    # START TEST
    # ------------------------------------------------------

    print(
        "\n"
        "=== START EC2 INTERNET WORKFLOW ==="
        "\n"
    )


    start = start_aws_troubleshooting(
        "ec2_no_internet"
    )


    print(
        json.dumps(
            start,
            indent=2
        )
    )


    # ------------------------------------------------------
    # DECISION TEST
    # ------------------------------------------------------

    print(
        "\n"
        "=== DECISION: INSTANCE NETWORK OK ==="
        "\n"
    )


    next_step = get_next_step(
        "check_ec2_network_state",
        "instance_network_ok"
    )


    print(
        json.dumps(
            next_step,
            indent=2
        )
    )


    # ------------------------------------------------------
    # GRAPH VALIDATION
    # ------------------------------------------------------

    print(
        "\n"
        "=== GRAPH VALIDATION ==="
        "\n"
    )


    problems = validate_graph()


    if not problems:

        print(
            "AWS knowledge graph is valid."
        )

    else:

        print(
            f"Found {len(problems)} problem(s):"
        )


        for problem in problems:

            print(
                f"- {problem}"
            )