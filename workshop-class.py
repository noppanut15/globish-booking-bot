import requests
import dotenv
import os
import logging
from pprint import pprint

# Load environment variables from .env file
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('globish_booking_bot.log'),
                        logging.StreamHandler()
                    ])

class GlobishBookingBot:
    def __init__(self):
        self.workshop_class_url = 'https://api-student.globish.co.th/Student/Booking/GroupClass?type=workshop&campaign=workshop&language=en'
        self.masterclass_url = 'https://api-student.globish.co.th/Student/Booking/GroupClass?type=master-class&campaign=master-class&language=en'
        self.book_class_url = 'https://api-student.globish.co.th/Student/Booking/GroupClass/'
        self.token = os.getenv('GB_TOKEN')
        self.headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'access-control-allow-origin': '*',
            'authorization': f'Bearer {self.token}',
            'origin': 'https://app.globish.co.th',
            'priority': 'u=1, i',
            'referer': 'https://app.globish.co.th/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'x-lang': 'en',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.check_token()
        logging.info("Globish Booking Bot initialized.")


    def check_token(self):
        response = requests.get(self.workshop_class_url, headers=self.headers)
        if response.status_code == 401:
            logging.error("Invalid token. Please check your GB_TOKEN in the .env file.")
            raise ValueError("Invalid token. Please check your GB_TOKEN in the .env file.")
        response.raise_for_status()


    def get_classes(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['data']['classes']

    def book_class(self, class_id, class_topic):
        response = requests.post(f"{self.book_class_url}{class_id}", headers=self.headers)
        response_dict = response.json()
        if response_dict['statusCode'] == 201:
            logging.info(f"Booked class: [#{class_id}] {class_topic}")
        else:
            # TODO: Add error handling (notify user)
            logging.error(f"Failed to book class: [#{class_id}] {class_topic}\n{response_dict}")

    def book_available_classes(self, url):
        classes = self.get_classes(url)
        for class_ in classes:
            if not class_['booked']:
                self.book_class(class_['id'], class_['topic'])

    def book_workshop(self):
        self.book_available_classes(self.workshop_class_url)
    
    def book_masterclass(self):
        self.book_available_classes(self.masterclass_url)

if __name__ == "__main__":
    bot = GlobishBookingBot()
    bot.book_masterclass()
    bot.book_workshop()
