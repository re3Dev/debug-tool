## To Update the Pi's Code
# Clone the repo
# Take each file from the repo and update the real file in here

## To Update the Repo's Code
# Connect to the remote repo
# Look at all files that could have possibly changed
# Grab them and update the repo folder
# Then push the repo folder

import os
import git
from shutil import copy2
import filecmp

##NOTE: Make sure to clone the repo first manually, update the repo's path (if needed) ##

REPO_PATH = "/home/pi/debug-tool" 
PATH_TO_BASE = "/home/pi"
PATH_TO_SCRIPTS = "/home/pi/saved_scripts"
PATH_TO_CONFIG = "/etc/OliveTin"
PATH_TO_ENTITIES = "/etc/OliveTin/entities"
PATH_TO_THEME = "/etc/OliveTin/custom-webui/themes/dark-mode"

# Define mappings for where to sync files
FOLDER_MAPPINGS = {
    "/home/pi/debug-tool/saved_scripts": PATH_TO_SCRIPTS,
    "/home/pi/debug-tool/entities": PATH_TO_ENTITIES
}

FILE_MAPPINGS = {
    "config.yaml": PATH_TO_CONFIG,
    "theme.css": PATH_TO_THEME,
}

os.environ["GIT_SSH_COMMAND"] = "ssh -i ~/.ssh/id_rsa"

repo = git.Repo(REPO_PATH)

def sync_pi_from_repo():

    # Pulls from the repo
    repo.remotes.origin.pull()

    for root, _, files in os.walk(REPO_PATH):
        if ".git" in root.split(os.sep):
            continue

        for file in files:
            if file.startswith("."):  # Ignore hidden files
                continue
            
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, REPO_PATH)
            
            # Determine the destination
            destination = FOLDER_MAPPINGS.get(root, None) or FILE_MAPPINGS.get(file, None)
            if file.endswith("html"):
                destination = PATH_TO_BASE

            if not destination:
                print(f"Skipping {file} (no predefined destination)")
                continue

            # Ensure the destination folder exists
            os.makedirs(destination, exist_ok=True)

            # # Copy file
            dest_file_path = os.path.join(destination, file)
            copy2(file_path, dest_file_path)
            print(f"{file} → {dest_file_path}")


def sync_repo_from_pi():
    changes_detected = False

    # Sync folders
    for file, system_path in FOLDER_MAPPINGS.items():
        source_dir = system_path
        repo_path = os.path.join(REPO_PATH, file)

        # Get all file paths inside source_dir
        source_paths = [
            os.path.join(dirpath, f)  # Construct full file path
            for dirpath, dirnames, filenames in os.walk(source_dir)
            for f in filenames
        ]

        print(f"Files in {source_dir}: {source_paths}")

        for source_path in source_paths:
            # Ensure the destination directory exists
            print(source_dir)

            os.makedirs(os.path.dirname(repo_path), exist_ok=True)
            # Check if file needs to be copied
            print(f"Updating repo with {source_path}...")
            copy2(source_path, repo_path)
            changes_detected = True
                
    # Sync individual files
    for file, system_path in FILE_MAPPINGS.items():

        source_path = os.path.join(system_path, file)
        repo_path = os.path.join(REPO_PATH, file)

        print(f"Files in {source_path}: {repo_path}")
        os.makedirs(os.path.dirname(repo_path), exist_ok=True)

        # Check if file needs to be copied
        print(f"Updating repo with {source_path}...")
        copy2(source_path, repo_path)
        changes_detected = True

    # Detect and copy .html files from /home/pi
    html_files = [
        f for f in os.listdir(PATH_TO_BASE)
        if f.endswith(".html") and os.path.isfile(os.path.join(PATH_TO_BASE, f))
    ]

    for html_file in html_files:
        source_path = os.path.join(PATH_TO_BASE, html_file)
        repo_dest = os.path.join(REPO_PATH, html_file)

        # Only copy if the file is new or has changed
        if not os.path.exists(repo_dest) or not filecmp.cmp(source_path, repo_dest, shallow=False):
            copy2(source_path, repo_dest)
            print(f"HTML file updated: {html_file}")
            changes_detected = True

    print(changes_detected)

    if changes_detected:
        print("Committing and pushing changes to the remote repo...")
        repo.git.add(A=True)  # Stage all changes
        commit_message = input("Enter the commit message: ")
        repo.index.commit(commit_message)  # Commit changes
        repo.remotes.origin.push()  # Push to remote
        print("Repo updated and pushed to remote!")
    else:
        print("No changes detected, skipping repo update.")


def main():
    choice = input("Enter 1 to update Pi's files from remote repo (Pull), or 0 to update remote repo from the Pi (Push): ").strip()

    if choice == "1":
        sync_pi_from_repo()  # Update pi files from the repo
    elif choice == "0":
        sync_repo_from_pi()  # Updates the remote repo from the pi
    else:
        print("Invalid choice. Please enter 1 or 0.")

if __name__ == '__main__':
    main()