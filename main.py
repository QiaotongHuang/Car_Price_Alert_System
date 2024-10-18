import os
import schedule
import time
import re
import json
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import autotrader_scraper as crawler  
import send_email as email  
import logging  

# Configure logging
logging.basicConfig(
    filename='project.log',          # Log file to write to
    filemode='a',                    # Append mode
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO               # Set logging level to INFO
)

# Create logger instance
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Email configuration
recipient_email = os.getenv("RECIPIENT_EMAIL")
subject = "Autotrader Data"

# Your function to scrape the website and send email
def scrape_and_send_email():
    try:
        logger.info("Starting the scraping process...")
        car_data = crawler.scrape_autotrader(num_pages=10)
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

        # Filter cars that are $5,000 or more below market price
        def extract_below_market_value(price_delta_str):
            if not price_delta_str:
                logger.info("Empty or None price_delta string provided.")
                return 0

            # Removing non-digit characters but keeping digits and commas for thousands separators
            corrected_str = price_delta_str.replace('$', '').replace(',', '')
            logger.info(f"Corrected string: {corrected_str}")

            # Extracting the first group of digits that may include commas
            match = re.search(r'([\d,]+)', corrected_str)
            if match:
                numeric_value = match.group(1) # Remove commas before conversion
                try:
                    return int(numeric_value)
                except ValueError as e:
                    logger.error(f"Failed to convert extracted value to int: {numeric_value}")
                    return 0
            else:
                logger.info("No numeric value found in the string.")
                return 0


        df['price_delta_clean'] = df['price_delta'].apply(extract_below_market_value)
        filtered_cars = df[df['price_delta_clean'] >= 3000]
        logger.info(f"Total cars below market price: {len(filtered_cars)}")

        # Send the email
        creds = email.authenticate_gmail()
        # Create the email body with car details
        body = "Here are the cars that are $3,000 or more below market price:\n\n"
        for index, car in filtered_cars.iterrows():
            body += f"Title: {car['title']}\n"
            body += f"Price: {car['price']}\n"
            body += f"Price Below Market: {car['price_delta']}\n"
            body += f"Location: {car['location']}\n"
            body += f"Mileage: {car['mileage']}\n"
            body += f"Dealer: {car['dealer']}\n"
            body += f"URL: {car['link_url']}\n\n"
        email.send_email(
            creds,
            recipient_email, 
            subject, 
            body
        )
        logger.info(f"Email sent successfully to {recipient_email}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")


# Schedule the job to run daily
schedule.every().day.at("17:00").do(scrape_and_send_email)

# Keep the script running to check the schedule
if __name__ == "__main__":
    logger.info("Scheduled scraping and email sending started...")

    while True:
        schedule.run_pending()
        time.sleep(60) 
    # scrape_and_send_email()  # Uncomment this line to run the function once