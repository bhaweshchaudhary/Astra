# Astra User Guide

**Last Updated**: May 15, 2025  
**Version**: 1.1

## Introduction
Welcome to the Astra User Guide! Astra is an open-source network scanning tool designed for security researchers, network administrators, and enthusiasts. Built with Python, Astra allows you to scan IP ranges, resolve domains to IPs, and identify open ports with a high degree of flexibility. Unlike many tools, Astra operates locally without third-party API dependencies, offering users control, privacy, and customization.

### Why Astra?
In a landscape filled with network scanning tools, Astra stands out by:
- Running locally, eliminating the need for external APIs.
- Providing customizable IP and port range options.
- Supporting both domain-based and CIDR-based scanning in one tool.
- Delivering detailed logging for transparency.

This guide will walk you through installing, configuring, and using Astra effectively.

## System Requirements
- **Operating System**: Linux, macOS, or Windows (tested on macOS and Linux).
- **Python Version**: Python 3.7 or higher.
- **Dependencies**: Managed via `requirements.txt` (installs `dnspython`).
- **Internet Connection**: Required for domain resolution; optional for CIDR-only scans.
- **Permissions**: May require `sudo` on some systems for certain port scans (ensure legal authorization).

## Installation
Follow these steps to set up Astra on your system:

1. **Clone the Repository**:
   - Open a terminal and run:
     ```bash
     git clone https://github.com/yourusername/astra.git
     cd astra
     ```

2. **Set Up a Virtual Environment**:
   - Create and activate a virtual environment to isolate dependencies:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

3. **Install Dependencies**:
   - Install required packages listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

4. **(Optional) Configure Settings**:
   - Create a config file at `~/.astra/config.json` to set defaults:
     ```json
     {
       "api_token": "",  // Leave empty unless using ipinfo.io (optional feature)
       "default_ports": "22,80,443,8080,8443",
       "default_timeout": 1.0
     }
     ```
   - This step is optional but recommended for frequent use.

5. **Verify Installation**:
   - Run `python3 astra.py -h` to display the help message and confirm the tool is working.

## Usage
Astra is operated via the command line. Below are detailed instructions on how to use it, including command options and examples.

### Basic Command Structure
```bash
python3 astra.py [org] [options]
```
- `[org]`: Organization name or domain (e.g., `apple.com`), optional if using `--cidr`.
- `[options]`: Customize the scan behavior (see Command-Line Options).

### Command-Line Options
Run `python3 astra.py -h` for the latest options. As of v1.1, the following are available:

- **Positional Argument**:
  - `org`: Organization name or domain (e.g., `apple` or `apple.com`). Optional if `--cidr` is used.

- **Optional Arguments**:
  - `-h, --help`: Display this help message and exit.
  - `--api-token API_TOKEN`: ipinfo.io API token (optional, overrides config; not used for core functionality).
  - `--ports PORTS`: Comma-separated ports to scan (e.g., `80,443`).
  - `--first-1000`: Scan the first 1,000 ports (0-999).
  - `--first-300`: Scan the first 300 ports (0-299).
  - `--max-ips-per-cidr MAX_IPS_PER_CIDR`: Maximum number of IPs to scan per CIDR range.
  - `--first-1-per-cidr`: Scan only the first IP per CIDR range.
  - `--first-2-per-cidr`: Scan only the first 2 IPs per CIDR range.
  - `--first-10-per-cidr`: Scan only the first 10 IPs per CIDR range.
  - `--timeout TIMEOUT`: Timeout for host/port scans in seconds (default: 1.0 from config).
  - `--max-ips MAX_IPS`: Maximum total number of IPs to scan (global limit).
  - `--verbose`: Enable verbose output with detailed logs.
  - `--output OUTPUT`: File to save results (e.g., `results.json`).
  - `--output-format {json,csv}`: Output format (default: json).
  - `--config CONFIG`: Path to config file (default: `~/.astra/config.json`).
  - `--cidr CIDR`: Comma-separated CIDR ranges to scan (e.g., `192.168.1.0/24`), skips domain resolution.

### Usage Examples
1. **Scan a Domain with Default Settings**:
   - Scan all ports for `apple.com`:
     ```bash
     python3 astra.py apple.com --verbose
     ```
   - Expected output includes resolved IPs, live hosts, and open ports.

2. **Scan a Domain with Limited Ports and IPs**:
   - Scan the first 1,000 ports for `facebook.com` with a maximum of 100 IPs:
     ```bash
     python3 astra.py facebook.com --first-1000 --max-ips 100 --timeout 2.0 --verbose
     ```
   - Adjusts timeout to 2 seconds for slower networks.

3. **Scan a CIDR Range**:
   - Scan the first 2 IPs of `17.44.246.0/23` with the first 300 ports:
     ```bash
     python3 astra.py --cidr 17.44.246.0/23 --first-300 --first-2-per-cidr --verbose
     ```
   - Limits scanning to the first two IPs in the CIDR range.

4. **Scan Multiple CIDR Ranges**:
   - Scan the first 2 IPs of two CIDR ranges:
     ```bash
     python3 astra.py --cidr 17.44.246.0/23,17.44.248.0/23 --first-300 --first-2-per-cidr --verbose
     ```
   - Processes multiple ranges in one command.

5. **Save Results to a File**:
   - Scan `apple.com` and save results in JSON:
     ```bash
     python3 astra.py apple.com --first-1000 --output results.json --verbose
     ```
   - Results are saved to `results.json` for later analysis.

### Output Interpretation
- **Verbose Mode**: Displays timestamps, log levels (DEBUG, INFO), and details like:
  - Resolved IPs (e.g., `Resolved 3 IPs for apple.com: ['17.253.144.10', ...]`).
  - IPs scanned (e.g., `Extracted 3 IPs`).
  - Live hosts and open ports (e.g., `Found 1 open ports - 17.253.144.10:80`).
- **Output File**: Contains structured data (JSON/CSV) with IPs, ports, and scan status.

## Configuration
- **Default Settings**: Loaded from `~/.astra/config.json` if present.
- **Override**: Command-line options (e.g., `--timeout`) override config values.
- **Example Config**: See Installation step 4.

## Troubleshooting
- **No IPs Resolved**:
  - Check your internet connection or DNS settings.
  - Ensure the domain is valid (e.g., `python3 astra.py invalid.domain --verbose` will log an error).
- **Permission Denied**:
  - Some ports may require `sudo` (e.g., `sudo python3 astra.py apple.com --first-1000 --verbose`).
  - Ensure legal authorization before using elevated privileges.
- **Timeout Issues**:
  - Increase `--timeout` (e.g., `--timeout 5.0`) for slower networks.
- **Large CIDR Scans**:
  - Use `--first-2-per-cidr` or `--max-ips` to limit resource usage.
- **Verbose Output Too Detailed**:
  - Omit `--verbose` for minimal output.

## Frequently Asked Questions (FAQs)
1. **Is Astra free?**
   - Yes, Astra is open-source under the MIT License.
2. **Can I scan any network?**
   - No, scanning requires explicit permission. Unauthorized scanning is illegal.
3. **Why only TCP scanning?**
   - Current version supports TCP only. UDP support is planned (see DEVELOPER.md).
4. **How do I contribute?**
   - Follow the guidelines in `DEVELOPER.md`.
5. **What if I encounter bugs?**
   - Report issues on the GitHub repository with steps to reproduce.

## Best Practices
- **Ethical Use**: Always obtain permission before scanning. Use Astra for authorized security testing (e.g., bug bounty programs).
- **Resource Management**: Limit `--max-ips` and use per-CIDR flags for large networks to avoid overloading your system.
- **Regular Updates**: Check the GitHub repository for updates and new features.
- **Backup Results**: Use `--output` to save scan data for analysis.

## Limitations
- **IPv4 Only**: Does not support IPv6 (planned for future releases).
- **TCP Only**: No UDP scanning (under development).
- **Resource Intensive**: Large scans may require significant memory and CPU; use limits wisely.
- **No GUI**: Command-line only; no graphical interface.

## Getting Help
- **GitHub Issues**: Submit questions or bugs at [https://github.com/yourusername/astra](https://github.com/yourusername/astra).
- **Documentation**: Refer to `USERGUIDE.md` and `DEVELOPER.md` in the repository.
- **Community**: Engage with other users via GitHub discussions (if enabled).

## License
Astra is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Developed with Python and enhanced with `dnspython` for robust DNS resolution.
- Inspired by the need for a customizable, local network scanning tool.

---

**Note**: Astra is for ethical use only. Unauthorized network scanning is illegal and may result in legal consequences. Ensure compliance with all applicable laws and obtain permission before use.