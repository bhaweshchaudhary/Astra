# Astra Developer Documentation

**Last Updated**: May 15, 2025

## Overview

Astra is an open-source network scanning tool written in Python, designed for security researchers and network administrators. It enables users to scan IP ranges, resolve domains to IPs, and identify open ports with high flexibility. Unlike many existing tools, Astra operates locally without third-party API dependencies (e.g., no reliance on services like ipinfo.io for core functionality), prioritizing user control, privacy, and customization.

### Purpose

Astra was developed to address the need for a lightweight, customizable network scanner that:

- Operates independently of external APIs for core functionality.
- Provides fine-grained control over IP and port scanning (e.g., per-CIDR IP limits, custom port ranges).
- Supports both domain-based and CIDR-based scanning in a single tool.
- Offers detailed logging for debugging and transparency.

This documentation is intended for developers and maintainers who wish to understand, maintain, or extend Astra’s functionality.

## Core Features

Astra’s core features are designed to be modular and extensible. Below is an overview of each feature and its implementation:

1. **Domain Resolution**:

   - Resolves domains (e.g., `apple.com`) to multiple IPs using the `dnspython` library.
   - Implemented in `astra/api.py` via the `get_cidr_ranges_local` function.
   - Converts each resolved IP into a `/32` CIDR range for consistent handling with user-provided CIDR ranges.

2. **CIDR Scanning**:

   - Supports scanning user-provided CIDR ranges (e.g., `192.168.1.0/24`) or comma-separated CIDR lists.
   - Validates CIDR ranges using Python’s `ipaddress` module.
   - Implemented in `astra/api.py` via the `get_cidr_ranges` function.

3. **Flexible Port Scanning**:

   - Scans all 65,535 ports by default, with options to limit to the first 1,000 (`--first-1000`), 300 (`--first-300`), or custom ports (`--ports 80,443`).
   - Uses concurrent TCP scanning with `socket` and `concurrent.futures.ThreadPoolExecutor` for efficiency.
   - Implemented in `astra/network.py` via the `scan_network` function.

4. **IP Limits**:

   - Global limit (`--max-ips`) caps the total number of IPs scanned across all CIDR ranges.
   - Per-CIDR limit (`--max-ips-per-cidr`, `--first-1-per-cidr`, `--first-2-per-cidr`, `--first-10-per-cidr`) controls the number of IPs scanned per CIDR range.
   - Implemented in `astra/network.py` via the `extract_ips` function.

5. **Output Options**:

   - Saves results in JSON or CSV format (`--output`, `--output-format`).
   - Implemented in `astra/report.py` via the `save_results` function.

6. **Verbose Logging**:

   - Provides detailed logs with `--verbose`, including CIDR ranges, IP counts, and scan progress.
   - Uses Python’s `logging` module, configured in `astra/cli.py`.

7. **Configurability**:
   - Supports a config file (`~/.astra/config.json`) for default settings (e.g., timeout, default ports).
   - Implemented in `astra/config.py` via the `load_config` function.

## Architecture

Astra follows a modular design with distinct components for each major functionality. The architecture is structured to ensure separation of concerns, making it easy to modify or extend specific features.

### Workflow

1. **Command-Line Parsing** (`astra/cli.py`):

   - Parses user arguments using `argparse`.
   - Determines ports to scan, IP limits, and other settings.
   - Initiates the scanning process.

2. **CIDR Resolution** (`astra/api.py`):

   - Resolves domains to IPs or processes user-provided CIDR ranges.
   - Returns a list of CIDR ranges to scan.

3. **IP Extraction** (`astra/network.py`):

   - Expands CIDR ranges into individual IPs.
   - Applies global and per-CIDR IP limits.

4. **Network Scanning** (`astra/network.py`):

   - Identifies live hosts by attempting a TCP connection (default port 80).
   - Scans specified ports on live hosts using concurrent threads.
   - Returns live hosts and open ports.

5. **Result Handling** (`astra/report.py`):

   - Saves results to a file (JSON/CSV) or prints to console.
   - Formats output for readability.

6. **Configuration** (`astra/config.py`):
   - Loads default settings from a config file, if provided.

### File Structure

- `astra/`
  - `__init__.py`: Package initializer.
  - `cli.py`: Command-line interface and main entry point.
  - `api.py`: Handles domain resolution and CIDR range processing.
  - `network.py`: Manages IP extraction and network scanning.
  - `report.py`: Formats and saves scan results.
  - `config.py`: Loads configuration settings.
- `astra.py`: Entry script that calls `cli.main()`.
- `requirements.txt`: Lists dependencies (e.g., `dnspython`).
- `README.md`: User-facing documentation.
- `DEVELOPER.md`: This file.

## Code Walkthrough

### Key Functions

1. **cli.py: main()**

   - Entry point for the CLI.
   - Displays a banner, parses arguments, sets up logging, and orchestrates the scanning process.
   - Calls `get_cidr_ranges`, `extract_ips`, `scan_network`, and `save_results`.

2. **api.py: get_cidr_ranges()**

   - Takes an organization name (or domain) and optional CIDR range.
   - If `--cidr` is provided, validates and returns the CIDR(s).
   - Otherwise, resolves the domain to IPs using `get_cidr_ranges_local`.

3. **api.py: get_cidr_ranges_local()**

   - Uses `dns.resolver` to fetch A records for a domain.
   - Converts IPs to `/32` CIDR ranges.
   - Includes error handling for DNS failures.

4. **network.py: extract_ips()**

   - Expands CIDR ranges into IPs using `ipaddress.ip_network`.
   - Applies per-CIDR (`max_ips_per_cidr`) and global (`max_ips`) limits.
   - Logs the number of IPs extracted per CIDR.

5. **network.py: scan_network()**

   - Performs a two-step scan:
     1. Identifies live hosts by attempting a TCP connection to port 80.
     2. Scans specified ports on live hosts using concurrent threads.
   - Optimizes thread count (`max_workers`) based on workload.

6. **report.py: save_results()**
   - Saves scan results to a file in JSON or CSV format.
   - If no output file is specified, results are logged to the console.

### Dependencies

- `dnspython`: For domain resolution (`dns.resolver`).
- Python Standard Library:
  - `argparse`: Command-line argument parsing.
  - `logging`: Verbose logging.
  - `socket`: TCP scanning.
  - `ipaddress`: CIDR range handling.
  - `concurrent.futures`: Concurrent scanning.
  - `json` and `csv`: Output formatting.

Dependencies are listed in `requirements.txt` and can be installed with:

```bash
pip install -r requirements.txt
```

## Extending Astra

Astra’s modular design makes it straightforward to add new features or modify existing ones. Below are common extension scenarios:

### Adding a New Command-Line Argument

1. Open `astra/cli.py` and locate the `parse_args` function.
2. Add a new argument using `parser.add_argument`. For example, to add a `--scan-type` argument:
   ```python
   parser.add_argument("--scan-type", choices=["tcp", "udp"], default="tcp", help="Type of scan to perform (tcp, udp)")
   ```
3. Use the new argument in `main`. For example:
   ```python
   scan_type = args.scan_type
   logging.info(f"Using scan type: {scan_type}")
   ```

### Supporting UDP Scanning

1. Open `astra/network.py`.
2. Modify `scan_port` to support UDP by adding a `scan_type` parameter:
   ```python
   def scan_port(ip: str, port: int, timeout: float, scan_type: str = "tcp") -> bool:
       try:
           if scan_type == "tcp":
               sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           elif scan_type == "udp":
               sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
           sock.settimeout(timeout)
           result = sock.connect_ex((ip, port))
           sock.close()
           return result == 0
       except socket.error:
           return False
   ```
3. Update `scan_network` to pass the `scan_type` parameter to `scan_port`.

### Adding a New Output Format

1. Open `astra/report.py`.
2. Modify `save_results` to support the new format (e.g., XML):
   ```python
   if output_format == "xml":
       import xml.etree.ElementTree as ET
       root = ET.Element("scan_results")
       # Add scan data to XML structure
       tree = ET.ElementTree(root)
       tree.write(output_file)
   ```
3. Update `cli.py` to include the new format in the `--output-format` choices:
   ```python
   parser.add_argument("--output-format", choices=["json", "csv", "xml"], help="Output format (json, csv, xml)")
   ```

### Improving Performance

- **Increase Concurrency**: Adjust `max_workers` in `network.py`’s `scan_network` function. Be cautious of system resource limits.
- **Optimize Logging**: Add log levels or filters in `cli.py` to reduce I/O overhead in non-verbose mode.
- **Batch Processing**: Modify `extract_ips` to process IPs in batches if memory usage becomes an issue with large CIDR ranges.

## Testing

To ensure changes don’t break existing functionality:

1. **Unit Tests**:

   - Currently, Astra lacks unit tests. Consider adding tests using `unittest` or `pytest`.
   - Example test for `extract_ips`:

     ```python
     import unittest
     from astra.network import extract_ips

     class TestNetwork(unittest.TestCase):
         def test_extract_ips(self):
             cidr_ranges = ["192.168.1.0/30"]
             ips = extract_ips(cidr_ranges, max_ips=2)
             self.assertEqual(len(ips), 2)
             self.assertEqual(ips, ["192.168.1.0", "192.168.1.1"])

     if __name__ == "__main__":
         unittest.main()
     ```

2. **Manual Testing**:
   - Test domain resolution: `python3 astra.py apple.com --first-1000 --verbose`
   - Test CIDR scanning: `python3 astra.py --cidr 192.168.1.0/30 --first-300 --first-2-per-cidr --verbose`
   - Test output: `python3 astra.py apple.com --output results.json --verbose`

## Contribution Guidelines

1. **Fork and Clone**:

   - Fork the repository on GitHub.
   - Clone your fork: `git clone https://github.com/bhaweshchaudhary/Astra.git`

2. **Create a Feature Branch**:

   - `git checkout -b feature/your-feature-name`

3. **Code Style**:

   - Follow PEP 8 guidelines.
   - Use type hints where possible (as seen in function signatures).
   - Add docstrings for new functions.

4. **Commit Messages**:

   - Use clear, descriptive messages: e.g., “Add UDP scanning support in network.py”

5. **Pull Request**:

   - Push your branch: `git push origin feature/your-feature-name`
   - Open a pull request on GitHub, describing your changes and testing steps.

6. **Testing**:
   - Ensure all existing functionality works.
   - Add tests for new features if possible.

## Known Limitations

- **No UDP Scanning**: Currently supports only TCP scanning. See “Extending Astra” for adding UDP support.
- **Resource Usage**: Large CIDR ranges or full port scans can be resource-intensive. Consider batching or reducing `max_workers`.
- **No IPv6 Support**: Astra handles IPv4 only. Extending to IPv6 requires updates to `api.py` and `network.py` to use `socket.AF_INET6`.
- **Error Handling**: While robust, some edge cases (e.g., network interruptions) may need additional handling.

## Future Enhancements

- Add support for IPv6 scanning.
- Implement UDP scanning for broader protocol coverage.
- Add unit tests to ensure reliability.
- Support additional output formats (e.g., XML, YAML).
- Introduce rate limiting to avoid overwhelming target networks.

## Contact

For questions or collaboration, reach out via GitHub issues at [https://github.com/bhaweshchaudhary/astra](https://github.com/bhaweshchaudhary/astra).

---

**Note**: Astra is for ethical use only. Developers and maintainers must ensure that any use of the tool complies with legal and ethical standards. Unauthorized network scanning is illegal.
