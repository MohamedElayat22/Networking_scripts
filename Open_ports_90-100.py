""" This script is being used to open TCP/UDP ports range 90-100 for source localhost=127.0.0.1 for testing purposes

Range can be modified as well the source IP

Note: Open only for trusted source IPs

IP = ANY = 0.0.0.0  ISNOT recommended"""

import socket
import threading

HOST = '127.0.0.1'  # Listen on all interfaces
START_PORT = 90
END_PORT = 100

def tcp_listener(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen()
        print(f"TCP listening on port {port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"TCP connection from {addr} on port {port}")
                # Echo back received data
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

def udp_listener(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, port))
        print(f"UDP listening on port {port}")
        while True:
            data, addr = s.recvfrom(1024)
            print(f"UDP message from {addr} on port {port}: {data.decode(errors='ignore')}")
            # Echo back data
            s.sendto(data, addr)

def main():
    threads = []

    for port in range(START_PORT, END_PORT + 1):
        t_tcp = threading.Thread(target=tcp_listener, args=(port,), daemon=True)
        t_udp = threading.Thread(target=udp_listener, args=(port,), daemon=True)
        t_tcp.start()
        t_udp.start()
        threads.extend([t_tcp, t_udp])

    print(f"Listening on TCP & UDP ports from {START_PORT} to {END_PORT}...")
    try:
        while True:
            # Keep main thread alive while listeners run
            pass
    except KeyboardInterrupt:
        print("\nShutting down listeners.")

if __name__ == "__main__":
    main()
