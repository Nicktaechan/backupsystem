import shutil
import os
import datetime

# Backup source directory
source_dir = 'C:/Users/nosiemo/Desktop/VLAN Hopping'
# Backup destination directory
destination_dir = 'C:/Users/nosiemo/Documents'

# Create a timestamp for the backup folder
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
backup_folder = os.path.join(destination_dir, 'backup_' + timestamp)

try:
    # Create the backup folder
    os.makedirs(backup_folder)

    # Iterate over files and directories in the source directory
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)

        # Check if item is a file
        if os.path.isfile(item_path):
            # Copy the file to the backup folder
            shutil.copy2(item_path, backup_folder)
        elif os.path.isdir(item_path):
            # Copy the entire directory to the backup folder
            shutil.copytree(item_path, os.path.join(backup_folder, item))

    print('Backup successful!')
except Exception as e:
    print(f'An error occurred during the backup process: {str(e)}')
