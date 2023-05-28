## TelecomsXChange Carrier Relations Automation Scripts

These Python scripts automate various tasks in the management of telecom services using the TelecomsXChange API. They replace typically manual, time-consuming processes with streamlined, efficient approaches.

### Scripts

1. **Automated Searching and Purchasing (Automate_CarrierRelations.py):** This script automates the process of searching for and purchasing voice routes.

    - Features
        - 🔍 Automated Searching: Utilizing TelecomsXChange's Market View API, the script automatically searches for the best routes based on price and quality.
        - ⚙️ Automated Purchasing: Once optimal routes are identified, the script uses the Interconnect API to establish connections with these routes.
        - 📈 Detailed Logging: All actions and responses are logged in real-time, allowing for easy tracking, debugging, and analysis.

2. **Automated Trouble Ticketing (Automate_LowQoS_TT.py):** This script automates the detection and escalation of low QoS calls to carriers responsible for terminating the calls.

    - Features
        - 🚫 Automated Call Quality Detection: The script checks the call history from the TelecomsXChange API and identifies calls with low quality based on certain disconnect reasons.
        - 📨 Automated Trouble Ticketing: The script sends a message to the respective vendor via the TelecomsXChange messaging API, automatically escalating the issue.
        - 🎟 Unique Trouble Ticket IDs: Each message sent has a unique ticket ID to differentiate between different issues.
        - ⏰ Real-time Operation: The script is designed to run in real time, checking the past 30 minutes for any low-quality calls.

### Prerequisites

- Python 3.6+
- requests library
- TCXC API Login and Key 

### Usage

To run the scripts:

```shell
python3 Automate_CarrierRelations.py
python3 Automate_LowQoS_TT.py
```

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


Please note: this script is intended for illustrative purposes and should be used responsibly. Ensure you have necessary permissions and understand the TelecomsXChange API usage terms and conditions.
