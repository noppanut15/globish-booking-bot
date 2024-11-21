import requests
import dotenv
import os
from pprint import pprint

# Load environment variables from .env file
dotenv.load_dotenv()

workshop_list_url = 'https://api-student.globish.co.th/Student/Booking/GroupClass?type=workshop&campaign=workshop&language=en'
masterclass_list_url = 'https://api-student.globish.co.th/Student/Booking/GroupClass?type=master-class&campaign=master-class&language=en'

book_class_url = 'https://api-student.globish.co.th/Student/Booking/GroupClass/'

# Get the token from the .env file
token = os.getenv('GB_TOKEN') 

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'access-control-allow-origin': '*',
    'authorization': f'Bearer {token}',
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

# response = requests.get(workshop_list_url, headers=headers)
response = requests.get(masterclass_list_url, headers=headers)

response_dict = response.json()
classes = response_dict['data']['classes']

for class_ in classes:
    if class_['booked']:
        continue
    
    response = requests.post(f"{book_class_url}{class_['id']}", headers=headers)
    response_dict = response.json()
    if response_dict['statusCode'] == 201:
        print(f"Booked class: {class_['topic']}")
        print(f"ID: {class_['id']}")
    else:
        # TODO: Add error handling (notify user)
        print(f"Failed to book class: {class_['topic']}")
        pprint(response_dict)
        
    print("-" * 50)
