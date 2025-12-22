#!/usr/bin/env python3
"""Fetch FIDE federations and output as a country name to code mapping."""

import json
import re
import requests


def extract_country_name(html: str) -> str:
    """Extract country name from the HTML div."""
    match = re.search(r'>([^<]+)</a>', html)
    if match:
        return match.group(1)
    return ""


def fetch_federations() -> dict[str, str]:
    """Fetch federations from FIDE and return name->code mapping."""
    response = requests.get("https://ratings.fide.com/a_top_fed.php")
    data = response.json()

    federations = {}
    for entry in data.get("data", []):
        html = entry[1]
        code = entry[3]
        name = extract_country_name(html)
        if name and code:
            federations[name] = code

    return federations


if __name__ == "__main__":
    federations = fetch_federations()
    print(json.dumps(federations, indent=2))
