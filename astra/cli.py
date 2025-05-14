import argparse
import logging
from typing import List
from .config import load_config
from .api import get_cidr_ranges
from .network import extract_ips, scan_hosts, scan_ports
from .report import report_results

def setup_logging(verbose: bool):
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=level
    )

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Astra: A Powerful Network Scanner")
    parser.add_argument("org", help="Organization name or domain (e.g., apple or apple.com)")
    parser.add_argument("--api-token", help="ipinfo.io API token (overrides config)")
    parser.add_argument("--ports", default="22,80,443,8080,8443", help="Comma-separated ports to scan (e.g., 80,443)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout for host/port scans in seconds")
    parser.add_argument("--max-ips", type=int, help="Maximum number of IPs to scan per CIDR")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--output", help="File to save results (e.g., results.json)")
    parser.add_argument("--output-format", choices=["json", "csv"], default="json", help="Output format (json, csv)")
    parser.add_argument("--config", default="~/.astra/config.json", help="Path to config file")
    return parser.parse_args()

def main():
    """Main CLI logic."""
    args = parse_args()
    setup_logging(args.verbose)

    # Load configuration
    config = load_config(args.config)
    api_token = args.api_token or config.get("api_token")
    if not api_token:
        logging.error("API token required. Provide via --api-token or config file.")
        return

    # Fetch CIDR ranges
    logging.info(f"Starting scan for {args.org}")
    cidrs = get_cidr_ranges(args.org, api_token)
    if not cidrs:
        logging.error("No CIDR ranges found. Exiting.")
        return

    # Extract IPs
    all_ips = extract_ips(cidrs, args.max_ips)
    if not all_ips:
        logging.error("No IPs extracted. Exiting.")
        return

    # Scan for live hosts
    live_hosts = scan_hosts(all_ips, args.timeout)
    if not live_hosts:
        logging.error("No live hosts found. Exiting.")
        return

    # Scan ports
    try:
        ports = [int(p) for p in args.ports.split(",")]
    except ValueError:
        logging.error("Invalid ports format. Use comma-separated integers (e.g., 80,443).")
        return
    open_ports = scan_ports(live_hosts, ports, args.timeout)

    # Report results
    report_results(
        org=args.org,
        cidrs=cidrs,
        live_hosts=live_hosts,
        open_ports=open_ports,
        output_file=args.output,
        output_format=args.output_format
    )
