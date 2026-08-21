from dataclasses import dataclass, field
from typing import List


@dataclass
class TerraformProvider:
    name: str = "aws"
    region: str = "us-east-1"


@dataclass
class Route53Record:
    name: str
    record_type: str
    ttl: int
    values: List[str] = field(
        default_factory=list
    )


@dataclass
class Route53HostedZone:
    name: str


@dataclass
class Route53Configuration:
    provider: TerraformProvider
    hosted_zone: Route53HostedZone
    records: List[Route53Record] = field(
        default_factory=list
    )


def build_route53_configuration(
    domain_name: str,
    region: str,
    record_name: str,
    record_type: str,
    record_value: str,
    ttl: int
) -> Route53Configuration:
    """
    Convert user-style Route 53 input into
    one normalized internal model.

    All renderers will consume this same model.
    """

    provider = TerraformProvider(
        region=region
    )

    hosted_zone = Route53HostedZone(
        name=domain_name
    )

    # If user enters "www", convert it to
    # "www.example.com".
    #
    # If they already provide an FQDN,
    # preserve it.
    if record_name.endswith(
        domain_name
    ):
        fqdn = record_name
    else:
        fqdn = (
            f"{record_name}."
            f"{domain_name}"
        )

    record = Route53Record(
        name=fqdn,
        record_type=record_type.upper(),
        ttl=ttl,
        values=[
            record_value
        ]
    )

    return Route53Configuration(
        provider=provider,
        hosted_zone=hosted_zone,
        records=[
            record
        ]
    )