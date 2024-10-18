# Car Listings Price Alert System
## Project Description
This project is an automated price alert system designed to gather car listings from a website. It allows users to specify search criteria such as car model, price range, and year. The system automatically retrieves and filters the listings based on these criteria and sends email notifications with the relevant results.

## Features
- Retrieve car listings based on specific search parameters.
- Filter listings according to user-defined preferences.
- Schedule price checks at regular intervals.
- Send email notifications using Gmail API.
- Log system activities (e.g., email sent, errors) for better traceability.

## Setup and Installation
### Prerequisites
Before you begin, ensure you have the following:
- Python 3.x installed.
- Google Chrome (used by Selenium for checking the website).
- A Google account to enable the Gmail API for sending emails.

### Installation Steps
**1. Clone the Repository**

Clone this repository to your local machine:
```bash
git clone <repository_url>
cd car_listings_price_alert_system
```

**2. Install Python Dependencies**

Install the required Python libraries using pip by running the following command: 
```bash
pip install -r requirements.txt
```

**3. Set Up Environment Variables**

Copy the .env.example file and rename it to .env. Update the file. 
```bash
cp .env.example .env
```
**4. Google API Setup for Email Notifications**

To enable email notifications, you'll need to configure the Gmail API. Follow these steps:

- Create a Google Cloud project.
- Enable the Gmail API.
- Download the credentials.json file from the Google API Console.
- Place this file in the project directory.
- On the first run, the script will authenticate with Google and generate a token.json file that will be used to store your authentication tokens for future use.

**5. Logging Setup**

The system logs all email-sending activities and errors to a file named project.log. Ensure this file is writable in the directory to capture logs.

## Usage
### Running the Price Alert System
**1. Customize Search Criteria**

Update the search criteria for retrieving car listings by modifying the parameters in the autotrader_scraper.py file to suit your needs (such as car model, price range, etc.).

**2. Start the Price Alert System**

To run the system, execute the main.py file: 
```python
python main.py
```
This will authenticate the user with Gmail (if not already authenticated) and start the price alert system. The system will scrape car listings, filter them based on the criteria, and send an email with the matching listings to the specified address.

**3. Scheduled Price Checks**

The script is set to run at scheduled intervals using the schedule library. You can adjust the frequency of the price checks in the main.py file by modifying the scheduling interval.
```python
schedule.every().day.at("08:00").do(run_price_alert_system)
```
This line schedules the price alert system to run every day at 8:00 AM.

# License
This project is licensed under the MIT License.
