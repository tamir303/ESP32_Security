# connect to access point
AP = const('TamirSP')
PW = const('Lipazb23')

# WEB token
def load_secret_token(file_path='secret.key'):
    """Load the secret token from a file."""
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()  # Read and strip whitespace/newline
    except FileNotFoundError:
        print("Secret key file not found.")
        return None
    
SECRET_TOKEN = load_secret_token()

# URL with the above UID and PWD, eg
# http://192.168.4.44/ait/Hi-AIT-123

def is_authenticated(request):
    """Check if the request URL contains the correct token."""
    if not SECRET_TOKEN:
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

    if token_param == SECRET_TOKEN:
        return True
    else:
        print("Invalid token.")
        return False
