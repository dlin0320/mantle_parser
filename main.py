from datetime import timezone
from provider import Provider
from extracter import Extracter
from datetime import datetime
from utilities import date_to_timestamp
from constant import *

if __name__ == "__main__":
  Extracter.addresses(SMART)
  Extracter.addresses(FRENS)
  start_time = date_to_timestamp(datetime(2024, 3, 22, 7, 0, 0, tzinfo=timezone.utc))
  end_time = date_to_timestamp(datetime(2024, 4, 21, 23, 59, 59, tzinfo=timezone.utc))

  (
    Provider
      .init()
      .set_range(start_time, end_time)
      .print(f"Start block: {Provider.start_block}, End block: {Provider.end_block}")
      .get_txn_in_range(Extracter.addresses())
      .print(len(Extracter.addresses()))
      .set_range(GENESIS_TIMESTAMP, start_time)
      .print(f"Start block: {Provider.start_block}, End block: {Provider.end_block}")
      .txn_exist_in_range(Extracter.addresses())
  )

  Extracter.write_addresses()
  Extracter.report()