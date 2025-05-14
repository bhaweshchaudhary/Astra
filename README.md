Astra: A Powerful Network Scanner
Astra is an open-source network scanning tool designed for security researchers and network administrators. It allows you to scan IP ranges, resolve domains to IPs, and identify open ports with flexible configuration options. Built with Python, Astra leverages local DNS resolution and concurrent scanning for efficiency.
Features

Domain Resolution: Resolves domains (e.g., apple.com) to multiple IPs using dnspython for comprehensive scanning.
CIDR Scanning: Scan specific CIDR ranges (e.g., 192.168.1.0/24) with optional comma-separated multiple ranges.
Flexible Port Scanning:
Scan all 65,535 ports by default.
Limit to the first 1,000 ports (--first-1000) or 300 ports (--first-300).
Specify custom ports (--ports 80,443).

IP Limits:
Global limit with --max-ips to cap the total number of IPs scanned.
Per-CIDR limit with --max-ips-per-cidr, or use shortcuts --first-1-per-cidr, --first-2-per-cidr, --first-10-per-cidr.

Output Options: Save results in JSON or CSV format.
Verbose Logging: Detailed logs with --verbose for debugging and monitoring.
Configurable: Use a config file (~/.astra/config.json) or command-line arguments.

Installation

Clone the repository:git clone https://github.com/bhaweshchaudhary/astra.git
cd astra

Create a virtual environment and activate it:python3 -m venv venv
source venv/bin/activate

Install dependencies:pip install dnspython

(Optional) Create a config file at ~/.astra/config.json with:{
"api_token": "",
"default_ports": "22,80,443,8080,8443",
"default_timeout": 1.0
}

Usage
Run Astra with the following command:
python3 astra.py [org] [options]

Examples

Scan all ports for apple.com with a global limit of 100 IPs:python3 astra.py apple.com --max-ips 100 --verbose

Scan the first 1,000 ports for facebook.com with a 2-second timeout:python3 astra.py facebook.com --first-1000 --timeout 2.0 --max-ips 100 --verbose

Scan a CIDR range with the first 2 IPs per range:python3 astra.py --cidr 17.44.246.0/23 --first-300 --first-2-per-cidr --verbose

Scan multiple CIDR ranges:python3 astra.py --cidr 17.44.246.0/23,17.44.248.0/23 --first-300 --first-2-per-cidr --verbose

Command-Line Options
usage: astra.py [-h] [--api-token API_TOKEN] [--ports PORTS | --first-1000 | --first-300] [--max-ips-per-cidr MAX_IPS_PER_CIDR | --first-1-per-cidr | --first-2-per-cidr | --first-10-per-cidr] [--timeout TIMEOUT] [--max-ips MAX_IPS] [--verbose] [--output OUTPUT] [--output-format {json,csv}] [--config CONFIG] [--cidr CIDR]
[org]

Astra: A Powerful Network Scanner

positional arguments:
org Organization name or domain (e.g., apple or apple.com), optional if --cidr is provided

optional arguments:
-h, --help show this help message and exit
--api-token API_TOKEN ipinfo.io API token (overrides config)
--ports PORTS Comma-separated ports to scan (e.g., 80,443)
--first-1000 Scan the first 1000 ports (0-999)
--first-300 Scan the first 300 ports (0-299)
--max-ips-per-cidr MAX_IPS_PER_CIDR
Maximum number of IPs to scan per CIDR range
--first-1-per-cidr Scan only the first IP per CIDR range
--first-2-per-cidr Scan only the first 2 IPs per CIDR range
--first-10-per-cidr Scan only the first 10 IPs per CIDR range
--timeout TIMEOUT Timeout for host/port scans in seconds (default: 1.0 from config)
--max-ips MAX_IPS Maximum total number of IPs to scan (global limit)
--verbose Enable verbose output with detailed logs
--output OUTPUT File to save results (e.g., results.json)
--output-format {json,csv}
Output format (json, csv)
--config CONFIG Path to config file (default: ~/.astra/config.json)
--cidr CIDR Comma-separated CIDR ranges to scan (e.g., 192.168.1.0/24), skips domain resolution; org is optional when used

Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built with Python and enhanced with dnspython for robust DNS resolution.
Inspired by the need for a flexible, local network scanning tool.
