import os
import shutil
import subprocess
import time
import zipfile
from threading import Thread

import requests
import schedule


def check_for_updates(repo_owner, repo_name, current_version):
    print("Checking for updates...")
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


def download_and_install_update(repo_owner, repo_name, asset_name, new_folder, old_folder):
    try:
        if old_folder != "":
            shutil.rmtree(old_folder)

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
        os.makedirs(new_folder, exist_ok=True)

        # Download the release asset
        response = requests.get(asset_url)
        response.raise_for_status()

        update_file_path = os.path.join(new_folder, asset_name)

        with open(update_file_path, 'wb') as update_file:
            update_file.write(response.content)

        # Extract the update
        with zipfile.ZipFile(update_file_path, 'r') as zip_ref:
            zip_ref.extractall(new_folder)
    except Exception as e:
        print(f"Error during update: {e}")


def check_install_updates():
    global current_version
    global update_folder
    global main_program_thread

    new_version, update = check_for_updates(repo_owner, repo_name, current_version)
    if update:
        print("New Version Available!")
        if main_program_thread != None:
            main_program_thread.stop()

        download_and_install_update(repo_owner, repo_name, asset_name, new_version, update_folder)
        current_version = new_version
        update_folder = current_version
        main_program_thread = Program(new_version, new_version)
        main_program_thread.start()

        print("Running Version:", current_version)
    else:
        print("No New Version Available")


def get_folders_in_directory(directory):
    try:
        # Get a list of all entries in the directory
        entries = os.listdir(directory)
        # Filter the entries to include only directories
        folders = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]

        return folders

    except Exception as e:
        print(f"Error getting folders in directory: {e}")
        return None


repo_owner = "rafaeldpsilva"
repo_name = "iot-building-monitoring"
asset_name = "iot-bm.zip"


class Program(Thread):
    def __init__(self, current_version, run_folder):
        Thread.__init__(self)
        self.current_version = current_version
        self.run_folder = run_folder
        self.process = 0

    def stop(self):
        print("Stoping Version:", self.current_version)
        self.process.terminate()
        os.chdir("..")

    def run(self):
        os.chdir(self.run_folder)
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
        self.process = subprocess.Popen(['python', 'api/main.py'])


current_version = "v0.0.1"
update_folder = current_version
main_program_thread = None

new_version, update = check_for_updates(repo_owner, repo_name, current_version)
if new_version in get_folders_in_directory("."):
    main_program_thread = Program(new_version, new_version)
    main_program_thread.start()
else:
    check_install_updates()

schedule.every().day.at("00:00").do(check_install_updates)
while True:
    schedule.run_pending()
    time.sleep(1)
