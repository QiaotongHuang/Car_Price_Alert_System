import os
import base64
import logging
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(
    filename='project.log',  # Log file to write to
    filemode='a',                 # Append mode
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO            # Set logging level to INFO
)

logger = logging.getLogger(__name__) 

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """Shows basic usage of the Gmail API. Sends an email."""
    creds = None
    # Check if token.json exists (stores user's access and refresh tokens)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no (valid) credentials are available, prompt user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def send_email(creds, to, subject, message_text):
    """Send an email using Gmail API"""
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        message = (service.users().messages().send(userId='me', body={'raw': raw_message}).execute())
        logger.info(f"Message Id: {message['id']}")  # Log message ID
        logger.info("Email sent successfully.")  # Log success message
    except Exception as error:
        logger.error(f"An error occurred: {error}")  # Log error message

if __name__ == '__main__':
    # Authenticate and get credentials
    creds = authenticate_gmail()

    # Send an email
    send_email(
        creds,
        to="test_address",
        subject="Test Email",
        message_text="This is a test email sent from Python!"
    )
