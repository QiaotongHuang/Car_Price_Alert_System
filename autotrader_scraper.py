import json
import time
import random
import logging 
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    filename='project.log',  # Log file
    filemode='a',                # Append mode
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO           # Log level
)
logger = logging.getLogger(__name__)  # Create logger instance

# Set up Selenium options
def create_driver():
    """Create and return a Selenium WebDriver instance with options."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_page(driver, url):
    try:
        driver.get(url)
        # Random wait between 5 and 10 seconds
        time.sleep(random.uniform(5, 10))
        
        # Wait for the listings to be loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "result-item-inner"))
        )
        
        # Scroll down the page to load all content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        listings = soup.find_all('div', class_='result-item-inner')
        
        cars = []
        for listing in listings:
            car = {}
            
            title = listing.find('span', class_='result-title')
            if title:
                car['title'] = title.text.strip()
            
            price = listing.find('span', class_='price-amount')
            if price:
                car['price'] = price.text.strip()
            
            location = listing.find('span', class_='proximity-text')
            if location:
                car['location'] = location.text.strip()
            
            mileage = listing.find('span', class_='odometer-proximity')
            if mileage:
                car['mileage'] = mileage.text.strip()
            
            dealer = listing.find('div', class_='seller-name')
            if dealer:
                car['dealer'] = dealer.text.strip()
            
            img = listing.find('img', class_='photo-image')
            if img and 'src' in img.attrs:
                car['image_url'] = img['src']

            detail = listing.find('p', class_ = 'details used')
            if detail:
                car['detail'] = detail.text.strip()

            price_delta_elem = listing.find('p', id=lambda x: x and x.endswith('_DeltaPrice'))
            logger.info(f"Price delta element found: {price_delta_elem is not None}")
            if price_delta_elem:
                logger.info(f"Price delta text: {price_delta_elem.text}")
                car['price_delta'] = price_delta_elem.text.strip()
            else:
                logger.info("No price delta element found")
                car['price_delta'] = None  

            link_element = listing.find('a', class_='inner-link')
            if link_element and 'href' in link_element.attrs:
                base_url = "https://www.autotrader.ca"  
                car['link_url'] = base_url + link_element['href'].split('?')[0]

            cars.append(car)
        
        return cars
    
    except TimeoutException:
        logger.error(f"Timeout waiting for listings on {url}")
        return []
    except NoSuchElementException:
        logger.error(f"Could not find expected elements on {url}")
        return []
    except Exception as e:
        logger.error(f"An error occurred while scraping {url}: {e}")
        return []
    

def scrape_autotrader(num_pages=1):    
    all_cars = []
    base_url = 'https://www.autotrader.ca/suv/'
    driver = create_driver()
    
    try:
        for page in range(1, num_pages + 1):
            # url = f"{base_url}?rcp=15&rcs=0&srt=9&prx=-1&prv=Ontario&loc=L4M%204Y8&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch&pg={page}"
            url = f"https://www.autotrader.ca/cars/on/rcp=100&rcs=0&srt=9&pRng=%2C30000&prx=-2&prv=Ontario&loc=M5V%202G7&body=SUV&hprc=True&wcp=True&inMarket=advancedSearch&pg={page}"
            logger.info(f"Scraping page {page}: {url}")
            
            cars = scrape_page(driver, url)
            all_cars.extend(cars)
            
            logger.info(f"Found {len(cars)} cars on page {page}")
            
            # Random wait between 5 and 15 seconds between pages
            time.sleep(random.uniform(5, 15))
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    
    finally:
        driver.quit()
    
    return all_cars


def get_car_specifications(driver, url):
    try:
        driver.get(url)
        # Random wait between 5 and 10 seconds
        time.sleep(random.uniform(10, 15))
                
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # Find all list items (li) under the ul with id "sl-card-body"
        list_items = soup.find('ul', id='sl-card-body').find_all('li')

        # Extract the data into a dictionary
        car_specs = {'url': url}
        for item in list_items:
            key = item.find('span', id=lambda x: x and x.startswith('spec-key')).text
            value = item.find('span', id=lambda x: x and x.startswith('spec-value')).strong.text
            car_specs[key] = value

        for key, value in car_specs.items():
            logger.info(f"{key}: {value}")
        return car_specs
    
    except Exception as e:
        logger.error(f"An error occurred while scraping {url}: {e}")
        return []
    

def scrape_car_spec(df):
    driver = create_driver()
    url_list = df['link_url'].tolist()
  
    car_spec = []
    for url in url_list:
        try:
                spec = get_car_specifications(driver, url)
                car_spec.append(spec)
                # Random wait between 10 and 18 seconds between pages
                time.sleep(random.uniform(10, 18))
                break  # remove this line to scrape all cars
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    driver.quit()
    
    return car_spec

if __name__ == '__main__':
    # Scrape 10 pages
    car_data = scrape_autotrader(num_pages=10)
    logger.info(f"Total cars found: {len(car_data)}")

    # Get current date and time to append to filenames
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save to JSON file with date-time appended
    json_filename = f'autotrader_data_{current_time}.json'
    try:
        with open('autotrader_data.json', 'w') as f:
            json.dump(car_data, f, indent=2)
        logger.info(f"Data saved to {json_filename}")
    except Exception as e:
        logger.error(f"Failed to save data to JSON: {e}")

    # Save to CSV file with date-time appended
    csv_filename = f'autotrader_data_{current_time}.csv'
    try:
        df = pd.DataFrame(car_data)
        df.to_csv('autotrader_data.csv', index=False)
        logger.info(f"Data saved to {csv_filename}")
    except Exception as e:
        logger.error(f"Failed to save data to CSV: {e}")

    # Scrape car specifications
    scrape_car_spec(df)