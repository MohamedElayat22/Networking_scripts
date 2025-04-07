import pandas as pd
import socket
import ssl
import sys
from datetime import datetime

# Function to check TLS information including supported versions
def check_tls_info(domain):
    # Define TLS versions in a list, remove TLSv1.3 for compatibility if necessary
    tls_versions = {
        'TLSv1': ssl.PROTOCOL_TLSv1,
        'TLSv1.1': ssl.PROTOCOL_TLSv1_1,
        'TLSv1.2': ssl.PROTOCOL_TLSv1_2
        # 'TLSv1.3': ssl.PROTOCOL_TLSv1_3  # Uncomment if using Python 3.7 or later
    }
    
    enabled_versions = []

    for version_name, version in tls_versions.items():
        try:
            # Create a new SSL context for the specific version
            context = ssl.SSLContext(version)
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain):
                    enabled_versions.append(version_name)  # If successful, add the version to list
        except (ssl.SSLError, Exception) as e:
            # Handle error (specific SSL issues or other exceptions)
            continue  

    return enabled_versions

# Main function
def main(input_file, output_file):
    results = []

    # Read domains from the input file
    try:
        with open(input_file, 'r') as f:
            domains = f.read().splitlines()  # Read and split lines into domain list
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        return

    for domain in domains:
        enabled_tls_versions = check_tls_info(domain.strip())
        
        if enabled_tls_versions:
            result_string = f"{domain}: Enabled TLS Versions: {', '.join(enabled_tls_versions)}"
        else:
            result_string = f"{domain}: No enabled TLS versions found"
        
        results.append(result_string)

    # Write results to output file
    with open(output_file, 'w') as f:
        f.write("\n".join(results))

    print(f"Results have been saved to: {output_file}")

# Execute the script
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file.txt> <output_file.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)
