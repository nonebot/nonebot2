from datetime import timedelta

API_ROOT = ''
SECRET = ''
ACCESS_TOKEN = ''
HOST = '127.0.0.1'
PORT = 8080
DEBUG = True

SUPERUSERS = set()
COMMAND_START = {'/', '!', '／', '！'}
COMMAND_SEP = {'/', '.'}
SESSION_EXPIRE_TIMEOUT = timedelta(minutes=5)
