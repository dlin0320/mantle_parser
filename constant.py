import dotenv
import os

dotenv.load_dotenv()

API_KEYS = os.environ.get('API_KEYS').split(',')

BASE_URL = 'https://api.mantlescan.xyz/api'

GENESIS_TIMESTAMP = 1688314886

SMART = '0xc799d8f3ad911a03ac1e1f93baa2e961b4047803'

FRENS = '0x827c60adabef4419a0b23fe675fd1827b588caac'

ERROR_MESSAGES = ['Max rate limit reached']

MIN_PAUSE = 0.1

MAX_PAUSE = 10