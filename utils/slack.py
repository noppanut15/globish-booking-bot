"""
This module provides a utility class for sending messages to a Slack channel using the Slack API.

Classes:
    SlackMessenger: A class to send messages to a specified Slack channel.

Usage example:
    messenger = SlackMessenger(token="your-slack-token", channel="your-channel-id")
    messenger.send_message("Hello, Slack!")
"""
import requests

class SlackMessenger:
    """
    A class to send messages to a Slack channel using the Slack API.
    """
    def __init__(self, token, channel):
        """
        Initializes the Slack client with the provided token and channel.
        Args:
            token (str): The authentication token for the Slack API.
            channel (str): The Slack channel ID where messages will be posted.
        """
        self.token = token
        self.channel = channel
        self.url = "https://slack.com/api/chat.postMessage"

    def send_message(self, text):
        """
        Sends a message to a Slack channel.
        Args:
            text (str): The message text to send.
        Raises:
            requests.exceptions.HTTPError: If the request to the Slack API fails.
        Returns:
            dict: The JSON response from the Slack API.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        payload = {
            "channel": self.channel,
            "text": text
        }
        response = requests.post(self.url, json=payload, headers=headers, timeout=10)
        response_json = response.json()
        if not response_json["ok"]:
            raise requests.exceptions.HTTPError(f"Request to Slack API failed with error `{response_json["error"]}`, response: {response.text}")
        return response_json
