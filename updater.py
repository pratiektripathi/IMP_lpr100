import requests
import zipfile
import io
import os
import shutil

def download_github_repo(dest_folder="downloaded_repo"):
    url = "https://github.com/pratiektripathi/lpr100exe/archive/refs/heads/main.zip"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Unzipping the content
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(dest_folder)
        
    else:
        print(f"Failed to download repository: {response.status_code}")




def copy_and_replace(source_folder="downloaded_repo/lpr100exe-main/", destination_folder="/"):
    # Check if destination folder exists, create if it doesn't
    if not os.path.exists(destination_folder):
        pass
    else:
        for filename in os.listdir(source_folder):
            source_file = os.path.join(source_folder, filename)
            destination_file = os.path.join(destination_folder, filename)
            shutil.copy2(source_file, destination_file)  # Overwrite if exists

    print(f"All files from {source_folder} copied to {destination_folder} with replacement.")




# download_github_repo()

copy_and_replace()