# app/sms_service.py

import requests
import logging

logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self):
        self.url = 'your_API_url'
        self.api_key = 'your_API_KEY'  # Your API key

    def send_sms(self, phone, message):
        try:
            response = requests.post(self.url, data={
                'msisdn': phone,
                'message': message,
                'key': self.api_key
            }, verify=False)  # Disable SSL verification for the request
            
            response.raise_for_status()  # Raise an error for bad responses
            logger.info("SMS sent successfully: %s", response.text)
            return response.text
        except requests.RequestException as e:
            logger.error("Failed to send SMS: %s", e)
            return None
