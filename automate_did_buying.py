#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Automate Buying DID numbers on TelecomsXChange Platform
    Copyright (c) 2023 TelecomsXChange. All rights reserved.

    This script automates the process of buying DID numbers on TelecomsXChange platform.
    It first makes a call to the 'market' API to get a list of available numbers. Then 
    it extracts each number from the returned list and checks if the 'monthly_fee' and 'setup_fee' 
    are below 2.00. If the conditions are met, the script makes a call to the 'purchase' 
    API to purchase that number. If the conditions are not met, the script skips that number 
    and moves on to the next one. 
"""

import requests
from requests.auth import HTTPDigestAuth
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    handlers=[logging.FileHandler("automate_buying.log"), 
                              logging.StreamHandler(sys.stdout)])
logger = logging.getLogger()

# TelecomsXChange API Credentials
username = "{Buyer Username}"
password = "{API Key}"

# API endpoint
search_url = "https://apiv2.telecomsxchange.com/number/market"

# Data to be sent to API
search_data = {
    'prefix': "1954240", # Replace with your desired number prefix
    'country': "",
    'description': "",
    'seller': "", # Filter by seller name if necessary. For e.g. Nexmo
    'voice': "1",
    'sms': "1",
    'fax': "0",
    'video': "0",
    'did_type': "any",
    'pager': "10",
    'off': "1"
}

# Send the request
search_response = requests.post(search_url, data=search_data, auth=HTTPDigestAuth(username, password))

# Check if the request was successful
if search_response.status_code == 200:
    dids = search_response.json().get('dids', [])
    for did in dids:
        # Check if the monthly_fee and setup_fee are below 2.00
        if float(did.get('monthly_fee', 0)) < 2.00 and float(did.get('setup_fee', 0)) < 2.00: # Setup Target rate for number you want to purchase. if higher than set value will be skipped. 
            # Purchase the number
            purchase_url = "https://apiv2.telecomsxchange.com/number/purchase"
            purchase_data = {
                'i_did': did['i_did'],
                'billing_i_account': "{Enter here}", # Enter Billing Account ID 
                'contact': f"sip:{did['number']}@sip01.telecomsxchange.com:5060",  # Configure SIP route
                'smpp_contact': f"smpp:did:did:{did['number']}@smpp01.telecomsxchange.com:2776" # Configure SMS/SMPP Route
            }

            # Send the request
            purchase_response = requests.post(purchase_url, data=purchase_data, auth=HTTPDigestAuth(username, password))

            # Check if the request was successful and purchase was confirmed
            if purchase_response.status_code == 200 and purchase_response.json().get('status') == 'success':
                logger.info(f"🟢 Successfully purchased number: {did['number']}")
                break
            else:
                logger.warning(f"⚠️ Failed to purchase number: {did['number']}. Reason: {purchase_response.json().get('message')}. Trying the next number.")
        else:
            logger.info(f"⚠️ Skipped number: {did['number']} due to high cost. Trying the next number.")
    else:
        logger.error("🔴 Failed to purchase any number: No available numbers, they are too costly, or all attempts failed.")
