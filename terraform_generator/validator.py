import ipaddress
import re


SUPPORTED_RECORD_TYPES = {
    "A",
    "AAAA",
    "CNAME",
    "TXT"
}


def validate_domain_name(domain_name: str):
    """
    Basic DNS-style validation for the learning portal.
    """

    if not domain_name:
        return False, "Domain name is required."

    domain_name = domain_name.strip().lower()

    if len(domain_name) > 253:
        return False, "Domain name is too long."

    pattern = re.compile(
        r"^(?:[a-z0-9]"
        r"(?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
        r"[a-z]{2,63}$"
    )

    if not pattern.match(domain_name):
        return False, "Domain name format is invalid."

    return True, None


def validate_record_name(record_name: str):
    if not record_name:
        return False, "Record name is required."

    record_name = record_name.strip()

    if len(record_name) > 253:
        return False, "Record name is too long."

    return True, None


def validate_record_type(record_type: str):
    if not record_type:
        return False, "Record type is required."

    record_type = record_type.upper()

    if record_type not in SUPPORTED_RECORD_TYPES:
        return (
            False,
            (
                "Unsupported record type. "
                f"Supported types: "
                f"{', '.join(sorted(SUPPORTED_RECORD_TYPES))}"
            )
        )

    return True, None


def validate_record_value(
    record_type: str,
    record_value: str
):
    if not record_value:
        return False, "Record value is required."

    record_type = record_type.upper()

    try:

        if record_type == "A":
            ipaddress.IPv4Address(
                record_value
            )

        elif record_type == "AAAA":
            ipaddress.IPv6Address(
                record_value
            )

    except ipaddress.AddressValueError:

        return (
            False,
            f"Invalid {record_type} address."
        )

    return True, None


def validate_ttl(ttl):
    try:
        ttl = int(ttl)

    except (TypeError, ValueError):
        return False, "TTL must be an integer."

    if ttl < 1:
        return False, "TTL must be greater than 0."

    if ttl > 86400:
        return (
            False,
            "TTL must be 86400 seconds or less for this learning portal."
        )

    return True, None


def validate_route53_input(
    domain_name: str,
    record_name: str,
    record_type: str,
    record_value: str,
    ttl
):
    """
    Validate all Route 53 generator input.

    Returns:
        {
            "valid": bool,
            "errors": []
        }
    """

    errors = []

    checks = [
        validate_domain_name(
            domain_name
        ),
        validate_record_name(
            record_name
        ),
        validate_record_type(
            record_type
        ),
        validate_record_value(
            record_type,
            record_value
        ),
        validate_ttl(
            ttl
        )
    ]

    for valid, error in checks:

        if not valid:
            errors.append(
                error
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }