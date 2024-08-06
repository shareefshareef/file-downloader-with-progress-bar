# File Downloader with Progress Bar

This Python script provides a utility for downloading files from a given URL with an integrated progress bar. It's designed to be useful in various scenarios, including web scraping, where downloading large files or media is common.

## Features

- **Progress Bar:** Visual feedback on the download progress, making it easy to track the status of large file downloads.
- **Logging:** Detailed logs of the download process and error handling for easier debugging.
- **Error Handling:** Robust exception handling to ensure the program runs smoothly even when issues arise.

## Use Cases

- **Web Scraping:** Ideal for web scraping projects where large files or media need to be downloaded from various sources.
- **Data Collection:** Useful for collecting datasets or resources from the web in a reliable and trackable manner.
- **File Management:** Helpful for managing and tracking file downloads in any Python-based application.

## Prerequisites

- Python 3.x
- `requests` library (install with `pip install requests`)

## Usage

1. **Clone the Repository:** Download or clone the repository to your local machine.
2. **Modify the URL:** Update the `url` variable in the `download` function with the URL of the file you want to download.
3. **Run the Script:** Execute the script to start the download process.

Here's an example of how the script is used:

```python
import logging
import requests

BAR = chr(9608)

def getProgressBar(progress, total, barWidth=40):
    progressBar = ''
    progressBar += '['

    if progress > total:
        progress = total
    if progress < 0:
        progress = 0

    numberofBars = int((progress / total) * barWidth)

    progressBar += BAR * numberofBars
    progressBar += ' ' * (barWidth - numberofBars)
    progressBar += ']'

    percentComplete = round(progress / total * 100, 2)
    progressBar += ' ' + str(percentComplete) + '%'

    progressBar += ' ' + str(progress) + '/' + str(total)

    return progressBar

def get_image_size(url):
    response = requests.head(url)
    if 'Content-Length' in response.headers:
        return int(response.headers['Content-Length'])
    else:
        return None

logging.basicConfig(
    filename='download.log', 
    level=logging.INFO,       
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def download(link, name, ext='.mp4'):
    try:
        size = get_image_size(link)
        if size is None:
            print("Cannot determine file size")
            return
        
        res = requests.get(link, stream=True)
        logging.info("Getting URL data")
        res.raise_for_status()
        logging.info("Checking for connection error")
        logging.info("File opened.")
        logging.info("File download starting...")

        with open(f"{name}{ext}", 'wb') as file:
            total_downloaded = 0
            for chunk in res.iter_content(8192):
                if chunk:
                    file.write(chunk)
                    total_downloaded += len(chunk)
                    
                    progress_bar = getProgressBar(total_downloaded, size)
                    print(progress_bar, end="")
                    print('\b'*len(progress_bar), end='', flush=True)
        
        logging.info(f"{name} file download complete.")
        
    except Exception as e:
        logging.error(e)
    finally:
        logging.info("File closed.\n")

url = 'https://videos.pexels.com/video-files/5608091/5608091-uhd_2560_1440_24fps.mp4'

download(url, "crops")
