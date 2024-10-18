# Car Listings Price Alert System
## Project Description
This project is an automated price alert system designed to gather car listings from a website. It allows users to specify search criteria such as car model, price range, and year. The system automatically retrieves and filters the listings based on these criteria and sends email notifications with the relevant results.

## Features
Retrieve car listings based on specific search parameters.
Filter listings according to user-defined preferences.
Schedule price checks at regular intervals.
Send email notifications with filtered listings.
Secure authentication using Google API for sending emails.

## Setup and Installation
### Prerequisites
Before you begin, ensure you have the following:
Python 3.x installed.
Google Chrome (used by Selenium for checking the website).

### Installation Steps
1. Clone the Repository

Clone this repository to your local machine:
```bash
git clone <repository_url>
cd car_listings_price_alert_system
```

2. Install Python Dependencies

Install the required Python libraries using pip by running the following command: 
```bash
pip install -r requirements.txt
```

3. Set Up Environment Variables

Copy the .env.example file and rename it to .env. 
```bash
cp .env.example .env
```
4. Google API Setup for Email Notifications

To enable email notifications, you'll need to configure the Gmail API. Create a Google Cloud project, enable Gmail API, and download the credentials.json file. Place this file in the project directory.

## Usage
### Running the Price Alert System
1. Customize Search Criteria

Update the search criteria for retrieving car listings by modifying the parameters in the autotrader_scraper.py file to suit your needs (such as car model, price range, etc.).

2. Start the Price Alert System

To run the system, execute the main.py file: 
```python
python main.py
```
This will initiate the price alert system, filter the car listings based on your criteria, and send an email with the results.

### Scheduling Price Checks
The system is set to check prices on a schedule using the schedule library. You can modify the scheduling interval in the main.py file by updating the following line:
```python
schedule.every().day.at("08:00").do(run_price_alert_system)
```
This line schedules the price alert system to run every day at 8:00 AM. You can change this to meet your preferred schedule.

# License
This project is licensed under the MIT License.
