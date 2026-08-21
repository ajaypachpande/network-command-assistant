from terraform_generator.models import (
    build_route53_configuration
)

from terraform_generator.validator import (
    validate_route53_input
)

from terraform_generator.renderers.hcl_renderer import (
    render_route53_hcl
)

from terraform_generator.renderers.json_renderer import (
    render_route53_json
)

from terraform_generator.renderers.yaml_renderer import (
    render_route53_yaml
)


def generate_route53_terraform(
    domain_name: str,
    region: str,
    record_name: str,
    record_type: str,
    record_value: str,
    ttl
):
    """
    Main controller for Route 53 Terraform generation.

    Flow:

    User Input
        ↓
    Validation
        ↓
    Normalized Model
        ↓
    HCL / Terraform JSON / YAML
    """

    # --------------------------------------------------
    # STEP 1
    # Validate user input
    # --------------------------------------------------

    validation = validate_route53_input(
        domain_name=domain_name,
        record_name=record_name,
        record_type=record_type,
        record_value=record_value,
        ttl=ttl
    )

    if not validation["valid"]:

        return {
            "success": False,
            "errors": validation["errors"],
            "hcl": None,
            "json": None,
            "yaml": None
        }

    # --------------------------------------------------
    # STEP 2
    # Normalize values
    # --------------------------------------------------

    domain_name = domain_name.strip().lower()

    region = region.strip()

    record_name = record_name.strip()

    record_type = record_type.strip().upper()

    record_value = record_value.strip()

    ttl = int(ttl)

    # --------------------------------------------------
    # STEP 3
    # Build normalized internal model
    # --------------------------------------------------

    config = build_route53_configuration(
        domain_name=domain_name,
        region=region,
        record_name=record_name,
        record_type=record_type,
        record_value=record_value,
        ttl=ttl
    )

    # --------------------------------------------------
    # STEP 4
    # Render all supported formats
    # --------------------------------------------------

    hcl_output = render_route53_hcl(
        config
    )

    json_output = render_route53_json(
        config
    )

    yaml_output = render_route53_yaml(
        config
    )

    # --------------------------------------------------
    # STEP 5
    # Return one predictable result
    # --------------------------------------------------

    return {
        "success": True,
        "errors": [],
        "hcl": hcl_output,
        "json": json_output,
        "yaml": yaml_output
    }