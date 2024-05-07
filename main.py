from datetime import datetime, timezone
from utilities import date_to_timestamp
from extracter import Extracter
from provider import Provider
from icecream import ic
from constant import *
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--debug', '-D', action='store_true')
args = parser.parse_args()
debug = args.debug
if debug:
  ic.configureOutput(includeContext=True)

if __name__ == '__main__':
  Extracter.addresses(SMART)
  Extracter.addresses(FRENS)
  start_time = date_to_timestamp(datetime(2024, 3, 22, 7, 0, 0, tzinfo=timezone.utc))
  end_time = date_to_timestamp(datetime(2024, 4, 21, 23, 59, 59, tzinfo=timezone.utc))
  new_wallet_time = date_to_timestamp(datetime(2024, 3, 22, 0, 0, 0, tzinfo=timezone.utc))
  start = time.time()

  (
    Provider
      .init()
      .print('Setting range...')
      .set_range(start_time, end_time)
      .print(f'Start block: {Provider.start_block}, End block: {Provider.end_block}')
      .print('Getting transactions...')
      .get_txn_in_range(Extracter.addresses())
      .print('Setting range...')
      .set_range(GENESIS_TIMESTAMP, new_wallet_time)
      .print(f'Start block: {Provider.start_block}, End block: {Provider.end_block}')
      .print('Checking transactions...')
      .txn_exist_in_range(Extracter.addresses())
      .print(f'Execution time: {time.time() - start}')
  )

  Extracter.write_addresses()
  Extracter.report()