import os
import requests
import logging
import webbrowser
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# Scopes for accessing Google Photos
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

MONTHS = {
    '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
    '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
    '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
}

webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"))

def setup_logging(log_file):
    """Setup logging to console and a specified log file."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    
    # Formatter for handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    # Adding handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

def authenticate_google_photos():
    """Authenticate and return the Google Photos service."""
    creds = None
    # Check if token.json exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials, request new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('photoslibrary', 'v1', credentials=creds, static_discovery = False)

def download_file(item, month_path, year, month_name):
    """Download a single file."""
    try:
        date_str = item['mediaMetadata'].get('creationTime')
        mime_type = item['mimeType']
        media_url = item['baseUrl']

        if 'video' in mime_type or 'audio' in mime_type:
            media_url += '=dv'  # Download video/audio in original quality
        else:
            media_url += '=d'   # Download images in original quality

        response = requests.get(media_url, stream=True)
        
        if response.status_code == 200:
            file_name = item['filename']
            file_path = os.path.join(month_path, file_name)
            
            # Save the media file
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            logging.info(f"Downloaded {file_name} to {month_path}")
            
            # Set the file's modification and access times to match the original creation time
            creation_time = datetime.fromisoformat(date_str[:-1]).timestamp()
            os.utime(file_path, (creation_time, creation_time))
        else:
            logging.error(f"Failed to download {item['filename']} from {year}/{month_name}")

    except Exception as e:
        # Log any exception that occurs during download
        logging.error(f"Failed to download {item['filename']} from {year}/{month_name} due to error:\n{e}")

def download_media(service, base_path, max_workers=4):
    """Download photos and save them into respective month folders."""
    page_token = None
    current_year = None
    current_month = None

    while True:
        results = service.mediaItems().list(pageSize=100, pageToken=page_token).execute()
        items = results.get('mediaItems', [])

        # Create a ThreadPoolExecutor for concurrent downloads
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for item in items:
                date_str = item['mediaMetadata'].get('creationTime')
                if date_str:
                    date_parts = date_str.split('-')
                    year = date_parts[0]
                    month = date_parts[1]
                    month_name = MONTHS.get(month, month)  # Get month name

                    if (year != current_year) or (month != current_month):
                        # Update folder paths if year or month has changed
                        if current_year is not None:
                            logging.info(f"Completed processing {current_year}/{MONTHS[current_month]}")
                        current_year = year
                        current_month = month
                        month_path = os.path.join(base_path, current_year, month_name)
                        os.makedirs(month_path, exist_ok=True)
                        logging.info(f"Created folders for {current_year}/{month_name}")

                    # Submit download tasks to the executor
                    futures.append(executor.submit(download_file, item, month_path, year, month_name))
            
            # Wait for all downloads to complete
            for future in as_completed(futures):
                try:
                    future.result()  # Raise any exceptions encountered during download
                except Exception as e:
                    logging.error(f"Error occurred in thread: {e}")

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    logging.info("All media downloaded.")

def main():
    """Main function to authenticate and list unique months by year."""
    log_file = 'GoogPics_download.log'
    setup_logging(log_file)
    service = authenticate_google_photos()
    base_path = os.path.dirname(os.path.abspath(__file__))
    download_media(service, base_path)

if __name__ == '__main__':
    main()
