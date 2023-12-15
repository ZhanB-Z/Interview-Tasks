from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import os
import time
import random
from selenium_stealth import stealth

options = webdriver.ChromeOptions()
options.headless = False
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)


def random_delay(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def parse_ten_brands(driver):
    try:    
        driver.get("https://www.auto.ru")
        
        input("Hit Enter once done with manual checkups...")

        brands = driver.find_elements(By.CSS_SELECTOR, "div.IndexMarks__col a.IndexMarks__item")

        ten_brands = {}
        for brand in brands[:10]:
            name = brand.find_element(By.CSS_SELECTOR, "div.IndexMarks__item-name").text
            random_delay(1,2)
            link = brand.get_attribute('href')
            ten_brands[name] = link
        
        print(ten_brands)
        return ten_brands
    except Exception as e:
        print(f"Something went wrong: {e}")

def get_ad_links(driver, brand_page_link, max_ads=20):
    driver.get(brand_page_link)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ListingItem")))
    except TimeoutException:
        print(f"Timeout when loading brand: {brand_page_link}")
        return {}
    ad_elements = driver.find_elements(By.CSS_SELECTOR, "div.ListingItem__main")[:10]
    ad_links = {}
    
    for ad_element in ad_elements:
        ad_title_element = ad_element.find_element(By.CSS_SELECTOR, "a.ListingItemTitle__link")
        ad_title = ad_title_element.text
        ad_link = ad_element.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        ad_id = ad_link.split('/')[-2]
        ad_links[ad_id] = {"link": ad_link, "title": ad_title}

    print(ad_links)
    return ad_links

def get_photo_urls(driver, ad_link):
    driver.get(ad_link)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ImageGalleryDesktop__itemContainer")))
    except TimeoutException:
        print(f"Couldn't find ads for {ad_link}")
        return []

    photo_elements = driver.find_elements(By.CSS_SELECTOR, "img.ImageGalleryDesktop__image")[:5]
    photo_urls = []
    
    for photo_element in photo_elements:
        photo_url = photo_element.get_attribute('src')
        if not photo_url.startswith(('http:', 'https:')):
            photo_url = 'https:' + photo_url
        photo_urls.append(photo_url)
    
    # print(photo_urls)
    return photo_urls

def download_image(url, folder_path, filename):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    response = requests.get(url)

    if response.status_code == 200:
        with open(os.path.join(folder_path, filename), 'wb') as file:
            file.write(response.content)


if __name__ == "__main__":
    ten_brands = parse_ten_brands(driver)
    base_folder = "photos"
    required_ad_count = 10

    for brand, link in ten_brands.items():
        brand_folder = os.path.join(base_folder, brand.replace('/', '_'))
        print(f"Collecting ads for {brand}")
        ads = get_ad_links(driver, link, max_ads = 20)
    
        successful_ad_count = 0
        for ad_id, ad_data in ads.items():
            if successful_ad_count >= required_ad_count:
                break
            
            ad_folder = os.path.join(brand_folder, ad_data['title'].replace('/', '-'))
            print(f"Collecting photos from ad {ad_data['title']}")
            photo_urls = get_photo_urls(driver, ad_data["link"])

            if photo_urls:
                successful_ad_count += 1
                for photo_index, photo_url in enumerate(photo_urls):
                    filename = f"photo_{photo_index + 1}.jpg"
                    download_image(photo_url, ad_folder, filename)


    driver.quit()

    


# stealth(driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="MacIntel",
#         webgl_vendor="Google Inc. (Apple)",  # Ваш WebGL Vendor
#         renderer="ANGLE (Apple, Apple M1 Pro, OpenGL 4.1 Metal - 88)",  # Ваш WebGL Renderer
#         fix_hairline=True,
#         ) #will check webdriver stealth mode later

# import undetected_chromedriver as uc - didnt work, will check later
# options.add_argument('--user-data-dir=/Users/a970/Library/Application Support/Google/Chrome/Default')
# user_agent = "..." didn't help, will check later
# options.add_argument(user_agent)