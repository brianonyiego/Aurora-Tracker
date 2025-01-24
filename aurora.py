# Aurora Tracker
# Script to monitor the Kp index from NOAA data and send a notification if Northern Lights are likely visible.

import requests
from datetime import datetime, timedelta
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Constants
NOAA_URL = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"  # NOAA data source
KP_THRESHOLD = 5  # Kp index threshold for visible auroras
CHECK_TIME = "20:30"  # Daily check time (24-hour format)
PSEUDO_EMAIL = "northernlights.notify@gmail.com"  # Pseudo-email for sending notifications

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function: Fetch NOAA data
def fetch_noaa_data(url):
    """
    Fetch the latest aurora forecast data from NOAA.
    
    Args:
        url (str): URL to the NOAA data source.
    
    Returns:
        str: Raw data as a string if successful, None otherwise.
    """
    try:
        logging.info("Fetching NOAA data...")
        response = requests.get(url)
        response.raise_for_status()
        logging.info("NOAA data fetched successfully.")
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching NOAA data: {e}")
        return None

# Function: Parse Kp indices
def parse_kp_indices(data):
    """
    Extract Kp indices from the NOAA data.
    
    Args:
        data (str): Raw data fetched from NOAA.
    
    Returns:
        dict: Dictionary with dates as keys and lists of Kp values as values.
    """
    logging.info("Parsing Kp indices from NOAA data...")
    kp_indices = {}
    lines = data.split("\n")

    try:
        for i, line in enumerate(lines):
            if line.startswith("Kp Index"):  # Identify the Kp Index section
                forecast_lines = lines[i + 1: i + 4]  # The next 3 lines contain the forecast
                for forecast in forecast_lines:
                    parts = forecast.split()
                    if len(parts) >= 9:
                        date = parts[0]
                        kp_values = [float(value) for value in parts[1:]]
                        kp_indices[date] = kp_values
        logging.info("Kp indices parsed successfully.")
    except Exception as e:
        logging.error(f"Error parsing Kp indices: {e}")

    return kp_indices

# Function: Check aurora visibility conditions
def check_conditions(kp_indices):
    """
    Identify dates with favorable Kp index values for aurora visibility.
    
    Args:
        kp_indices (dict): Dictionary of dates and corresponding Kp values.
    
    Returns:
        list: Dates with Kp values above the threshold.
    """
    logging.info("Checking for favorable aurora conditions...")
    favorable_dates = [
        date for date, kp_values in kp_indices.items()
        if any(kp >= KP_THRESHOLD for kp in kp_values)
    ]
    return favorable_dates

# Function: Send notification via pseudo-email
def send_notification(dates):
    """
    Send a notification with favorable aurora viewing dates via pseudo-email.
    
    Args:
        dates (list): List of favorable dates for aurora viewing.
    """
    recipient_email = "user@example.com"  # Replace with the intended recipient's email
    subject = "Northern Lights Notification"

    if dates:
        body = f"The Northern Lights are likely visible on the following dates: {', '.join(dates)}."
    else:
        body = "No favorable aurora viewing conditions detected in the forecast."

    try:
        # Set up email
        msg = MIMEMultipart()
        msg['From'] = PSEUDO_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Simulate sending email (pseudo-email setup, no actual email server)
        logging.info("Sending notification...")
        logging.info(f"To: {recipient_email}\nSubject: {subject}\nBody: {body}")
    except Exception as e:
        logging.error(f"Error sending notification: {e}")

# Function: Calculate seconds until next check
def get_seconds_until_next_check(check_time_str):
    """
    Calculate the number of seconds until the next scheduled check time.
    
    Args:
        check_time_str (str): Scheduled check time in HH:MM format.
    
    Returns:
        float: Seconds until the next check.
    """
    now = datetime.now()
    check_time = datetime.strptime(check_time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    if now > check_time:
        check_time += timedelta(days=1)
    return (check_time - now).total_seconds()

# Main function
def main():
    """
    Main function to orchestrate the aurora tracking script.
    """
    logging.info("Aurora Tracker started.")

    while True:
        seconds_until_check = get_seconds_until_next_check(CHECK_TIME)
        logging.info(f"Next check scheduled in {seconds_until_check / 60:.2f} minutes.")
        time.sleep(seconds_until_check)

        logging.info("Checking NOAA data for aurora forecast...")
        data = fetch_noaa_data(NOAA_URL)
        if data:
            kp_indices = parse_kp_indices(data)
            favorable_dates = check_conditions(kp_indices)
            send_notification(favorable_dates)
        else:
            logging.error("Failed to fetch NOAA data. Skipping this check.")

if __name__ == "__main__":
    main()
