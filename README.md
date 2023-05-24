## TelecomsXChange Carrier Relations Automation Script

This Python script automates the process of searching for and purchasing voice routes using the TelecomsXChange API. It replaces a typically manual, time-consuming process with a streamlined, efficient approach.

### Features

- 🔍 Automated Searching: Utilizing TelecomsXChange's Market View API, the script automatically searches for the best routes based on price and quality.
- ⚙️ Automated Purchasing: Once optimal routes are identified, the script uses the Interconnect API to establish connections with these routes.
- 📈 Detailed Logging: All actions and responses are logged in real-time, allowing for easy tracking, debugging, and analysis.

### Prerequisites

- Python 3.6+
- requests library
- TCXC API Login and Key 


### Usage

To run the script:

```shell
python3 automate_cr.py
```

The script will search for voice routes, purchase the optimal ones, and log the details.

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


Please note: this script is intended for illustrative purposes and should be used responsibly. Ensure you have necessary permissions and understand the TelecomsXChange API usage terms and conditions.
