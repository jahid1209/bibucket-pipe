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
        # Create the directory if it doesn't exist
        os.makedirs(extracted_dir, exist_ok=True)

        # Extract the contents of the zip file
        with zipfile.ZipFile(binary_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)

        # Give execute permission to all extracted files
        for root, dirs, files in os.walk(extracted_dir):
            for file in files:
                file_path = os.path.join(root, file)
                os.chmod(file_path, 0o755)  # Give execute permission to owner, group, and others

        # Remove the zip file
        # os.remove(binary_path)

        return extracted_dir
    except Exception as e:
        print(f"Error extracting bridge zip file: {e}")
        return None