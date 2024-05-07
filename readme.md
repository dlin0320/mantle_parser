# Mantle Parser

## Requirements

This application requires Python 3.12 and the Python packages listed in `requirements.txt`.

To install the required packages, run the following command:

```
pip install -r requirements.txt
```

Mantle API keys are also required. Please add your keys to the `.env` file as shown below, or refer to the [References](#references) section for more information.
```
API_KEYS=key1,key2,key3
```

## Structure

- `main.py`: This is the main script that runs the application.
- `provider.py`: This script provides on-chain data from the Mantle API.
- `extracter.py`: This script extracts target data from on-chain data.
- `utilities.py`: This script contains utility functions used by the other scripts.
- `test.py`: This script contains unit tests for the application.

## How to Run

To run the application, use the following command:

```
sudo python main.py
```

The progress will be logged to stdout:

`ic| progress: 'Queue size: 38, Future size: 22, Pause: 0.1'`

A constant decrement in the queue size is a sign that the application is working properly.

Upon successful execution, the number of unique and new wallet addresses will be displayed. 

`ic| report: 'Unique addresses: 931, New addresses: 900'`

The result will be saved in `addresses.json` in the format `{address: new_wallet_boolean}`.

## Testing

To run the unit tests, use the following command:

```
sudo python -m unittest
```

## References

- [Mantle Account API](https://docs.mantlescan.xyz/api-endpoints/accounts)
- [Mantle Blocks API](https://docs.mantlescan.xyz/api-endpoints/blocks#get-block-number-by-timestamp)
- [Mantle API Key](https://docs.mantlescan.xyz/getting-started/viewing-api-usage-statistics)