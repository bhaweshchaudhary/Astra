import ipaddress
import socket
import concurrent.futures
import logging
from typing import List, Set, Tuple

def extract_ips(cidrs: List[str], max_ips: int = None) -> List[str]:
    """Convert CIDR ranges to a list of IPs."""
    all_ips = []
    for cidr in cidrs:
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            ips = [str(ip) for ip in network]
            if max_ips and len(ips) > max_ips:
                logging.warning(f"Limiting {cidr} to {max_ips} IPs (out of {len(ips)})")
                ips = ips[:max_ips]
            all_ips.extend(ips)
        except ValueError as e:
            logging.error(f"Invalid CIDR {cidr}: {e}")
    logging.info(f"Extracted {len(all_ips)} IPs")
    return all_ips

def is_host_alive(ip: str, timeout: float) -> bool:
    """Check if a host is alive using TCP connect to port 80."""
    logging.debug(f"Checking if {ip} is alive")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, 80))
        alive = result == 0
        logging.debug(f"{ip} is {'alive' if alive else 'not alive'}")
        return alive
    except socket.error:
        logging.debug(f"{ip} is not alive (socket error)")
        return False
    finally:
        sock.close()

def scan_port(ip: str, port: int, timeout: float) -> Tuple[str, int, bool]:
    """Scan a specific port on an IP."""
    logging.debug(f"Scanning {ip}:{port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, port))
        is_open = result == 0
        logging.debug(f"{ip}:{port} is {'open' if is_open else 'closed'}")
        return ip, port, is_open
    except socket.error:
        logging.debug(f"{ip}:{port} scan failed (socket error)")
        return ip, port, False
    finally:
        sock.close()

def scan_hosts(ips: List[str], timeout: float, max_workers: int = 50) -> Set[str]:
    """Check which IPs are alive."""
    logging.info(f"Scanning {len(ips)} IPs for live hosts")
    live_hosts = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(is_host_alive, ip, timeout): ip for ip in ips}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    live_hosts.add(ip)
            except Exception as e:
                logging.error(f"Error checking {ip}: {e}")
    logging.info(f"Found {len(live_hosts)} live hosts")
    return live_hosts

def scan_ports(live_hosts: Set[str], ports: List[int], timeout: float, max_workers: int = 100) -> List[Tuple[str, int]]:
    """Scan specified ports on live hosts."""
    logging.info(f"Scanning ports {ports} on {len(live_hosts)} live hosts")
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_scan = {
            executor.submit(scan_port, ip, port, timeout): (ip, port)
            for ip in live_hosts
            for port in ports
        }
        for future in concurrent.futures.as_completed(future_to_scan):
            ip, port = future_to_scan[future]
            try:
                ip, port, is_open = future.result()
                if is_open:
                    open_ports.append((ip, port))
            except Exception as e:
                logging.error(f"Error scanning {ip}:{port}: {e}")
    logging.info(f"Found {len(open_ports)} open ports")
    return open_ports
