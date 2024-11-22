# Global dictionary to simulate environment variables
env = {}

def load_secrets(token_path="secret.key", wifi_cred_path="wifi_cred.txt"):
    """
    Reads a secrets file and returns a dictionary of its contents.

    :param file_path: The path to the secrets file.
    :return: A dictionary with keys: 'secret_token', 'AP', and 'PW'.
    """
    global env
    try:
        # Token File
        with open(token_path, "r") as file:
            lines = file.readlines()
            if len(lines) < 1:
                raise ValueError("The secrets file must have at least three lines for secret_token.")
            
            # Assigning values to dictionary
            env['secret_token'] = lines[0].strip()
        
        # Wifi File
        with open(wifi_cred_path, "r") as file:
            lines = file.readlines()
            if len(lines) < 2:
                raise ValueError("The secrets file must have at least three lines for AP and PW.")
            
            # Assigning values to dictionary
            env['AP'] = lines[0].strip()
            env['PW'] = lines[1].strip()
    except OSError:
        print(f"Failed to open the file: {file_path}")
    except Exception as e:
        print(f"Error reading secrets file: {e}")

# URL with the above UID and PWD, eg
# http://192.168.4.44/ait/Hi-AIT-123

def is_authenticated(request):
    """Check if the request URL contains the correct token."""
    if not env['secret_token']:
        print("Secret token is missing.")
        return False
    
    # Extract token from URL in request
    try:
        # Split the request line and extract the token
        request_line = request.decode().split('\r\n')[0]
        path = request_line.split()[1]  # Extract the URL path
        token_param = path.split('token=')[-1] if 'token=' in path else None
    except IndexError:
        print("Malformed request.")
        return False

    if token_param == env['secret_token']:
        return True
    else:
        print("Invalid token.")
        return False
