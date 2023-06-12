"""
Script Name: Telecomsxchange Routing Strategies Automation
Version: 1.0
Last Modified: 2023-06-12
Author: Ameed Jamous

Description:
This script automates the process of analyzing routing strategies based on least cost using Telecomsxchange/NeutrafiX buyer credentials.
It fetches the rates from Telecomsxchange/NeutrafiX API, performs various analyses, and uses OpenAI API to suggest an optimal routing strategy.
The API endpoints, credentials, and other configurations can be adjusted within the script.

Credentials, API endpoints, and other configurations can be adjusted in the respective sections of the 
script.
"""

import requests
import os
from requests.auth import HTTPDigestAuth
import logging
from collections import Counter
import numpy as np
import openai

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Log to file
file_handler = logging.FileHandler('automate_cr.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)



# OpenAI API credentials
openai.api_key = os.environ.get('OPENAI_API_KEY')

if openai.api_key is None:
    raise ValueError('Please set the OPENAI_API_KEY environment variable.')

# Start message
logger.info('🚀 TelecomsXChange (TCXC) Routing Strategies Automation Script started')

# Telecomsxchange Buyer Credentials
username = os.environ.get('TCXC_USERNAME')
password = os.environ.get('TCXC_PASSWORD')

if username is None or password is None:
    raise ValueError('Please set the TCXC_USERNAME and TCXC_PASSWORD environment variables.')

# TCXC API endpoints
search_url = 'https://apiv2.telecomsxchange.com/marketview/search'

# Neutrafix API endpoints
# search_url = 'https://apiv2.neutrafix.telin.net/marketview/search'

# Headers for the requests
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Data for the search API request
search_data = {
    'prefix': '2279',  # Replace with the dial code you're targeting
    'searchform': '1',
    'seller': '',
    'type': 'CLI',  # Trunk Type - you can pass string values {cli, nocli, tdm, any}
    'pager': '100',
    'off': '0',
}

# Make the POST request for search
logger.info(f'🔍 Searching TCXC market view API for Dial Code: +{search_data["prefix"]} ...\n')
search_response = requests.post(search_url, headers=headers, data=search_data,
                                auth=HTTPDigestAuth(username, password))

# Check if the search request was successful
if search_response.status_code == 200:
    try:
        search_info = search_response.json()
        if search_info.get('status') == 'success':
            rates = search_info.get('rates')
            logger.info('✅ Found some routes \n')

            if rates:
                # Sort the rates from lowest to highest to form the routing strategy
                sorted_rates = sorted(rates, key=lambda rate: float(rate.get('price_1', '0')))

                # Print out the routing strategy
                logger.info('📋 Routing Strategy based on Least Cost: \n')
                for i, rate in enumerate(sorted_rates, start=1):
                    logger.info(
                        f"Route {i}: Vendor = {rate.get('vendor_name')}, Connection = {rate.get('connection_name')}, Price = {rate.get('price_1')}")

                # Generate a paragraph summary of the rates
                rates_summary = "\n".join(
                    f"Route {i}: Vendor = {rate.get('vendor_name')}, Connection = {rate.get('connection_name')}, Price = {rate.get('price_1')}"
                    for i, rate in enumerate(sorted_rates, start=1)
                )

                # Generate a prompt for OpenAI API
                prompt = f"Based on the analysis of the current rates from Telecomsxchange, please suggest an optimal routing strategy:\n\n{rates_summary}"

                # Call OpenAI API to generate the routing strategy suggestion
                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=prompt,
                    max_tokens=100,
                    n=1,
                    stop=None,
                    temperature=0.7
                )

                # Extract the generated suggestion from the OpenAI API response
                suggestion = response.choices[0].text.strip()

                # Print the generated routing strategy suggestion
                logger.info('\nRouting Strategy Suggestion:')
                logger.info(suggestion)

            else:
                logger.info('No rates available.')

        else:
            logging.error("Search request returned an error. Details: %s", search_info)
    except ValueError:
        logging.error("Error decoding the search response as JSON")
else:
    logging.error("Search request failed")
