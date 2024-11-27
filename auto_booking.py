"""
Module for Globish Booking Bot.

This module provides functionality to automate the booking of classes on the Globish platform.
It includes methods to load ignored class IDs, check the validity of the token, 
retrieve available classes, and book classes.

Classes:
    GlobishBookingBot: A bot for booking classes on Globish.
"""

import os
import time
import logging
import dotenv
from curl_cffi import requests
from utils.slack import SlackMessenger

# Load environment variables from .env file
dotenv.load_dotenv(override=True)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('globish_booking_bot.log'),
                        logging.StreamHandler()
                    ])

class GlobishBookingBot:
    """
    A bot for booking classes on the Globish platform.

    This class provides methods to load ignored class IDs, check the validity of the token,
    retrieve available classes, and book classes.

    Attributes:
        workshop_class_url (str): URL for fetching workshop classes.
        masterclass_url (str): URL for fetching masterclass classes.
        book_class_url (str): URL for booking a class.
        token (str): Authorization token for API requests.
        headers (dict): Headers for API requests.
        ignored_ids (set): Set of ignored class IDs.
        time_delay (int): Time delay between requests.
    """
    def __init__(self):
        """Initialize the bot with URLs and headers."""
        logging.info("Initializing Globish Booking Bot...")
        self.workshop_class_url = 'https://api-student.globish.co.th/Student/Booking/GroupClass?type=workshop&campaign=workshop&language=en'
        self.masterclass_url = 'https://api-student.globish.co.th/Student/Booking/GroupClass?type=master-class&campaign=master-class&language=en'
        self.book_class_url = 'https://api-student.globish.co.th/Student/Booking/GroupClass/'
        self.messenger = SlackMessenger(token=os.getenv('GB_BOT_SLACK_TOKEN'), channel=os.getenv('GB_BOT_SLACK_CHANNEL'))
        self.headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'access-control-allow-origin': '*',
            'authorization': f'Bearer {os.getenv('GB_BOT_TOKEN')}',
            'origin': 'https://app.globish.co.th',
            'priority': 'u=1, i',
            'referer': 'https://app.globish.co.th/',
            'sec-ch-ua': '"Google Chrome";v="123", "Chromium";v="123", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'x-lang': 'en',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.ignored_ids = self.load_ignored_ids()
        self.time_delay = 5
        self.check_previous_crash()
        self.check_token()
        logging.info("Globish Booking Bot initialized.")


    def load_ignored_ids(self):
        """Load ignored class IDs from a file."""
        try:
            with open('ignored_ids.txt', 'r', encoding='utf-8') as file:
                ignored_ids = {line.strip() for line in file}
                logging.debug("Ignored Class IDs: %s", ignored_ids)
                return ignored_ids
        except FileNotFoundError:
            logging.warning("ignored_ids.txt file not found. No Class IDs will be ignored.")
            return set()

    def check_previous_crash(self):
        """Check if the bot crashed during the last run."""
        if os.path.exists('.crash.flag'):
            self.messenger.send_message("Bot crashed during the last run. Please check the logs.")
            logging.error("Bot crashed during the last run, stopping execution.")
            raise SystemExit("Bot crashed during the last run, stopping execution.")

    def generate_crash_flag(self):
        """Generate a crash flag file."""
        with open('.crash.flag', 'w', encoding='utf-8'):
            pass
        logging.info("Crash flag file generated.")

    def check_token(self):
        """Check if the token is valid."""
        response = requests.get(self.workshop_class_url, headers=self.headers, timeout=10, impersonate="chrome123")
        if response.status_code == 401:
            logging.error("Invalid token. Please check your GB_BOT_TOKEN in the .env file.")
            self.messenger.send_message("Invalid token. Please check your GB_BOT_TOKEN in the .env file.")
            self.generate_crash_flag()
            raise ValueError("Invalid token. Please check your GB_BOT_TOKEN in the .env file.")
        if response.status_code == 404:
            logging.error("404 Client Error: Not Found - Impersonation failed.")
            self.messenger.send_message("404 Client Error: Not Found - Impersonation failed.")
            self.generate_crash_flag()
            raise ConnectionRefusedError("404 Client Error: Not Found - Impersonation failed.")
        response.raise_for_status()
        time.sleep(self.time_delay)

    def add_ignored_id(self, class_id):
        """Add a class ID to the ignored list."""
        self.ignored_ids.add(class_id)
        with open('ignored_ids.txt', 'a', encoding='utf-8') as file:
            file.write(f"{class_id}\n")
        logging.info("Added class ID to ignored list: %s", class_id)

    def get_classes(self, url):
        """Get classes from the given URL."""
        response = requests.get(url, headers=self.headers, timeout=10, impersonate="chrome123")
        response.raise_for_status()
        time.sleep(self.time_delay)
        return response.json()['data']['classes']

    def book_class(self, class_id, class_topic):
        """Book a class given its ID and topic."""
        response = requests.post(f"{self.book_class_url}{class_id}", headers=self.headers, timeout=10, impersonate="chrome123")
        response_dict = response.json()
        if response_dict['statusCode'] == 201:
            logging.info("Booked class: #[%s] %s", class_id, class_topic)
        else:
            self.messenger.send_message(f"Failed to book class, adding to the ignored list: #[{class_id}] {class_topic}\n```{response_dict}```")
            logging.error("Failed to book class, adding to the ignored list: #[%s] %s\n%s", class_id, class_topic, response_dict)
            self.add_ignored_id(str(class_id))
        time.sleep(self.time_delay)

    def book_available_classes(self, url):
        """Book available classes from the given URL."""
        classes = self.get_classes(url)
        for class_ in classes:
            if not class_['booked'] and str(class_['id']) not in self.ignored_ids:
                logging.debug("Available class: #[%s] %s", class_['id'], class_['topic'])
                self.book_class(class_['id'], class_['topic'])

    def book_workshop(self):
        """Book available Workshop classes."""
        logging.info("Finding available Workshop classes...")
        self.book_available_classes(self.workshop_class_url)

    def book_masterclass(self):
        """Book available Master Class classes."""
        logging.info("Finding available Master Class classes...")
        self.book_available_classes(self.masterclass_url)

if __name__ == "__main__":
    bot = GlobishBookingBot()
    bot.book_workshop()
    bot.book_masterclass()
