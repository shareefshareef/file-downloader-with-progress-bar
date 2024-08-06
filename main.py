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

def download(link, name,ext='.mp4'):
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
                    print(progress_bar,end="")
                    print('\b'*len(progress_bar),end='',flush=True)
        

        logging.info(f"{name} file download complete.")
        
    except Exception as e:
        logging.error(e)
    finally:
        logging.info("File closed.\n")

url = 'https://videos.pexels.com/video-files/5608091/5608091-uhd_2560_1440_24fps.mp4'

download(url, "crops")
