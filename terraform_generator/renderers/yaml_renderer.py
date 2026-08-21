import yaml

from terraform_generator.models import Route53Configuration


def render_route53_yaml(
    config: Route53Configuration
) -> str:
    """
    Convert the normalized Route53Configuration
    into the portal's portable YAML specification.

    Important:
    This YAML is not executed directly by Terraform.

    The portal can later use this specification
    to generate Terraform HCL or Terraform JSON.
    """

    records = []

    for record in config.records:
        records.append(
            {
                "name": record.name,
                "type": record.record_type,
                "ttl": record.ttl,
                "values": record.values
            }
        )

    yaml_config = {
        "terraform": {
            "provider": config.provider.name,
            "region": config.provider.region
        },

        "route53": {
            "hosted_zone": {
                "name": config.hosted_zone.name
            },

            "records": records
        }
    }

    return yaml.safe_dump(
        yaml_config,
        sort_keys=False,
        default_flow_style=False
    )