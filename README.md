# Globish Booking Bot

This script automates the booking of classes on the Globish platform. It uses the Globish API to book available Workshops and Master Classes.

## Prerequisites

- Python 3
- `curl_cffi` library
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

4. Create a `.env` file in the root directory and add your Globish token and Slack credentials:

    ```env
    GB_BOT_TOKEN=your_globish_token_here
    GB_BOT_SLACK_TOKEN=your_slack_token_here
    GB_BOT_SLACK_CHANNEL=your_slack_channel_id_here
    ```

5. Create an `ignored_ids.txt` file in the root directory to specify class IDs that should be ignored during booking. Each line should contain one class ID. 
    > **Important Note:** Ensure there is always a blank line at the end of the `ignored_ids.txt` file, should you change this file manually.

## Usage

Run the script to start booking available Workshops and Master Classes:

```sh
python auto_booking.py
```

Alternatively, you can schedule the script to run periodically using crontab:
```sh
crontab -e
```
```
00-59/2 18 * * 2,4 /home/toppy/git/auto_run.sh  # This example runs the script every 2 minutes between 18:00 and 18:59 on Tuesdays and Thursdays.
```
For an example of the shell script used with crontab, please refer to `scripts/auto_run.sh.example`.

## Logging
The script logs its activity to `globish_booking_bot.log` and also outputs to the console.

## Troubleshooting

If the script encounters an issue and creates a `.crash.flag` file, you need to resolve the issue and then remove the `.crash.flag` file to allow the script to execute again: 

```sh
rm .crash.flag
```

> **Note:** The `.crash.flag` file is generated to prevent the script from repeatedly running and consuming API requests when invoked by crontab. Ensure that all issues are resolved before deleting this file.
