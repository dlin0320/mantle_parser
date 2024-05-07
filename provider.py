from utilities import build_url, logging, retry, try_get, defer
from concurrent.futures import Future, ThreadPoolExecutor
from enum import Enum
from threading import Semaphore
from itertools import cycle
from constant import API_KEYS
from logger import get_logger
from extracter import Extracter
from constant import *
from icecream import ic
import queue
import time
import os

'''
Provide raw transactions from mantle api
'''
class Provider:
  class Status(Enum):
    IDLE = 'idle'
    RUNNING = 'running'

    def transition(self):
      provider = ''
      if self == self.IDLE:
        Provider.status = self.RUNNING
        provider = f'{self} -> {Provider.status}'
        ic(provider)
        Provider._executor.submit(Provider._start)
        Provider._wait()
      elif self == self.RUNNING:
        Provider.status = self.IDLE
        provider = f'{self} -> {Provider.status}'
        ic(provider)
        Provider._reset()

  _logger = get_logger(__name__)
  status = Status.IDLE
  start_block = 0
  end_block = 'latest'

  @classmethod
  def _speedup(cls, factor=10):
    cls._pause = max(cls._pause / factor, MIN_PAUSE)

  @classmethod
  def _slowdown(cls, factor=10):
    cls._pause = min(cls._pause * factor, MAX_PAUSE)

  @classmethod
  def _qsize(cls):
    return cls._queue.qsize()
  
  @classmethod
  def _fsize(cls):
    return len(cls._futures)
  
  @classmethod
  def _reset(cls):
    cls._keys = cycle(API_KEYS)
    cls._queue = queue.PriorityQueue()
    cls._max_workers = os.cpu_count()
    cls._semaphore = Semaphore(cls._max_workers)
    cls._executor = ThreadPoolExecutor()
    cls._futures = list[Future]()
    cls._pause = MIN_PAUSE
    cls._count = 0
    cls._action_list = [
      'txlist', 
      'txlistinternal', 
      'tokentx', 
      'tokennfttx', 
      'token1155tx'
    ]
  
  @classmethod
  @logging()
  def _retry(cls, *args):
    return cls._enqueue(0, *args)
  
  @classmethod
  @logging()
  def _enqueue(cls, priority, *args):
    cls._count += 1
    item = (priority, cls._count, *args)
    return cls._queue.put(item)
    
  @classmethod
  @logging()
  def _start(cls):
    while not cls._queue.empty():
      cls._semaphore.acquire()
      item = cls._queue.get()
      _, _, func, *args = item
      future = cls._executor.submit(func, *args)
      cls._futures.append(future)

      cls._count += 1
      if cls._count % 6 == 0:
        cls._speedup()

      time.sleep(cls._pause)

  @classmethod
  @logging()
  def _wait(cls) -> 'Provider':
    with defer(cls.status.transition):
      while cls._qsize() > 0 or cls._fsize() > 0:
        progress = f'Queue size: {cls._qsize()}, Future size: {cls._fsize()}, Pause: {cls._pause}'
        ic(progress)
        cls._futures = [future for future in cls._futures if not future.done()]
        time.sleep(3)

      return cls

  @classmethod
  @logging()
  @retry()
  def _get_txn(cls, url):
    with defer(cls._semaphore.release):
      if isinstance(result := try_get(url), Exception):
        cls._slowdown()
        raise result
      Extracter.unique_address(result)

  @classmethod
  @logging()
  @retry()
  def _txn_exist(cls, url, address):
    with defer(cls._semaphore.release):
      if Extracter.addresses()[address]:
        return
      
      if isinstance(result := try_get(url), Exception):
        cls._slowdown()
        raise result
      Extracter.new_address(result, address)

  @classmethod
  @logging()
  @retry()
  def _set_start_block(cls, url):
    with defer(cls._semaphore.release):
      if isinstance(result := try_get(url), Exception):
        cls._slowdown()
        raise result
      cls.start_block = result

  @classmethod
  @logging()
  @retry()
  def _set_end_block(cls, url):
    with defer(cls._semaphore.release):
      if isinstance(result := try_get(url), Exception):
        cls._slowdown()
        raise result
      cls.end_block = result

  @classmethod
  def init(cls) -> 'Provider':
    cls._reset()
    return cls
  
  @classmethod
  @logging()
  def set_range(cls, start_time, end_time) -> 'Provider':
    with defer(cls.status.transition):
      params = {
        'module': 'block',
        'action': 'getblocknobytime',
        'timestamp': start_time,
        'closest': 'before',
        'apikey': next(cls._keys)
      }
      cls._enqueue(0, cls._set_start_block, build_url(params))

      params.update({
        'timestamp': end_time,
        'apikey': next(cls._keys)
      })
      cls._enqueue(0, cls._set_end_block, build_url(params))

      return cls

  @classmethod
  def get_txn_in_range(cls, addresses) -> 'Provider':
    with defer(cls.status.transition):
      for address in addresses:
        for priority, action in enumerate(cls._action_list):
          key = next(cls._keys)
          params = {
            'module': 'account',
            'action': str(action),
            'address': address,
            'startblock': cls.start_block,
            'endblock': cls.end_block,
            'page': '1',
            'offset': '10000',
            'sort': 'asc',
            'apikey': key
          }
          url = build_url(params)
          cls._enqueue(priority, cls._get_txn, url)
      return cls

  @classmethod
  def txn_exist_in_range(cls, addresses) -> 'Provider':
    with defer(cls.status.transition):
      for address in addresses:
        for priority, action in enumerate(cls._action_list):
          key = next(cls._keys)
          params = {
            'module': 'account',
            'action': str(action),
            'address': address,
            'startblock': cls.start_block,
            'endblock': cls.end_block,
            'page': '1',
            'offset': '1',
            'apikey': key
          }
          url = build_url(params)
          cls._enqueue(priority, cls._txn_exist, url, address)

      return cls
  
  @classmethod
  def print(cls, provider) -> 'Provider':
    ic(provider)

    return cls
  
  @classmethod
  def check(cls, condition) -> 'Provider':
    assert condition

    return cls