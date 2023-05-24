# Copyright (c) 2023 Ameed Jamous - TelecomsXChange.com
# This script is also compatiable with NeuTrafix Market Place API

import requests
from requests.auth import HTTPDigestAuth
import logging

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

# Start message
logger.info('🚀 TelecomsXChange (TCXC) Carrier Relations Automation Script started')

# Your Telecomsxchange Buyer username and password
username = '{Enter API login}'
password = '{Enter API key}'

# TCXC API endpoints
search_url = 'https://apiv2.telecomsxchange.com/marketview/search'
interconnect_url = 'https://apiv2.telecomsxchange.com/buyers/interconnect'

# NeuTrafix API endpoints
# search_url = 'https://apiv2.neutrafix.telin.net/marketview/search'
# interconnect_url = 'https://apiv2.neutrafix.telin.net/buyers/interconnect'

# Headers for the requests
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Data for the search API request
search_data = {
    'prefix': '22797', # Replace with the dial code you're targeting
    'searchform': '1',
    'type': 'ANY',
    'pager': '100',
    'off': '0',
}

# Make the POST request for search
logger.info('🔍 Searching TCXC market view API for Niger Mobile (Dial Code: +22797) ...\n')
search_response = requests.post(search_url, headers=headers, data=search_data,
                                auth=HTTPDigestAuth(username, password))

# Check if the search request was successful
if search_response.status_code == 200:
    try:
        search_info = search_response.json()
        if search_info.get('status') == 'success':
            rates = search_info.get('rates')
            logger.info('✅ Found some routes \n')

            # Interconnect process
            logger.info('⚙️ Running Interconnection and Provisioning process. Please wait...\n')
            for rate in rates:
                price_1 = float(rate.get('price_1', '0'))
                i_connection = rate.get('i_connection')

                # If the price_1 is below 0.19, interconnect
                logger.info('🔍 Interconnect with carriers that match target rates of 0.22 or lower \n')
                if price_1 < 0.22:
                    logging.info(f"Attempting to interconnect with i_connection: {i_connection}")
                    
                    # Data for the interconnect API request
                    interconnect_data = {
                        'add': '1',
                        'i_account': '{ENTER I_account}',
                        'agree': 'yes',
                        'id': str(i_connection)
                    }

                    # Make the POST request for interconnect
                    interconnect_response = requests.post(interconnect_url, headers=headers, 
                                                          data=interconnect_data,
                                                          auth=HTTPDigestAuth(username, password))

                    # Print the status code and the response text for debugging purposes
                    logging.info(f"Interconnect Response Status Code: {interconnect_response.status_code}")
                    logging.info(f"Interconnect Response Text: {interconnect_response.text}")

                    # Check if the interconnect request was successful
                    if interconnect_response.status_code == 200:
                        try:
                            interconnect_info = interconnect_response.json()
                            if interconnect_info.get('status') == 'success':
                             logging.info(f"Successfully interconnect with i_connection: {i_connection}. "
                                 f"Details: {interconnect_info}. All details have also been emailed to relevant departments in your organization.")

                            else:
                                logging.error(f"Interconnect request returned an error for i_connection: {i_connection}. "
                                              f"Details: {interconnect_info}")
                        except ValueError:
                            logging.error("Error decoding the interconnect response as JSON")
                    else:
                        logging.error(f"Interconnect request failed for i_connection: {i_connection}")
                else:
                    logging.info(f"Price too high for i_connection: {i_connection}. Skipping interconnect.")
        else:
            logging.error("Search request returned an error. Details: %s", search_info)
    except ValueError:
        logging.error("Error decoding the search response as JSON")
else:
    logging.error("Search request failed")
