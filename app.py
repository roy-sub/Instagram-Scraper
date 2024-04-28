import os
import shutil
from scrape_insta_profile import InstagramScraper
from data_post_processing import InstagramDataProcessor
from download_file import Downloader
from notification import EmailSender
from constants import IMAGE_URL_JSON_PATH, CAPTION_JSON_PATH, MIDDLEWARE 

class Scraper:

  def __init__(self):
    pass

  def scrape_instagram(self, username, password, target_username, additional = False, user_emailID = None):
    try:
    
      # Scrape Instagram - Image URLS, Video / Reel Thumbnail URLS, Captions and Additional Informations
      
      scraper = InstagramScraper(username, password, target_username)
      
      scraper.scrape_instagram(additional)
      
      # Data Cleaning and Transformation
      
      data_processor = InstagramDataProcessor()
      
      output_path = data_processor.data_post_processing(IMAGE_URL_JSON_PATH, CAPTION_JSON_PATH, target_username)
      
      # Downloading the .JSON File to Local System
      
      downloader = Downloader()
      downloader.download_json_from_vscode(output_path)
      
      # Sending the .JSON File via Email
      if user_emailID is not None:
        EmailSender().send_email(user_emailID, username, output_path)
    
    except Exception as e:
      
      print(f"Error occurred: {e}")
      
    else:
      
      # Deleting the Middleware Folder as it contains Raw Data which are also Reduntant
      
      if os.path.exists(MIDDLEWARE):
        shutil.rmtree(MIDDLEWARE)
      
      print("Process completed") 

# User Input

if __name__ == "__main__":
  
  username = "de.clairmont"
  password = "Ourdemocracy@99"
  target_username = "filippzorz"
  additional = True
  user_emailID = "subhraturning@gmail.com"
  
  scrape_instagram = Scraper()
  scrape_instagram.scrape_instagram(username, password, target_username, additional) 
  