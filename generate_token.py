from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# Define the required API scopes
SCOPES = ['https://www.googleapis.com/auth/presentations']

def main():
    creds = None
    # Check if token.json already exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If credentials are not valid, request new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials to token.json
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    print("token.json generated successfully!")

if __name__ == "__main__":
    main()
