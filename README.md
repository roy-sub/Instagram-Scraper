# Instagram-Scraper

This **Instagram Scraper** allows you to extract a wealth of information from Instagram profiles with just three inputs: **your Instagram username**, **your password**, and the **target username**. With this scraper, you can gather the following information :

* Image post URLs
* Video URLs
* Thumbnail URLs
* Captions
* Number of Followers
* Number of Following
* Number of Posts
* Actual Name
* Bio
* Website Link

This README provides a step-by-step explanation of the entire code base, enabling you to understand the inner functionality and quickly and easily scrape the desired information from **Public Instagram Profiles**. In addition to a detailed **Set Up** guide with tutorial and resources linked.

# Step-by-step Explanation of the Entire Code Base

## Step I

```

def scrape_instagram(self, username, password, target_username, additional = False, user_emailID = None):
    
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

```

This code base is structured into four key sections, as outlined in the comments: data scraping, data cleaning, data downloading and email notification. The scraper allows for the extraction of various data points from Instagram profiles, such as image post URLs, video URLs, thumbnail URLs, captions, follower counts, following counts, post counts, actual names, bios, and website links. 

Notably, two parameters, "additional" and "user_emailID," are optional. The "additional" parameter serves as a flag to control the scraping of extra data, a measure implemented to avoid detection by Instagram. Furthermore, the email notification feature will only be activated if the "email_ID" parameter is provided.

## Step II

```

def setup_driver(self):
    chrome_options = webdriver.ChromeOptions()
    
    # Important : Add Resedential Proxy
    chrome_options.add_argument('proxy.soax.com'.format(PROXY))
    
    return webdriver.Chrome('/home/subhrastien/driver/chromedriver', options=chrome_options)

```

```
PROXY = "proxy.soax.com:9000"

```
The instantiation of the WebDriver with a residential proxy is a pivotal step in mitigating detection by Instagram. However, in the current codebase, this line is commented out. This is due to the nature of residential proxies, which are tied to individual machine IP addresses, necessitating the creation of a custom residential proxy and its addition to the constants.py file. Detailed instructions on creating a Residential Proxy will be provided at the conclusion of this documentation.

```

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

```
The above script first check's the "additional" flag and if `True` scrape all the account information including follower counts, following counts, post counts, actual names, bios, and website links. Followed by saving them inside the `account_info` folder with the name - `f"{target_username}.json"`. Once done then we move on to scraping mage post URLs, video URLs, thumbnail URLs and captions using the below script and save them inside the `middleware` folder raw, that will need further transformation -

```

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

```

Following the preceding step, all necessary data has been scraped in its raw form and saved within the middleware and account_info folders under the filename f"{target_username}.json". The subsequent step involves transforming the data.

## Step III

```

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
    
    output_path = f'{RESULT_FOLDER_PATH}/{username}.json'

    with open(output_path, 'w') as outfile:
        json.dump(combined_json, outfile, indent=4)

    return output_path

```

The provided code snippet reads the raw data stored within the middleware folder and transforms it into a single JSON file named f"{target_username}" inside the result folder. The resulting JSON file is structured as follows:

```
{
    "image_url": "https://scontent.cdninstagram.com/v/t39.30808-6/439901859_18428791516014992_6292753477573328006_n.jpg?stp=dst-jpg_e15&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xNDQweDE2OTIuc2RyLmYzMDgwOCJ9&_nc_ht=scontent.cdninstagram.com&_nc_cat=108&_nc_ohc=57BbVV3sEK4Ab7xUmU4&edm=APs17CUAAAAA&ccb=7-5&ig_cache_key=MzM1NDEyOTc4MTczMTY4MDAxNA%3D%3D.2-ccb7-5&oh=00_AfDprjbjv_DfbPu9POjVEhkYgclKPj3vXp0iuKwa1P_hhA&oe=6631CC32&_nc_sid=10d13b",
    "caption": "a good day !!"
 }

```

## Step III

```
class Downloader:
  def __init__(self):
      self.save_path = os.path.expanduser('~')  # Root folder path

  def download_json_from_vscode(self, json_file_path):
      filename = json_file_path.split('/')[-1] # Extract filename from the provided path
      try:
          shutil.copyfile(json_file_path, os.path.join(self.save_path, filename)) # Copy the JSON file to the root folder
      except Exception as e:
          print(f"Failed to copy JSON file. Error: {e}") # Handle any exceptions that occur during copying

```

Since the codebase will already be set up on your local machine for Instagram scraping, you can easily download the .JSON file from your IDE's user interface. Alternatively, the provided code snippet can perform the same action for you, copying the file and moving it to the root directory of your machine, which is essentially the same as downloading any file to your root directory.

## Step IV

```
def send_email(self, receiver_address, user_name, attachment_path):
    
  # Compose email subject and content
  subject = f"Greetings {user_name}, your Data is Ready to be Downloaded"
  content_text = f"Hi {user_name}, we are excited to inform you that the data you requested has been successfully scraped and is now ready for your use.\n\nYou can download the data from the attachment provided with this email."
  
  # Extract filename from attachment path
  file_name = attachment_path.split('/')[-1].split('.')[0]
  
  # Create EmailMessage object
  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = self.email_address
  msg['To'] = receiver_address
  msg.set_content(content_text)
  
  # Add attachment to the email
  with open(attachment_path, 'rb') as f:
    file_data = f.read()
  msg.add_attachment(file_data,
                     maintype='text',
                     subtype='plain',
                     filename=attachment_path.split('/')[-1])
  
  # Send the email using SMTP server
  with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
    server.starttls()
    server.login(self.email_address, self.email_password)
    server.send_message(msg)

```

The provided code snippet executes a specific action when `user_emailID is not None`, indicating the email ID to which the email will be sent. It also requires updating the `EMAIL_ADDRESS` and `PASSWORD` in the `constant.py` file with the `email ID you want to send the email from`. However, it's important to note a few key points before utilizing this step. To use this feature, you need to provide additional credentials, including a `PASSWORD`, which can be a bit tricky to obtain as it differs from your `general email password`.

Therefore, it is advisable to use this step only when you intend to `develop a full-fledged application`, as it is well-written, customizable, and free. However, for your current use case, it may be too time-consuming and cumbersome, as you would still need to navigate to your email and download the file from there, whereas you can directly download it from the IDE and have it saved in your root folder automatically, as per the code flow.

![Alt Text](https://github.com/roy-sub/Instagram-Scraper/blob/main/Images/notification_email%20.png)

# Set Up Guide 

The setup process can be divided into four parts :

* Installing `Selenium` and other necessary packages and setting up the `Chrome WebDriver`.
* Updating the WebDriver paths : This step involves updating the WebDriver paths in the code in one or two places.
* Setting up `Residential Proxy` : Configuring and integrating a residential proxy into your setup.
* Setting `source_emailID` and `PASSWORD` : Providing the email ID and password for sending notifications via email. *( optional )*

## Selenium and Webdriver

To install `selenium` and all other dependencies you can refer to the `requirements.txt` file and simple run `pip install -r requirements.txt` where the `requirements.txt` contains -

```

certifi==2024.2.2
charset-normalizer==2.0.12
idna==3.7
packaging==21.3
Pillow==8.4.0
pyparsing==3.0.7
python-dotenv==0.20.0
requests==2.27.1
selenium==3.141.0
urllib3==1.26.18
webdriver-manager==3.7.1

```

* Please note that I am using `Python version 3.6.5`. In case you encounter any `dependency conflicts`, you can switch to a different Python version using `pyenv` or another method of your choice. If you decide to use `pyenv`, you can refer to my [blog](https://medium.com/@subhrastien/how-to-install-multiple-python-versions-on-a-single-computer-and-use-them-with-vscode-3bc0f0aa5ac7) for instructions on how to install multiple Python versions on a single computer and use them with VSCode. However, it is unlikely that you will encounter any issues.

* In addition to the steps outlined here for setting up `Selenium`, you can refer to this concise [tutorial](https://www.youtube.com/watch?v=RBpZ_kUTlqM&t=300s) which I found helpful. It allowed me to completely the setup both `Selenium` and `Webdriver` within a few minutes in a single session. Please be aware that the tutorial is based on a `Linux Debian machine`, so the steps may vary slightly for your system. However, the core concepts remain the same. I recommend watching the video at `1.5x` speed before proceeding with setting up the WebDriver.

* In the tutorial, you'll see that a folder named `hugo` is created to store the `WebDriver`. In our case, this folder will be named `Instagram Scraper`, which is the same folder where all the scripts are located. Even if you don't follow the above video, it's recommended to keep the `WebDriver` in the same folder and `update the paths accordingly`.

## Updating the WebDriver paths

After completing the `installation` and setting up the `WebDriver` on your local system, open the `scrape_insta_profile.py` file and update the specified lines with the `path to the WebDriver` on your machine.

```

os.chmod('/home/subhrastien/driver/chromedriver',0o755)
.
.
.
return webdriver.Chrome('/home/subhrastien/driver/chromedriver', options=chrome_options)

```

## Resedential Proxy -

* Setting up a **Residential Proxy** is a straightforward process. Simply visit the [Soax Official Website](https://soax.com/) and subscribe to one of their residential proxy plans. The recommended plan is the **Residential 15**, priced at around `$99 per month`. However, they also offer a `3-day trial for $1.99`, which is both affordable and adequate for scraping the necessary data.

* After subscribing to the plan, access the [dashboard](https://dashboard.soax.com/proxy). And then `Whitelist your system's IP address`, which you will use for scraping Instagram. Next, copy the credentials, which will be something like `proxy.soax.com:9000` from the dashboard itself, and update the `PROXY` variable in the `constants.py` file with these credentials.

## Email Password ( optional )-

To generate the password required for sending emails using an `SMTP server`, you can refer to this [video](https://www.youtube.com/watch?v=Sddnn6dpqk0&t=121s) at a suggested speed of `1.5X`.

## Scrape Instagram

Finally once you have completed all the aforementioned steps, you are ready to begin scraping Instagram. To do this, navigate to `app.py`, provide all the `necessary inputs` and run `python3 app.py in the terminal`.

```

# User Input

if __name__ == "__main__":
  
  username = ""
  password = ""
  target_username = ""
  additional = 
  user_emailID = ""
  
  scrape_instagram = Scraper()
  scrape_instagram.scrape_instagram(username, password, target_username, additional)

```

# Conclusion

In conclusion, this Instagram Scraper provides a comprehensive solution for extracting valuable information from Instagram profiles. With just a few inputs, you can gather image URLs, video URLs, captions, follower counts, following counts, post counts, actual names, bios, and website links. The scraper is easy to set up and use, with detailed instructions provided in this README.

The code base is structured into four key sections: data scraping, data cleaning, data downloading, and email notification. Optional features such as using a residential proxy and sending email notifications add flexibility and customization to the scraper.

To get started, follow the step-by-step guide provided in this README to set up the scraper on your local machine. If you encounter any issues or have any questions, feel free to reach out to me on [LinkedIn](https://www.linkedin.com/in/subhradip-roy/), [Twitter](https://twitter.com/iam_roysubhra), or via [Email](subhrastien@gmail.com).

