"""
TelecomsXChange Trouble Ticket Automation Script 

Copyright (c) 2023 Ameed Jamous - TelecomsXChange.com

This script automates the process of monitoring and reporting call failures 
in a telecom network. It retrieves call history data from the TCXC 
API, filters out failed calls based on specified disconnect reasons, and sends 
a formal and professional trouble ticket to the vendor through the TelecomsXChange 
messaging API. 

This tool aids telecom service providers in automating the identification and escalation process for calls with low Quality of Service (QoS). 
By directly raising trouble tickets with the carrier responsible for terminating the call, 
service providers can efficiently manage and enhance their network performance.

"""

import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime, timedelta
import os
import random
import string

# Function to generate random ticket ID
def get_random_ticket_id(length):
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Functions to handle sent messages
def check_if_message_sent(call_id, destination_number, vendor_id):
    message_id = f'{call_id}-{destination_number}-{vendor_id}'
    if not os.path.exists('sent_messages.txt'):
        return False
    with open('sent_messages.txt', 'r') as f:
        for line in f.readlines():
            if line.strip() == message_id:
                return True
    return False

def record_message_sent(call_id, destination_number, vendor_id):
    message_id = f'{call_id}-{destination_number}-{vendor_id}'
    with open('sent_messages.txt', 'a') as f:
        f.write(message_id + '\n')

# Telecomsxchange Buyer Credentials
username = '{API Login}'
password = '{API key}'

# API Endpoints
call_history_url = 'https://apiv2.telecomsxchange.com/buyers/callhistory/'
message_send_url = 'https://apiv2.telecomsxchange.com/buyers/message/send'

# Headers for the requests
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Time settings for the call history API request
end_time = datetime.utcnow()
start_time = end_time - timedelta(minutes=30)

# Data for the call history API request
call_history_data = {
    'show': 'bad',
    'date_from': start_time.strftime('%Y-%m-%d %H:%M:%S'),
    'date_to': end_time.strftime('%Y-%m-%d %H:%M:%S'),
}

# Disconnect reasons to filter out
disconnect_reasons = ["Service or option not available", "unspecified", "timeout", "Internetworking, unspecified", "Bearer capability not authorized"]

# Send GET request for call history
call_history_response = requests.post(call_history_url, headers=headers, data=call_history_data,
                                      auth=HTTPDigestAuth(username, password))

# Check if the call history request was successful
if call_history_response.status_code == 200:
    try:
        call_history_info = call_history_response.json()
        if call_history_info.get('status') == 'success':
            cdrs = call_history_info.get('cdrs')
            for cdr in cdrs:
                disconnect_reason = cdr.get('disconnect_reason')
                if disconnect_reason in disconnect_reasons and not check_if_message_sent(cdr['call_id'], cdr['CLD'], cdr['i_vendor']):
                    message_data = {
                        'id': cdr['i_vendor'],
                        'subject': f"Trouble Ticket #{get_random_ticket_id(10)}: Call Failure to Destination: {cdr['CLD']}",
                        'message': f"Dear Vendor,\n\nWe are writing to inform you of a detected issue concerning the quality of service on your route {cdr['connection_name']}."
                                    f"Our monitoring systems have identified that the call to destination number {cdr['CLD']} has failed.\n\nError Details:\n- Disconnect Reason: {disconnect_reason}"
                                    f"\n- Timestamp of Occurrence: {cdr['connect_time']}\n\nWe request your immediate attention and action to resolve this issue as it is affecting our service delivery."
                                    f"We appreciate your prompt response and solution to this matter.\n\nThank you for your cooperation."
                    }
                    message_response = requests.post(message_send_url, headers=headers, data=message_data,
                                                      auth=HTTPDigestAuth(username, password))
                    record_message_sent(cdr['call_id'], cdr['CLD'], cdr['i_vendor'])
        else:
            print("Call history request returned an error. Details: ", call_history_info)
    except ValueError:
        print("Error decoding the call history response as JSON")
else:
    print("Call history request failed")
