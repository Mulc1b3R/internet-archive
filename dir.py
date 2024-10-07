import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def list_files_with_extensions(url, extensions):
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch content.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    files = []
    file_extensions = tuple(extensions)
    
    for link in soup.find_all('a'):
        if 'href' in link.attrs:
            href_value = link.get('href')
            if href_value and href_value.endswith(file_extensions):
                files.append(urljoin('https://archive.org', href_value))

    if files:
        print(f"Files with extensions {file_extensions}:")
        for file in files:
            print(file)
    else:
        print(f"No files found with extensions {file_extensions}")

url = 'https://archive.org/details/0-1-aky'

extensions = ('.html', '.txt', '.pdf', '.gif', '.xml', '.htm', '.sqlite', '.torrent', '.gz', '.zip', '.json', '.epub', '.jpg', '.png', '.svg', '.mp3', '.mp4', '.csv', '.php')

list_files_with_extensions(url, extensions)