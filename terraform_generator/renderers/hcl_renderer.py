from terraform_generator.models import Route53Configuration


def render_route53_hcl(
    config: Route53Configuration
) -> str:
    """
    Convert the normalized Route53Configuration
    model into standard Terraform HCL.
    """

    lines = []

    # ======================================================
    # TERRAFORM / PROVIDER REQUIREMENTS
    # ======================================================

    lines.extend(
        [
            'terraform {',
            '  required_providers {',
            '    aws = {',
            '      source = "hashicorp/aws"',
            '    }',
            '  }',
            '}',
            '',
            'provider "aws" {',
            f'  region = "{config.provider.region}"',
            '}',
            ''
        ]
    )

    # ======================================================
    # ROUTE 53 HOSTED ZONE
    # ======================================================

    lines.extend(
        [
            'resource "aws_route53_zone" "primary" {',
            f'  name = "{config.hosted_zone.name}"',
            '}',
            ''
        ]
    )

    # ======================================================
    # ROUTE 53 RECORDS
    # ======================================================

    for index, record in enumerate(
        config.records,
        start=1
    ):

        resource_name = f"record_{index}"

        values = ", ".join(
            f'"{value}"'
            for value in record.values
        )

        lines.extend(
            [
                f'resource "aws_route53_record" "{resource_name}" {{',
                '  zone_id = aws_route53_zone.primary.zone_id',
                f'  name    = "{record.name}"',
                f'  type    = "{record.record_type}"',
                f'  ttl     = {record.ttl}',
                f'  records = [{values}]',
                '}',
                ''
            ]
        )

    return "\n".join(lines).rstrip() + "\n"