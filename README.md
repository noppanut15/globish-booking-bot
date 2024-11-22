# Globish Booking Bot

This script automates the booking of classes on the Globish platform. It uses the Globish API to book available Workshops and Master Classes.

## Prerequisites

- Python 3
- `requests` library
- `python-dotenv` library

## Setup

1. Clone the repository and navigate to the project directory.

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Globish token:

    ```env
    GB_TOKEN=your_globish_token_here
    ```

5. Create an `ignored_ids.txt` file in the root directory to specify class IDs that should be ignored during booking. Each line should contain one class ID.

## Usage

Run the script to start booking available Workshops and Master Classes:

```sh
python auto-booking.py
```

## Logging
The script logs its activity to `globish_booking_bot.log` and also outputs to the console.