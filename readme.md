# Mantle Parser

## Requirements

This application requires Python 3.12 and the Python packages in requirements.txt

```
pip install -r requirements.txt
```

Mantle API keys are also required, please add your keys to `.env`
```
API_KEYS=key1,key2,key3
```

## Structure
  - main.py: This is the main script that runs the application.
  - provider.py: Provides onchain data from mantle API.
  - extracter.py: Extracts target data from onchain data.
  - utilities.py: This script contains utility functions used by the other scripts.
  - test.py: This script contains unit tests for the application.

## How to run
```
python main.py
```
Stdout will log the progress like:

`ic| f'Queue size: {cls._qsize()}, Future size: {cls._fsize()}, Pause: {cls._pause}': 'Queue size: 3873, Future size: 32, Pause: 0.1'`

Constant decrement in Queue size is a sign of working properly.

Upon successful execution, the number of unique and new wallet addresses will be shown.

The result will be in addresses.json with the format `{address: new_wallet_boolean}`.

## Test
```
python -m unittest
```