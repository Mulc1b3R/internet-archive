# internet-archive
archive.org

 -----------------------------------------------------------------------------------------------------------------------------

  Internet Archive Scripts

This repository contains two Python scripts demonstrating web scraping functionalities using the Internet Archive and related tasks.
```
look4.py
```
This script uses the Internet Archive Python library to search items based on a user-entered query and writes the results to a text file with the item URLs.
How to use:

    *  Run the script.
    *  Enter the search query when prompted.
    *  The script will fetch search results and write the URLs of items to a text file.
```
dir.py
```
This script fetches web content from a specified URL and lists files with specific extensions using BeautifulSoup and requests.
How to use:

    * Modify the url and extensions variables in the script.
    *Run the script.
    *It will retrieve the files with specified extensions from the URL and print their links.

Example usage for list_files_with_extensions.py:

    URL: https://archive.org/details/0-1-aky
    Extensions: .html, .txt, .pdf, .gif, .xml, .htm, .sqlite, .torrent, .gz, .zip, .json, .epub, .jpg, .png, .svg, .mp3, .mp4, .csv, .php

