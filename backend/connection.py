import os.path
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the required scopes for Google Slides and Drive APIs
SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

def get_creds():
    """
    Authenticate and authorize the user using credentials.json.
    """
    creds = None

    if os.path.exists('token.json'):
        try:
            logger.info("Loading credentials from token.json...")
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception as e:
            logger.error(f"Failed to load credentials from token.json: {e}")
            logger.info("Deleting corrupted token.json and starting fresh...")
            os.remove('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            logger.info("No valid credentials found. Starting OAuth flow...")
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except FileNotFoundError:
                logger.error("Error: credentials.json file not found.")
                raise
            except Exception as e:
                logger.error(f"An error occurred during OAuth flow: {e}")
                raise

        logger.info("Saving credentials to token.json...")
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_slides_service():
    """
    Build and return the Google Slides API service.
    """
    try:
        logger.info("Building Google Slides service...")
        slides_service = build('slides', 'v1', credentials=get_creds())
        return slides_service
    except HttpError as error:
        logger.error(f"An error occurred while building Slides service: {error}")
        raise

def get_drive_service():
    """
    Build and return the Google Drive API service.
    """
    try:
        logger.info("Building Google Drive service...")
        drive_service = build('drive', 'v3', credentials=get_creds())
        return drive_service
    except HttpError as error:
        logger.error(f"An error occurred while building Drive service: {error}")
        raise