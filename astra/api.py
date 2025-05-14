import requests
import logging
from typing import List

def get_cidr_ranges(org: str, api_token: str) -> List[str]:
    """Fetch CIDR ranges using ipinfo.io API."""
    logging.debug(f"Fetching CIDR ranges for {org}")
    url = f"https://ipinfo.io/ranges/{org}?token={api_token}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        ranges = data.get("ranges", [])
        logging.info(f"Found {len(ranges)} CIDR ranges")
        return ranges
    except requests.RequestException as e:
        logging.error(f"Error fetching CIDR ranges: {e}")
        return []
