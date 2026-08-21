import json

from terraform_generator.models import Route53Configuration


def render_route53_json(
    config: Route53Configuration
) -> str:
    """
    Convert the normalized Route53Configuration
    model into Terraform JSON syntax.

    Output is suitable for a .tf.json file.
    """

    resources = {
        "aws_route53_zone": {
            "primary": {
                "name": config.hosted_zone.name
            }
        }
    }

    route53_records = {}

    for index, record in enumerate(
        config.records,
        start=1
    ):
        resource_name = f"record_{index}"

        route53_records[resource_name] = {
            "zone_id": "${aws_route53_zone.primary.zone_id}",
            "name": record.name,
            "type": record.record_type,
            "ttl": record.ttl,
            "records": record.values
        }

    if route53_records:
        resources[
            "aws_route53_record"
        ] = route53_records

    terraform_json = {
        "terraform": {
            "required_providers": {
                "aws": {
                    "source": "hashicorp/aws"
                }
            }
        },

        "provider": {
            "aws": {
                "region": config.provider.region
            }
        },

        "resource": resources
    }

    return json.dumps(
        terraform_json,
        indent=2
    )