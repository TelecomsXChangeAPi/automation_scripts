#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Automate Selling DID numbers on TelecomsXChange Platform
    Copyright (c) 2023 TelecomsXChange. All rights reserved.

    This script automates the process of selling DID numbers on TelecomsXChange platform,
    and then sends a message to the subscribed buyers informing them of the new numbers listed for sale.
"""

from requests.auth import HTTPDigestAuth
import requests
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO, filename='did_log.log', filemode='w', format='%(asctime)s - %(message)s')

# TelecomsXChange API Credentials
username = "{API Login}"
password = "{API Key}"

# List of numbers to sell
did_numbers = ["19542405440", "19542405441", "19542405442", "19542405443"]

# This will be used to store the messages for each number
did_messages = []

# Iterate through each number
for number in did_numbers:
    # API endpoint
    url = "https://apiv2.telecomsxchange.com/sellers/did/add"

    # Data to be sent to API
    did_data = {
        'number': number,
        'price_1': "0.02",
        'interval_1': "60",
        'monthly_fee': "10",
        'setup_fee': "10.00",
        'did_type': "mobile",
        'voice': "1",
        'sms': "1",
        'smpp_price': "0.01",
        'capacity': "5",
        'status': "idle",
        'parent': 'international'
    }

    # Send the request
    response = requests.post(url, data=did_data, auth=HTTPDigestAuth(username, password))

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        if 'status' in result and result['status'] == 'success':
            logging.info(f"DID Number {did_data['number']} was successfully listed for sale. 🎉")
            if did_data['status'] != 'blocked':
                # Add the did data to the messages list
                did_messages.append(did_data)
        else:
            logging.error(f"There was an error listing the DID Number {did_data['number']} for sale. Response: {response.content} 😕")
    else:
        logging.error(f"There was an error processing the request. Response: {response.content} 😕")

# If there are any messages, send them to the buyers
if did_messages:
    # Send message to buyers about new DID number
    buyers_url = "https://apiv2.telecomsxchange.com/sellers/buyers/list"
    buyers_response = requests.post(buyers_url, auth=HTTPDigestAuth(username, password))

    if buyers_response.status_code == 200:
        buyers = buyers_response.json()['buyers']
        for buyer in buyers:
            message_send_url = "https://apiv2.telecomsxchange.com/sellers/message/send"
            message_text = "Dear " + buyer['login'] + ",\n\nWe have recently listed new DID numbers on the marketplace for sale. Here are the details:\n\n"
            for did in did_messages:
                message_text += f"Number: {did['number']}\nPrice: {did['price_1']}\nInterval: {did['interval_1']}\nMonthly Fee: {did['monthly_fee']}\nSetup Fee: {did['setup_fee']}\nDID Type: {did['did_type']}\nVoice: {did['voice']}\nSMS: {did['sms']}\nSMPP Price: {did['smpp_price']}\nCapacity: {did['capacity']}\nStatus: {did['status']}\n\n"
            message_text += "Best Regards,\n"

            message_data = {
                'id': buyer['i_customer'],
                'subject': "New DID Numbers Listed for sale",
                'message': message_text
            }

            message_response = requests.post(message_send_url, data=message_data, auth=HTTPDigestAuth(username, password))

            if message_response.status_code == 200:
                message_result = message_response.json()
                if 'status' in message_result and message_result['status'] == 'success':
                    logging.info(f"Message {message_result['i_message']} was successfully sent to buyer {buyer['login']}. 🎉")
                else:
                    logging.error(f"Failed to send message to buyer {buyer['login']}. Response: {message_response.content} 😕")
            else:
                logging.error(f"There was an error processing the request. Response: {message_response.content} 😕")
