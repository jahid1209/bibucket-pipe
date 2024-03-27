import os
import zipfile
from os.path import expanduser
from bitbucket_pipes_toolkit import get_logger


logger = get_logger()

def extract_bridge(binary_path):
    logger.info('Executing the pipe...')

    # Expand the home directory path
    home_dir = expanduser("~")

    # Construct the path for the extracted directory
    extracted_dir = os.path.join(home_dir, "synopsys-bridge")

    try:
        os.makedirs(extracted_dir, exist_ok=True)

        with zipfile.ZipFile(binary_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)

        for root, dirs, files in os.walk(extracted_dir):
            for file in files:
                file_path = os.path.join(root, file)
                os.chmod(file_path, 0o755)

        # Remove the zip file
        os.remove(binary_path)

        return extracted_dir
    except Exception as e:
        print(f"Error extracting bridge zip file: {e}")
        return None