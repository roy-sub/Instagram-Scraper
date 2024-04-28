import shutil
import os

class Downloader:
    def __init__(self):
        
        self.save_path = os.path.expanduser('~')  # Root folder path

    def download_json_from_vscode(self, json_file_path):
        
        filename = json_file_path.split('/')[-1] # Extract filename from the provided path
        
        try:
            
            shutil.copyfile(json_file_path, os.path.join(self.save_path, filename)) # Copy the JSON file to the root folder
        
        except Exception as e:
            
            print(f"Failed to copy JSON file. Error: {e}") # Handle any exceptions that occur during copying
