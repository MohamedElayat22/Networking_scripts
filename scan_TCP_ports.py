""" This script scans a target host for open TCP ports within a specified range, helping you quickly identify open and potentially unused ports.

How to Use

Confirm the PC will be used to run script has a ((TEMP)) access to the destination for TCP-ports = ANY

Save the script to a file, e.g., port_scanner.py.

Install Python (if not already installed).

Run the script from your terminal or command prompt:

bash
python port_scanner.py <host> [--start <start_port>] [--end <end_port>]
Replace <host> with the target IP address or domain name.

[--start <start_port>] (optional) — starting port number (default is 1).

[--end <end_port>] (optional) — ending port number (default is 1024).

Examples
Scan ports 1–1024 on host 192.168.1.10:

text
python scan_TCP_ports.py 192.168.1.10
Scan ports 20–100 on host example.com:

text
python scan_TCP_ports.py example.com --start 20 --end 100
Notes
Only scan hosts you have permission to test!
"""


import socket
import argparse

def print_banner(host):
    banner_text = f"Scanning TCP ports for Host {host}"
    border = "=" * len(banner_text)
    print(border)
    print(banner_text.upper())
    print(border)
    print("by Ragab")
    print("github: @MohamedElayat22\n")

def scan_tcp_ports(host, start_port, end_port):
    print(f"Starting TCP scan from port {start_port} to {end_port}...\n")
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((host, port))
                if result == 0:
                    print(f"Port {port} is OPEN (TCP)")
                    open_ports.append(port)
        except Exception as e:
            print(f"Error scanning TCP port {port}: {e}")
    return open_ports

def main():
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("host", help="Target host IP or domain")
    parser.add_argument("--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("--end", type=int, default=65535, help="End port (default: 65535)")
    args = parser.parse_args()

    print_banner(args.host)
    open_ports = scan_tcp_ports(args.host, args.start, args.end)

    if open_ports:
        print(f"\nOpen TCP ports: {open_ports}")
    else:
        print("\nNo open TCP ports found in the specified range.")

if __name__ == "__main__":
    main()
