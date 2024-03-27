import os
import requests
from os.path import expanduser


def download_bridge(url):
    home_dir = expanduser("~")

    file_path = os.path.join(home_dir, "bridge.zip")

    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        return file_path
    except requests.RequestException as e:
        print(f"Error downloading synopsys-bridge binary from {url}: {e}")
        return None
    

def print_directory_files():
    files = os.listdir(".")

    # Print the list of files
    print(f"Files in current directory")
    for file in files:
        print(file)