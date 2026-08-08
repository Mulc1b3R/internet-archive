import os
import json
import urllib.parse
import requests
import re
from bs4 import BeautifulSoup

# ===================================================================== #
#             🗄️ INTERNET ARCHIVE INGESTION CONFIGURATION 🗄️ #
# ===================================================================== #
# Target node folder directory path containing the assets (Strictly /download/)
ARCHIVE_URL = "https://archive.org/download/the-avengers-volume-1-1993-uk-vhs/"

# Target Master JSON File
JSON_FILE = "avengers2.json"

def fetch_archive_metadata(base_url):
    """
    Connects to the hidden _meta.xml file to harvest true historical properties.
    Falls back gracefully to standard directory token parsing if tags are missing.
    """
    metadata = {
        "artist": "the-avengers-volume-1",
        "year": "1960's",
        "genre": "Archival",
        "id": "S23-GEN-0001"
    }
        
    # Isolate the exact unique folder folder item ID token directly from our root link
    item_id = base_url.rstrip('/').split('/')[-1]
        
    # Point directly to the metadata XML document inside the download repository
    meta_xml_url = f"{base_url.rstrip('/')}/{item_id}_meta.xml"
        
    print(f" -> Connecting to Deep Metadata Layer: {item_id}_meta.xml")
    try:
        response = requests.get(meta_xml_url, timeout=15)
        if response.status_code == 200:
            meta_soup = BeautifulSoup(response.text, 'xml')
                        
            creator = meta_soup.find('creator') or meta_soup.find('artist')
            if creator and creator.text.strip():
                metadata["artist"] = creator.text.strip().title()
                            
            date = meta_soup.find('date') or meta_soup.find('year')
            if date and date.text.strip():
                year_match = re.search(r'\d{4}', date.text.strip())
                metadata["year"] = year_match.group(0) if year_match else date.text.strip()
                            
            subject = meta_soup.find('subject') or meta_soup.find('genre')
            if subject and subject.text.strip():
                clean_genre = subject.text.strip().split(';')[0].split(',')[0]
                metadata["genre"] = f"Archival {clean_genre.strip().title()} / Shellac 78"
                            
            numeric_id = meta_soup.find('identifier-access') or meta_soup.find('numeric_id')
            if numeric_id and numeric_id.text.strip():
                digits = ''.join(filter(str.isdigit, numeric_id.text.strip()))
                metadata["id"] = f"S23-45-{digits[-4:]}" if len(digits) >= 4 else f"S23-45-0601"
            else:
                metadata["id"] = f"S23-45-{hash(item_id) % 10000:04d}"
            
            print(f"    ✔ Successfully Ledgered: {metadata['artist']} ({metadata['year']}) | ID: {metadata['id']}")
                
    except Exception as e:
        print(f"    ⚠️ Metadata extraction handshake delayed: {e}. Utilizing standard repository fallback tracking.")
            
    return metadata

def clean_title_text(filename_without_ext):
    """Cleans up raw filename segments into a beautiful uppercase track title."""
    filename_only = filename_without_ext.split('/')[-1]
    decoded = urllib.parse.unquote(filename_only)
        
    # Strip messy track numbering prefixes like "01.02. " or "01-"
    clean = re.sub(r'^[\d\.\s_-]+', '', decoded)
        
    clean = clean.replace("-", " ").replace("_", " ")
    return " ".join(clean.split()).upper()

def run_archive_pipeline():
    print(f"=====================================================================")
    print(f"       🏛️ SECTION 23 INTELLIGENT METADATA INGESTION CONSOLE 🏛️       ")
    print(f"=====================================================================")
    print(f" -> Initializing connection connection to: {ARCHIVE_URL}\n")

    scraped_meta = fetch_archive_metadata(ARCHIVE_URL)

    # Establish our clean baseline root path straight from configuration
    download_base_url = ARCHIVE_URL.rstrip('/')
    item_id = download_base_url.split('/')[-1]

    try:
        # Request directory structure mapping data
        response = requests.get(f"{download_base_url}/", timeout=15)
        if response.status_code != 200:
            print(f"❌ Error: Cannot reach server page. Status code: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Connection Failure: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a') if a.get('href')]

    mp4_files = []
    jpg_files = []
        
    # Process base layer listings 
    for link in links:
        link_lower = link.lower()
        if link_lower.endswith('.mp4'):
            mp4_files.append(link)
        if link_lower.endswith('__ia_thumb.jpg'):
            jpg_files.append(link)

    # Automatically map and step inside folder directories (like disc1/)
    sub_dirs = [l for l in links if l.endswith('/') and not l.startswith('..') and not l.startswith('/')]
        
    for sub_dir in sub_dirs:
        sub_url = f"{download_base_url}/{sub_dir}"
        try:
            sub_res = requests.get(sub_url, timeout=15)
            if sub_res.status_code == 200:
                sub_soup = BeautifulSoup(sub_res.text, 'html.parser')
                sub_links = [a.get('href') for a in sub_soup.find_all('a') if a.get('href')]
                for sl in sub_links:
                    if sl.lower().endswith('.mp4'):
                        mp4_files.append(f"{sub_dir}{sl}")
                    if sl.lower().endswith('__ia_thumb.jpg'):
                        jpg_files.append(f"{sub_dir}{sl}")
        except Exception:
            pass

    if not mp4_files:
        print("⚠ Warning: No valid video MP4 elements discovered on this directory leaf.")
        return

    # STEP B: Map the clean high-res thumbnail sleeve image cover
    remote_image_path = "assets/default_cover.jpg"
    if jpg_files:
        clean_jpg_filename = jpg_files[0].split('/')[-1]
        remote_image_path = f"{download_base_url}/{clean_jpg_filename}"
        print(f" -> Target Sleeve Artwork Acquired: {remote_image_path}")
    else:
        item_images = [l for l in links if 'itemimage' in l.lower() and l.lower().endswith('.jpg')]
        if item_images:
            clean_jpg_filename = item_images[0].split('/')[-1]
            remote_image_path = f"{download_base_url}/{clean_jpg_filename}"

    print(f"\n -> Vault Cracked! Parsing {len(mp4_files)} dynamic recording entries into the database...")

    # STEP C: Map each individual track to the exact matching properties format (1 by 1)
    for mp4_filename in mp4_files:
        raw_base_name, _ = os.path.splitext(mp4_filename)
        display_title = clean_title_text(raw_base_name)
                
        # Build the pristine path link combining download base path and filename cleanly
        unadulterated_mp4_url = f"{download_base_url}/{mp4_filename.lstrip('/')}"
        
        new_catalog_entry = {
            "id": scraped_meta["id"],
            "artist": scraped_meta["artist"],
            "title": display_title,
            "year": scraped_meta["year"],
            "genre": scraped_meta["genre"],
            "format": "Digital MP4 Video / Archive Master",
            "source_platform": "archive",
            "unadulterated_source_url": unadulterated_mp4_url,
            "local_image_path_target": remote_image_path,  
            "premium_vault_download": f"mp4/{scraped_meta['id']}.7z",
            "pricing": {
                "mp4_stream_preview": "0.00",
                "hd_digital_download": "2.50",
                "physical_dvd_post": "2.50"
            },
            "tags": [
                scraped_meta["artist"].lower(),
                "video",
                "archive",
                display_title.lower()
            ]
        }

        # STEP D: Load the existing file array data to append records safely (Line by Line)
        catalog_data = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                try:
                    catalog_data = json.load(f)
                    if not isinstance(catalog_data, list): 
                        catalog_data = [catalog_data]
                except json.JSONDecodeError:
                    catalog_data = []

        if not any(item.get('unadulterated_source_url') == unadulterated_mp4_url for item in catalog_data):
            catalog_data.append(new_catalog_entry)
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(catalog_data, f, indent=4, ensure_ascii=False)
            print(f"    ✔ Successfully Catalogued -> {display_title}")
        else:
            print(f"    ⚠️ Skipped duplicate record -> {display_title}")

if __name__ == "__main__":
    run_archive_pipeline()
