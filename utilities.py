from contextlib import contextmanager
import functools
from logging import Logger
from typing import Callable
from constant import *
from urllib.parse import urlencode, urlunparse, urlparse
from datetime import datetime
from logger import default_logger
import requests
import time

def date_to_timestamp(date: datetime):
	return int(date.timestamp())
	
def build_url(params):
	url_parts = list(urlparse(BASE_URL))
	url_parts[2] = '/api'
	url_parts[4] = urlencode(params)
	return urlunparse(url_parts)

def try_get(url, timeout=60):
	try:
		response = requests.get(url, timeout=timeout)
		response.raise_for_status()
		json = response.json()
		if (result := json['result']) in ERROR_MESSAGES:
			raise Exception(result)
		return result
	except Exception as e:
		return e
	
@contextmanager
def defer(defer: Callable):
	try:
		yield
	finally:
		defer()

def retry():
	def decorator(func):
		@functools.wraps(func)
		def wrapper(cls, *args, **kwargs):
			retry = getattr(cls, '_retry', None)
			try:
				return func(cls, *args, **kwargs)
			except Exception:
				if callable(retry):
					retry(func, *args)
				raise
		return wrapper
	return decorator

def logging():
	def decorator(func):
		@functools.wraps(func)
		def wrapper(cls, *args, **kwargs):
			logger: Logger = getattr(cls, '_logger', default_logger)
			try:
				start = time.time()
				result = func(cls, *args, **kwargs)
				end = time.time()
				logger.info(f'fun: {func.__name__}, time: {end - start}')
				return result
			except Exception as e:
				logger.debug(f'fun: {func.__name__}, err: {e}')
				raise
		return wrapper
	return decorator