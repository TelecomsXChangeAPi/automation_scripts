"""
Automate SIP Trunk Testing on TelecomsXChange Platform
Copyright (c) 2023 TelecomsXChange. All rights reserved.

This script automates the process of testing SIP trunks on the TelecomsXChange/NeuTrafix platforms.
It fetches a list of all SIP providers, lets the user choose a provider for testing, 
fetches test numbers based on the user's selected country and network, and then initiates 
a test call to the chosen numbers through the selected provider.
"""

import requests
from requests.auth import HTTPDigestAuth
import getpass
import inquirer
import tabulate
import re

# Your TCXC credentials
username = input("Please enter your username: ")
password = getpass.getpass("


from tabulate import tabulate
import requests
from requests.auth import HTTPDigestAuth
import getpass

# TCXC Base API URL
base_url = "https://apiv2.telecomsxchange.com"
                           
# NeuTrafix (NTX) Base API URL
# base_url = "https://apiv2.neutrafix.telin.net"

# API endpoints
sellers_list_endpoint = "/sellers/list"
get_numbers_endpoint = "/buyers/tools/getnumbers"
route_test_endpoint = "/buyers/routetest"

# TCXC/NTX API Credentials
username = ''
password = ''


# Getting sellers list
sellers_list_response = requests.post(
    base_url + sellers_list_endpoint,
    data={"pager": 300, "off": 0},
    auth=HTTPDigestAuth(username, password))


sellers_list = sellers_list_response.json()['routes']

# Displaying the sellers' list as a table
print("📋 Here is the list of available sellers with their i_connections and routes:")
headers = ["Seller Name", "i_Connection", "Route Name"]
table = [[seller['seller_name'], seller['i_connection'], seller['route_name']] for seller in sellers_list]
print(tabulate(table, headers, tablefmt="pretty"))

# User input for i_connection
i_connection = input("💼 Please select the i_connection of the seller you'd like to test the call through: ")

# Validate user input
while not i_connection.isnumeric():
    print("🔴 Error: Invalid input. Please enter a numeric value.")
    i_connection = input("💼 Please select the i_connection of the seller you'd like to test the call through: ")

# Getting test numbers
country = input("🌍 Please enter the country you'd like to fetch the test number from: ")
description = input("📄 Please enter the network (description) you'd like to fetch the test number from: ")

get_numbers_response = requests.get(
    base_url + get_numbers_endpoint,
    params={"country": country, "description": description},
    auth=HTTPDigestAuth(username, password))

numbers = get_numbers_response.json()['cdrs']

# Displaying the numbers' list as a table
print("📋 Here is the list of available test numbers:")
headers = ["Number", "Description", "Country"]
table = [[number['CLD'], number['description'], number['country_name']] for number in numbers]
print(tabulate(table, headers, tablefmt="pretty"))

# User input for cld1 and cld2
cld1 = input("🎯 Please enter the test number for the first leg of the call (cld1): ")
cld2 = input("🎯 Please enter the test number for the second leg of the call (cld2): ")

# User input for i_account
i_account = input("🔑 Please enter your i_account value which can be found in TCXC portal under account settings: ")

# Validate user input
while not i_account.isnumeric():
    print("🔴 Error: Invalid input. Please enter a numeric value.")
    i_account = input("🔑 Please enter your i_account value which can be found in TCXC portal under account settings: ")

# User input for cli1 and cli2
cli1 = input("📞 Please enter the caller id to be shown for the first leg of the call (cli1): ")
cli2 = input("📞 Please enter the caller id to be shown for the second leg of the call (cli2): ")

# Validate user input
while not cli1.isnumeric() or not cli2.isnumeric():
    print("🔴 Error: Invalid input. Please enter numeric values.")
    cli1 = input("📞 Please enter the caller id to be shown for the first leg of the call (cli1): ")
    cli2 = input("📞 Please enter the caller id to be shown for the second leg of the call (cli2): ")

# Initiate the test call
initiate_test_data = {
    "i_account": i_account,
    "cld1": cld1,
    "cli1": cli1,
    "i_connection1": i_connection,
    "cld2": cld2,
    "cli2": cli2,
    "i_connection2": i_connection
}

initiate_test_response = requests.post(
    base_url + route_test_endpoint,
    data=initiate_test_data,
    auth=HTTPDigestAuth(username, password))

print("📞 " + initiate_test_response.json()['status_text'])
