## TelecomsXChange Carrier Relations Automation Scripts

These Python scripts automate various tasks in the management of telecom services using the TelecomsXChange API. They replace typically manual, time-consuming processes with streamlined, efficient approaches.

### Few example scripts

1. **Automated Searching and Purchasing (automate_carrier_relations.py):** This script automates the process of searching for and purchasing voice routes.
    - Features
        - 🔍 Automated Searching: Utilizing TelecomsXChange's Market View API, the script automatically searches for the best routes based on price and quality.
        - ⚙️ Automated Purchasing: Once optimal routes are identified, the script uses the Interconnect API to establish connections with these routes.
        - 📈 Detailed Logging: All actions and responses are logged in real-time, allowing for easy tracking, debugging, and analysis.

2. **Automated Trouble Ticketing (automate_lowqos_tt.py):** This script automates the detection and escalation of low QoS calls to carriers responsible for terminating the calls.
    - Features
        - 🚫 Automated Call Quality Detection: The script checks the call history from the TelecomsXChange API and identifies calls with low quality based on certain disconnect reasons.
        - 📨 Automated Trouble Ticketing: The script sends a message to the respective vendor via the TelecomsXChange messaging API, automatically escalating the issue.
        - 🎟 Unique Trouble Ticket IDs: Each message sent has a unique ticket ID to differentiate between different issues.
        - ⏰ Real-time Operation: The script is designed to run in real time, checking the past 30 minutes for any low-quality calls.

3. **Automated Virtual Numbers Selling (automate_numbers_selling.py):** This script automates the process of selling DID numbers on TelecomsXChange platform, and then sends a message to the buyers informing them of the new numbers listed for sale.
    - Features
        - 📲 Automated Listing: The script lists new DID numbers on the TelecomsXChange platform for sale.
        - 📤 Automated Messaging: Once the DID numbers are listed, the script sends a message to all the buyers notifying them about the new numbers for sale.
        - 🎈 Detailed Logging: All actions and responses are logged in real-time, allowing for easy tracking, debugging, and analysis.

** Comparison Table Example **

| Task                                 | Automation Benefits                                     | Manual Work Challenges                                      |
|--------------------------------------|---------------------------------------------------------|-------------------------------------------------------------|
| Automated Searching and Purchasing   | - Faster search and identification of optimal routes     | - Time-consuming manual search                               |
|                                      | - Reduced human error in purchasing                      | - Higher chances of errors in purchasing                     |
|                                      | - Real-time logging for easy tracking and analysis       | - Manual logging and tracking can be cumbersome              |
| Automated Trouble Ticketing          | - Immediate detection and escalation of low QoS calls    | - Delayed detection and response to low QoS calls            |
|                                      | - Automated ticketing for efficient issue resolution     | - Manual ticket creation and escalation                      |
|                                      | - Unique ticket IDs for better issue tracking             | - Difficulty in tracking and organizing manual escalations    |
| Automated Virtual Numbers Selling    | - Efficient listing of new DID numbers for sale          | - Time-consuming manual listing                              |
|                                      | - Automated messaging to notify buyers                   | - Manual communication with each buyer individually          |
|                                      | - Real-time logging for easy tracking and analysis       | - Manual logging and tracking can be cumbersome              |
| Generate Ai Routing Strategies       | - Generates AI-based routing strategies from realtime voice, SMS market rates                 | - Manual creation of routing strategies can be complex       |
|                                      | - Consistent and optimized routing decisions              | - Limited optimization and scalability with manual approach  |
| Automate Routes Testing              | - Automated testing of route functionality               | - Time-consuming manual testing                              |
|                                      | - Rapid identification of route issues                    | - Manual identification of route issues can be challenging   |
|                                      | - Detailed logging for easy analysis and debugging        | - Manual logging and analysis can be time-consuming          |




### Prerequisites

- Python 3.6+
- requests library
- TCXC API Login and Key 

### Usage

To run the scripts:

```shell
python3 automate_carrier_relations.py
python3 automate_lowqos_tt.py
python3 automate_numbers_selling.py
python3 automate_did_buying.py
python3 generate_ai_routing_strategy.py
python3 automate_routes_testing.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please note: these scripts are intended for illustrative purposes and should be used responsibly. Ensure you have necessary permissions and understand the TelecomsXChange API usage terms and conditions.

