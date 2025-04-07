import sys
import ssl
from getpass import getpass

def authenticate_with_2fa(ip_address, username, password):
    """Authenticate with the F5 API and handle 2FA."""
    url = f"https://{ip_address}/mgmt/tm/system/hostname"
    
    session = requests.Session()
    
    # Disable SSL verification for self-signed certificates
    session.verify = False
    
    # Authenticate first with username and password
    response = session.get(url, auth=(username, password))
    
    if response.status_code == 200:
        print("Authentication successful. Waiting for 2FA...")
        
        # manual input for 2FA token
        two_fa_token = input("Enter your 2FA Code: ")

        # Send the 2FA code
        # response = session.post(url, headers={'2FA-Token': two_fa_token})

        # Re-attempt access with the session for device info after 2FA
        response = session.get(url, auth=(username, password))  # This may vary based on actual 2FA implementation

        if response.status_code == 200:
            hostname = response.json().get("name")  # Access the device hostname
            print(f"Device Hostname: {hostname}")
            return session  # Return authenticated session as needed
        else:
            print(f"Failed to retrieve hostname: {response.status_code} - {response.text}")
    else:
        print(f"Authentication failed: {response.status_code} - {response.text}")
    
    return None

def main():
    ip_address = input("Enter the F5 device IP address: ").strip()
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    authenticate_with_2fa(ip_address, username, password)

if __name__ == "__main__":
    main()
