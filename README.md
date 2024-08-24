
# Google Photos Downloader

This Python script allows you to download photos and videos from Google Photos, organized by year and month. The script uses the Google Photos Library API to fetch and download files.

## Features

- Downloads photos and videos from Google Photos.
- Organizes files into folders by year and month.
- Handles exceptions and logs download errors.

## Requirements

- Python 3.7+
- Google Photos Library API enabled on your Google Cloud project.
- `requests`, `google-auth`, `google-auth-oauthlib`, and `google-api-python-client` Python packages.

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/google-photos-downloader.git
   cd google-photos-downloader
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Enable the Google Photos Library API and download your `credentials.json` file. Place it in the project directory.

5. Run the script:
   ```bash
   python download_google_photos.py
   ```


