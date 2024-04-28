import requests
import json
import os
import re
from PIL import Image
from io import BytesIO
from constants import RESULT_FOLDER_PATH, ACCOUNT_INFO_FOLDER_PATH

class InstagramDataProcessor:
    def __init__(self):
        pass

    # Convert surrogate pairs to emoji codepoint
    
    def convert_surrogate_to_emoji(self, match):
        high_surrogate = ord(match.group(1))
        low_surrogate = ord(match.group(2))
        codepoint = 0x10000 + ((high_surrogate & 0x3FF) << 10) + (low_surrogate & 0x3FF)
        return chr(codepoint)

    # Update JSON data with emoji conversion
    
    def update_json_data_with_emoji_conversion(self, json_path):
        with open(json_path, 'r') as file:
            data = json.load(file)
        
        updated_data = []
        
        for element in data:
            if "caption" in element and element["caption"].startswith("Photo shared by"):
                continue
            updated_data.append(element) 
        
        result = []

        for element in updated_data:
            if "caption" in element:
                caption = element["caption"]
                updated_caption = re.sub(r'([\ud800-\udbff])([\udc00-\udfff])', 
                                         self.convert_surrogate_to_emoji, 
                                         caption)
                result_element = {"image_url": element["image_url"], "caption": updated_caption}
                result.append(result_element)
                
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

    # Check if the link is a valid image URL
    
    def is_valid_image_link(self, link):
        return link.startswith('https')

    # Check if the image size is valid (width and height > 150)
    
    def is_post_image_size(self, link):
        try:
            response = requests.get(link)
            image = Image.open(BytesIO(response.content))
            width, height = image.size
            return width > 150 and height > 150
        except Exception as e:
            print(f"Error checking image size: {e}")
            return False

    # Filter out invalid image links and images with size < 150x150
    
    def filter_post_images(self, data):
        filtered_data = {}
        failed_data = {}
        counter = 1
        for key, value in data.items():
            if self.is_valid_image_link(value):
                if self.is_post_image_size(value):
                    filtered_data[counter] = value
                    counter += 1
                else:
                    failed_data[key] = value
            else:
                failed_data[key] = value
        return filtered_data, failed_data

    # Perform data transformation and save as JSON
    
    def data_transformation(self, image_url_json_path, caption_json_path, username):
        with open(caption_json_path, 'r', encoding='utf-8-sig') as file:
            captions = json.load(file)
        
        with open(image_url_json_path, 'r') as file:
            links = json.load(file)
        
        filtered_data, _ = self.filter_post_images(links)
        
        combined_json = []
        for key in filtered_data.keys():
            element = {
                'image_url': filtered_data.get(key, ''),
                'caption': captions.get(f"{key}")
            }
            combined_json.append(element)
        
        combined_json_str = json.dumps(combined_json, indent=4)
        
        if not os.path.exists(RESULT_FOLDER_PATH):
            os.makedirs(RESULT_FOLDER_PATH)
        
        output_path = f'{RESULT_FOLDER_PATH}/{username}.json'

        with open(output_path, 'w') as outfile:
            json.dump(combined_json, outfile, indent=4)

        return output_path 

    # Perform data post-processing
    
    def data_post_processing(self, image_url_json_path, caption_json_path, target_username):
        
        output_path = self.data_transformation(image_url_json_path, caption_json_path, target_username)
        
        self.update_json_data_with_emoji_conversion(output_path)
        
        return output_path 
