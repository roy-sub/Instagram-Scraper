import os
import time
import json
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from constants import MIDDLEWARE, PROXY, ACCOUNT_INFO_FOLDER_PATH

# Change the permissions of the chromedriver which allows the owner to execute the file and allows 
# others to read and execute it.

os.chmod('/home/subhrastien/driver/chromedriver',0o755) 

class InstagramScraper:
    def __init__(self, username, password, target_username):
        self.username = username
        self.password = password
        self.target_username = target_username
        self.driver = self.setup_driver()

    # Set up WebDriver with proxy options
    
    def setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        
        # Important : Add Resedential Proxy
        # chrome_options.add_argument('proxy.soax.com'.format(PROXY))
        
        return webdriver.Chrome('/home/subhrastien/driver/chromedriver', options=chrome_options)

    # Log in to Instagram
    
    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        
        username_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Log in']")))
        
        time.sleep(5)
        username_input.clear()
        username_input.send_keys(self.username)
        
        time.sleep(5)
        password_input.clear()
        password_input.send_keys(self.password)
        
        time.sleep(5)
        login_button.click()
        time.sleep(30)

    # Scraping the Required Data from Instagram
    
    def scrape_instagram(self, additional):
        try:
            self.login()
            self.driver.get(f"https://www.instagram.com/{self.target_username}")
            
            # Scrape Account Info if "additional" is True
            
            if additional:
                time.sleep(15)
                details = self.driver.find_elements(By.CSS_SELECTOR, "span._ac2a._ac2b")
                
                time.sleep(15)
                element = self.driver.find_element_by_css_selector(".x7a106z.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xdt5ytf.x2lah0s.xdj266r.x11i5rnm.xwonja6.x1dyjupv.x1onnzdu.xwrz0qm.xgmu61r.x1nbz2ho.xbjc6do")
                
                all_text = element.text
                elements = all_text.split('\n')

                acc_info = {
                    "number_of_post": details[0].text,
                    "number_of_followers": details[1].text,
                    "number_of_followings": details[2].text,
                    "bio": elements
                }

                acc_data = json.dumps(acc_info, indent=4)
                
                if not os.path.exists(ACCOUNT_INFO_FOLDER_PATH):
                    os.makedirs(ACCOUNT_INFO_FOLDER_PATH)
                            
                path = f"{ACCOUNT_INFO_FOLDER_PATH}/{self.target_username}.json"

                with open(path, 'w') as f:
                    f.write(acc_data)
            
            # Scrape Image URL, Video / Reel Thumnail URL and their Corresponding Captions
            
            time.sleep(15)
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            image_dict = {}
            caption_dict = {}
            counter = 1

            # Scroll to load more images
            
            while len(image_dict) < 150:
                
                time.sleep(5)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                time.sleep(5)
                images = self.driver.find_elements_by_tag_name('img')
                
                time.sleep(5)
                caption_elements = self.driver.find_elements_by_class_name("_aagv")

                # Extract image source and caption
                
                for image, caption_element in zip(images, caption_elements):
                    
                    src = image.get_attribute('src')
                    
                    caption = caption_element.find_element(By.TAG_NAME, "img").get_attribute("alt")

                    # Add to dictionary if not duplicate and source is not None
                    
                    if src not in image_dict.values() and src is not None: 
                        
                        image_dict[counter] = src
                        caption_dict[counter] = caption
                        counter += 1

                        if len(image_dict) == 150:
                            break

                time.sleep(5)
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height or len(image_dict) == 150:
                    break

                last_height = new_height

            # Saving the Scraped Data
            
            if not os.path.exists(MIDDLEWARE):
                os.makedirs(MIDDLEWARE)

            with open(f"{MIDDLEWARE}/image_url.json", 'w') as f:
                json.dump(image_dict, f)

            with open(f"{MIDDLEWARE}/caption.json", 'w') as f:
                json.dump(caption_dict, f)

            time.sleep(30)
            self.driver.quit()

        except Exception as e:
            print(f"Exception : {e}")
