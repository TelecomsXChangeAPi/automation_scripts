"""
TelecomsXChange Trouble Ticket Automation Script 

Copyright (c) 2023 YOUR NAME OR COMPANY NAME

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
import random
import string

# Your TCXC Buyer username (aka API login) and API Key
username = '{API Login}'
password = '{API Key}'

# API endpoints
call_history_url = 'https://apiv2.telecomsxchange.com/buyers/callhistory/'
message_send_url = 'https://apiv2.telecomsxchange.com/buyers/message/send'

# Headers for the requests
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Calculate the current time and the time 30 minutes ago
current_time = datetime.utcnow()
time_30_min_ago = current_time - timedelta(minutes=3600)

# Convert the times to the required string format
date_to = current_time.strftime('%Y-%m-%d %H:%M:%S')
date_from = time_30_min_ago.strftime('%Y-%m-%d %H:%M:%S')

# Data for the call history API request
call_history_data = {
    'show':'bad',
    'date_from': date_from,
    'date_to': date_to,
}

# Create a list of disconnect reasons that you are interested in
disconnect_reasons_to_filter = [
    "Service or option not available", 
    "unspecified", 
    "timeout", 
    "Internetworking, unspecified",
    "Bearer capability not authorized"
]

# Make the GET request for call history
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
                
                # Only process the cdrs with the specified disconnect reasons
                if disconnect_reason in disconnect_reasons_to_filter:
                    print(json.dumps(cdr, indent=4))
                    
                    # Extract vendor id from the cdr
                    i_vendor = cdr.get('i_vendor')

               # Generate a random ticket number
                    ticket_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

                # Compose the message to be sent
                    message_data = {
                        'id': str(i_vendor),
                        'subject': f"Trouble Ticket #{ticket_number}: Call Failure to Destination: {cdr.get('CLD')}",
                        'message': f"Dear Vendor,\n\n"
                                f"We are writing to inform you of a detected issue concerning the quality of service on your route {cdr.get('connection_name')}. Our monitoring systems have identified that the call to destination number {cdr.get('CLD')} has failed.\n\n"
                                f"Error Details:\n"
                                f"- Disconnect Reason: {disconnect_reason}\n"
                                f"- Timestamp of Occurrence: {cdr.get('connect_time')} UTC \n\n"
                                f"We request your immediate attention and action to resolve this issue as it is affecting our service delivery. We appreciate your prompt response and solution to this matter.\n\n"
                                f"Thank you for your cooperation."
                    }


                    # Send the message
                    message_response = requests.post(message_send_url, headers=headers, data=message_data,
                                                     auth=HTTPDigestAuth(username, password))

                    # Check if the message was sent successfully
                    if message_response.status_code == 200:
                        print("Message sent successfully to vendor: ", i_vendor)
                    else:
                        print("Failed to send message to vendor: ", i_vendor)
        else:
            print("Call history request returned an error. Details: ", call_history_info)
    except ValueError:
        print("Error decoding the call history response as JSON")
else:
    print("Call history request failed")
