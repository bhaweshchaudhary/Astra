---

# 🌐 **Astra: A Powerful Network Scanner**

**Astra** is an open-source network scanning tool built for security researchers and network administrators. Written in Python, it efficiently scans IP ranges, resolves domains, and detects open ports using local DNS resolution and concurrent scanning.

---

## 🚀 Features

* **🔍 Domain Resolution**
  Resolve domains (e.g., `apple.com`) to multiple IPs using `dnspython`.

* **📡 CIDR Scanning**
  Scan single or multiple CIDR ranges, e.g., `192.168.1.0/24`, `10.0.0.0/8`.

* **🔐 Flexible Port Scanning**

  * Scan all **65,535 ports** by default
  * Use `--first-1000` or `--first-300` for common ports
  * Customize with `--ports 80,443,...`

* **📏 IP Scanning Limits**

  * Global IP scan cap with `--max-ips`
  * CIDR-specific cap with `--max-ips-per-cidr`, or quick options:
    `--first-1-per-cidr`, `--first-2-per-cidr`, `--first-10-per-cidr`

* **🧾 Output Options**
  Save results in **JSON** or **CSV** with `--output-format`

* **🔧 Configuration & Verbose Logging**
  Use CLI flags or a config file (`~/.astra/config.json`)
  Enable detailed logging with `--verbose`

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/bhaweshchaudhary/astra.git
cd astra

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install dnspython
```

> **Optional**: Create a config file at `~/.astra/config.json`

```json
{
  "api_token": "",
  "default_ports": "22,80,443,8080,8443",
  "default_timeout": 1.0
}
```

---

## ⚙️ Usage

```bash
python3 astra.py [org] [options]
```

### 🔧 Examples

```bash
# Scan all ports for apple.com with a global IP limit
python3 astra.py apple.com --max-ips 100 --verbose

# Scan first 1000 ports for facebook.com with a 2s timeout
python3 astra.py facebook.com --first-1000 --timeout 2.0 --max-ips 100 --verbose

# Scan CIDR range with the first 2 IPs per range
python3 astra.py --cidr 17.44.246.0/23 --first-300 --first-2-per-cidr --verbose

# Scan multiple CIDRs
python3 astra.py --cidr 17.44.246.0/23,17.44.248.0/23 --first-300 --first-2-per-cidr --verbose
```

---

## 🧩 Command-Line Options

```
usage: astra.py [org] [options]

positional arguments:
  org                               Domain/organization name (e.g., apple.com) [optional if --cidr used]

optional arguments:
  -h, --help                        Show this help message and exit
  --api-token API_TOKEN            ipinfo.io API token
  --ports PORTS                    Comma-separated list of ports (e.g., 80,443)
  --first-1000                     Scan first 1000 ports (0–999)
  --first-300                      Scan first 300 ports (0–299)
  --timeout TIMEOUT                Set timeout (default: 1.0)
  --max-ips MAX_IPS                Global limit on IPs to scan
  --max-ips-per-cidr NUM           Limit IPs per CIDR
  --first-1-per-cidr               Scan first IP per CIDR
  --first-2-per-cidr               Scan first 2 IPs per CIDR
  --first-10-per-cidr              Scan first 10 IPs per CIDR
  --verbose                        Enable detailed logs
  --output OUTPUT                  Output filename (e.g., results.json)
  --output-format {json,csv}       Output format
  --config CONFIG                  Path to config file
  --cidr CIDR                      Comma-separated CIDR ranges to scan
```

---

## 🤝 Contributing

Contributions are welcome! Fork the repo, create a new feature branch, and open a pull request.

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

## 🙏 Acknowledgments

* Built with Python 🐍 and powered by [`dnspython`](https://www.dnspython.org/)
* Inspired by the need for flexible, fast, and local-first network scanning tools.

---