from constant import *
from logger import get_logger
from threading import Lock
from utilities import logging
from icecream import ic
import json

"""
Extract meaningful data from raw transactions
"""
class Extracter:
  _logger = get_logger(__name__)
  _addressess = {}
  _lock = Lock()

  @classmethod
  def addresses(cls, address=None, value=False):
    with cls._lock:
      if address:
        cls._addressess.update({address: value})
      return cls._addressess
  
  @classmethod
  @logging()
  def unique_address(cls, result):
    for txn in result:
      cls.addresses(txn["from"])
      cls.addresses(txn["to"])

  @classmethod
  @logging()
  def new_address(cls, result, address):
    if result:
      return
    
    cls.addresses(address, True)

  @classmethod
  def report(cls):
    unique_count = len(cls.addresses())
    new_count = len([value for value in cls.addresses().values() if value == True])
    ic(f"Unique addresses: {unique_count}, New addresses: {new_count}")

  @classmethod
  def write_addresses(cls):
    with open('addresses.json', 'w') as f:
      f.write(json.dumps(cls._addressess, indent=2))