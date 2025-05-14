Astra: A Powerful Network Scanner
Astra is a powerful, modular, and extensible command-line tool designed for bug bounty hunters and security researchers. It automates the process of network reconnaissance by fetching CIDR ranges for a given organization or domain, extracting IP addresses, identifying live hosts, and scanning for open ports. Astra is built with scalability in mind, making it easy to add new features like additional APIs or reporting formats.
Features

CIDR Range Retrieval: Fetches CIDR ranges using the ipinfo.io API.
IP Extraction: Converts CIDR ranges to individual IP addresses.
Live Host Detection: Identifies responsive hosts using TCP connect.
Port Scanning: Scans specified ports on live hosts.
Flexible Configuration: Supports command-line flags and a JSON config file.
Extensible Reporting: Outputs results to console, JSON, or CSV.
Scalable Design: Modular architecture for easy feature additions.

Installation
Prerequisites

Python 3.6 or higher
An ipinfo.io API token (free tier available)

Homebrew (macOS)
brew install astra

GitHub (Clone and Install)
git clone https://github.com/bhaweshchaudhary/astra.git
cd astra
pip install .

apt (Ubuntu/Debian)
sudo add-apt-repository ppa:xai-org/astra
sudo apt update
sudo apt install astra

From Source
git clone https://github.com/bhaweshchaudhary/astra.git
cd astra
python3 setup.py install

Configuration
Create a configuration file at ~/.astra/config.json to store defaults:
{
"api_token": "your_ipinfo_io_token",
"default_ports": "22,80,443,8080,8443",
"default_timeout": 1.0
}

Usage
Run Astra with the following command:
astra <organization> [options]

Options

--api-token: ipinfo.io API token (overrides config).
--ports: Comma-separated ports to scan (default: 22,80,443,8080,8443).
--timeout: Timeout for scans in seconds (default: 1.0).
--max-ips: Maximum IPs to scan per CIDR.
--verbose: Enable detailed logging.
--output: File to save results (e.g., results.json).
--output-format: Output format (json or csv, default: json).
--config: Path to config file (default: ~/.astra/config.json).

Example
astra apple --api-token your_token --ports 80,443 --timeout 2.0 --max-ips 100 --verbose --output results.json --output-format json

Example Output
2025-05-14 17:33:45,123 [INFO] Starting scan for apple
2025-05-14 17:33:45,456 [INFO] Found 3 CIDR ranges: ['17.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
2025-05-14 17:33:45,789 [INFO] Extracted 300 IPs
2025-05-14 17:33:46,012 [INFO] Found 10 live hosts
2025-05-14 17:33:46,013 [INFO] - 17.1.2.3
...
2025-05-14 17:33:46,456 [INFO] Found 2 open ports
2025-05-14 17:33:46,457 [INFO] - 17.1.2.3:80
2025-05-14 17:33:46,458 [INFO] - 17.1.2.3:443
2025-05-14 17:33:46,459 [INFO] Results saved as JSON to results.json

JSON Output
{
"organization": "apple",
"timestamp": "2025-05-14T12:33:46.459123",
"cidr_ranges": ["17.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"],
"live_hosts": ["17.1.2.3", ...],
"open_ports": [
{"ip": "17.1.2.3", "port": 80},
{"ip": "17.1.2.3", "port": 443}
]
}

CSV Output
IP,Port
17.1.2.3,80
17.1.2.3,443

Legal Disclaimer
Astra is intended for ethical security research and bug bounty programs. Only scan networks you have explicit permission to test. Unauthorized scanning is illegal and may result in legal consequences. Always adhere to the target organization's bug bounty policy and applicable laws.
Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/new-feature).
Commit changes (git commit -m "Add new feature").
Push to the branch (git push origin feature/new-feature).
Open a pull request.

Please include tests and update documentation as needed.
License
Astra is licensed under the MIT License.
Contact
For support or inquiries, contact support@x.ai.

Built by xAI
