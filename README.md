
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

## Google Photos API Setup

To use this script, you need to enable the Google Photos Library API and set up OAuth credentials. Follow these steps:

1. **Create a Google Cloud Project**  
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and name it (e.g., `Google Photos Downloader`).

2. **Enable the Google Photos Library API**  
   - In the API Library, search for "Google Photos Library API" and enable it.

3. **Set Up OAuth Consent Screen**  
   - Configure the OAuth consent screen with your app name and email.

4. **Create OAuth 2.0 Credentials**  
   - Create credentials for a "Desktop app" and download the `credentials.json` file.

5. **Move `credentials.json` to Project Directory**  
   - Place the file in the root of your project directory.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/josephnittala/google-photos-downloader.git
   cd google-photos-downloader
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Running the Script

To start downloading photos:

```bash
python download_google_photos.py
```

The first time you run the script, you'll be prompted to authenticate your Google account.

## Logging and Error Checking
The script logs all activities, including errors, to a file named `GoogPics_download.log`. This log file is created in the same directory as the script and contains information about the download process, including any failures.

## ⭐️ Support

If you find this project helpful, please give it a star ⭐ on GitHub! Your support means a lot! 

---

Take control of your google cloud storage and keep your memories safe! 🚀🎉🌟
