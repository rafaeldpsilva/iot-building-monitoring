import os
import subprocess
import sys
import zipfile
import shutil
import requests


def check_for_updates(repo_owner, repo_name, current_version):
    try:
        # Get the latest release from GitHub
        releases_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
        response = requests.get(releases_url)
        response.raise_for_status()
        release_info = response.json()

        # Get the latest version from the release
        latest_version = release_info['tag_name']

        if latest_version > current_version:
            return latest_version, True
        else:
            return None, False

    except Exception as e:
        print(f"Error checking for updates: {e}")
        return None


def download_and_install_update(repo_owner, repo_name, asset_name, update_folder, old_folder):
    try:
        # Get the latest release from GitHub
        releases_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
        response = requests.get(releases_url)
        response.raise_for_status()
        release_info = response.json()

        # Get the download URL for the release asset
        for asset in release_info['assets']:
            if asset['name'] == asset_name:
                asset_url = asset['browser_download_url']
                break
        else:
            raise ValueError(f"Asset '{asset_name}' not found in the latest release.")

        # Create a temporary folder for the update
        os.makedirs(update_folder, exist_ok=True)

        # Download the release asset
        response = requests.get(asset_url)
        response.raise_for_status()

        update_file_path = os.path.join(update_folder, asset_name)

        with open(update_file_path, 'wb') as update_file:
            update_file.write(response.content)

        # Extract the update
        with zipfile.ZipFile(update_file_path, 'r') as zip_ref:
            zip_ref.extractall(update_folder)

        shutil.rmtree(old_folder)
        os.chdir(update_folder)
        # Install/update required pip packages
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)

        subprocess.run(['python', 'api/main.py'])

        # Exit the current instance of the application
        sys.exit(0)
    except Exception as e:
        print(f"Error during update: {e}")
        sys.exit(1)


# Example Usage
repo_owner = "rafaeldpsilva"
repo_name = "iot-building-monitoring"
asset_name = "iot-bm.zip"
current_version = "v0.0.1"

update_folder = "temp_update_folder"

current_version, update = check_for_updates(repo_owner, repo_name, current_version)
if update:
    download_and_install_update(repo_owner, repo_name, asset_name, current_version, update_folder)
    update_folder = current_version
