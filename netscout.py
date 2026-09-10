#!/usr/bin/env python3
"""
NetScout - Network Port & Service Scanner
Author: Veereswar
Purpose: Authorized security testing and personal lab use.

Requirements:
    sudo apt install nmap
    pip install python-nmap

Examples:
    python3 netscout.py
    python3 netscout.py 192.168.56.10 -p 1-1000
"""

import argparse
import ipaddress
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import nmap


APP_NAME = "NetScout"
VERSION = "1.0"


def banner():
    print(r"""
 _   _      _   ____                  _
| \ | | ___| |_| ___|  ___ __ _ _   _| |_
|  \| |/ _ \ __|___ \ / __/ _` | | | | __|
| |\  |  __/ |_ ___) | (_| (_| | |_| | |_
|_| \_|\___|\__|____/ \___\__,_|\__,_|\__|

        Network Port & Service Scanner
        Built by haxk
""")


def valid_target(value: str) -> str:
    """Accept an IPv4/IPv6 address or a network hostname."""
    try:
        ipaddress.ip_address(value)
        return value
    except ValueError:
        if not value or any(c.isspace() for c in value):
            raise argparse.ArgumentTypeError("Invalid target.")
        return value


def valid_port_range(value: str) -> str:
    """Validate PORT or START-END."""
    value = value.replace(" ", "")

    if value.isdigit():
        port = int(value)
        if 1 <= port <= 65535:
            return value
        raise argparse.ArgumentTypeError("Port must be between 1 and 65535.")

    parts = value.split("-")
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        raise argparse.ArgumentTypeError("Use PORT or START-END, e.g. 80 or 1-1000.")

    start, end = map(int, parts)
    if not (1 <= start <= end <= 65535):
        raise argparse.ArgumentTypeError("Port range must be between 1 and 65535.")

    return f"{start}-{end}"


def check_dependencies():
    if shutil.which("nmap") is None:
        print("[!] Nmap is not installed or is not in PATH.")
        print("    Install it with: sudo apt install nmap")
        sys.exit(1)


def normalize_ports(port_range: str) -> str:
    """Convert a single port into the format accepted by python-nmap."""
    return port_range


def run_scan(target: str, ports: str):
    scanner = nmap.PortScanner()

    print(f"[+] Target : {target}")
    print(f"[+] Ports  : {ports}")
    print("[+] Mode    : TCP SYN + service detection")
    print("[+] Starting scan...\n")

    try:
        scanner.scan(
            hosts=target,
            ports=ports,
            arguments="-sS -sV --open",
        )
    except nmap.PortScannerError as exc:
        print(f"[!] Nmap error: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"[!] Scan failed: {exc}")
        sys.exit(1)

    if target not in scanner.all_hosts():
        print("[!] Target did not return a scan result.")
        return []

    host_data = scanner[target]
    results = []

    for protocol in host_data.all_protocols():
        ports_found = sorted(host_data[protocol].keys())

        for port in ports_found:
            info = host_data[protocol][port]

            record = {
                "protocol": protocol,
                "port": port,
                "state": info.get("state", "unknown"),
                "service": info.get("name", ""),
                "product": info.get("product", ""),
                "version": info.get("version", ""),
                "extra_info": info.get("extrainfo", ""),
            }
            results.append(record)

    return results


def display_results(target: str, results):
    print("=" * 72)
    print(f"{APP_NAME} Results")
    print("=" * 72)

    if not results:
        print("No open TCP ports were identified in the selected range.")
        return

    print(f"{'PORT':<10}{'STATE':<10}{'SERVICE':<18}{'VERSION'}")
    print("-" * 72)

    for item in results:
        service = item["service"] or "unknown"
        version = " ".join(
            x for x in [item["product"], item["version"], item["extra_info"]] if x
        )
        print(
            f"{item['port']}/{item['protocol']:<5}"
            f"{item['state']:<10}"
            f"{service:<18}"
            f"{version}"
        )

    print("-" * 72)
    print(f"Open ports found: {len(results)}")


def save_json(target: str, ports: str, results, output_dir: str):
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = target.replace(":", "_").replace("/", "_")
    output_file = directory / f"scan_{safe_target}_{timestamp}.json"

    report = {
        "tool": APP_NAME,
        "version": VERSION,
        "target": target,
        "ports_scanned": ports,
        "timestamp": datetime.now().astimezone().isoformat(),
        "results": results,
    }

    output_file.write_text(json.dumps(report, indent=2))
    print(f"[+] JSON report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="NetScout - simple Nmap-based port and service scanner."
    )

    parser.add_argument(
        "target",
        nargs="?",
        type=valid_target,
        help="Authorized IP address or hostname to scan.",
    )

    parser.add_argument(
        "-p",
        "--ports",
        type=valid_port_range,
        default="1-1000",
        help="Port or range to scan. Default: 1-1000",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="reports",
        help="Directory for JSON reports. Default: reports",
    )

    args = parser.parse_args()

    banner()
    check_dependencies()

    target = args.target or input("Enter your authorized lab target: ").strip()
    if not target:
        print("[!] Target cannot be empty.")
        sys.exit(1)

    results = run_scan(target, normalize_ports(args.ports))
    display_results(target, results)
    save_json(target, args.ports, results, args.output)

    print("\n[+] Scan complete.")
    print("[!] Only scan systems you own or have explicit permission to test.")


if __name__ == "__main__":
    main()
