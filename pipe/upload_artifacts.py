import os
import shutil
import requests
from http import HTTPStatus

BITBUCKET_BASE_URL = "https://bitbucket.org"
BITBUCKET_API_BASE_URL = "api.bitbucket.org/2.0/repositories"


def upload_sarif(self):
    api_url = f"https://{self.user_name}:{self.bitbucket_app_password}@{BITBUCKET_API_BASE_URL}/{self.owner_name}/{self.repository_name}/downloads"
    self.log_info("Uploading SARIF.....")

    file_path =  os.path.join(os.getcwd(), '.bridge/Blackduck SARIF Generator/report.sarif.json')

    files = []
    with open(file_path, "rb") as f:
        files = {"files": (os.path.basename(file_path), f)}

        response = requests.post(api_url, files=files)

        if response.status_code ==  HTTPStatus.CREATED:
            uploaded_url = f"{BITBUCKET_BASE_URL}/{self.owner_name}/{self.repository_name}/downloads"
            self.log_info(f"SARIF file uploaded successfully to: {uploaded_url}")
        else:
            self.log_info(f"Failed to upload file. Status code: {response.status_code}")


def upload_diagnostics(self):
    api_url = f"https://{self.user_name}:{self.bitbucket_app_password}@{BITBUCKET_API_BASE_URL}/{self.owner_name}/{self.repository_name}/downloads"
    self.log_info("Uploading diagnostics.....")

    directory_path = os.path.join(os.getcwd(), '.bridge')
    zip_file_name = 'diagnostics'
    zip_file_path = os.path.join(os.getcwd(), zip_file_name + '.zip')

    shutil.make_archive(zip_file_name, 'zip', directory_path)

    files = {'files': open(zip_file_path, 'rb')}
    response = requests.post(api_url, files=files)

    if response.status_code ==  HTTPStatus.CREATED:
        uploaded_url = f"{BITBUCKET_BASE_URL}/{self.owner_name}/{self.repository_name}/downloads"
        self.log_info(f"Diagnostics uploaded successfully {uploaded_url}")
    else:
        self.log_info(f'Error uploading file: {response.text}')

    os.remove(zip_file_path)
