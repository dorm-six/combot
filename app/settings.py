from __future__ import unicode_literals, absolute_import, print_function

import subprocess
import os

try:
    from app.secrets import SECRETS
except ImportError:
    SECRETS = dict()

# ---------------
# --- GLOBALS ---
# ---------------

JEKA_DJ_CHAT_ID = 239745097

OBWAGA6_CHAT_ID = -1001131239095
TESTGROUP_CHAT_ID = -1001176853573
OBWAGA_CHAT_IDS = [
    TESTGROUP_CHAT_ID,     # testgroup
    OBWAGA6_CHAT_ID,       # 
]

# -------------------
# --- ENV FETCHER ---
# -------------------

def fetchEnvVarFromHeroku(var_name):
    process = subprocess.Popen(['heroku', 'config:get', var_name], stdout=subprocess.PIPE)
    out, err = process.communicate()
    if err:
        print(err)
        exit(1)
    else:
        return out[:-1]

def fetchEnvVar(var_name):
    if var_name in SECRETS:
        return SECRETS[var_name]
    try:
        return os.environ[var_name]
    except KeyError:
        return fetchEnvVarFromHeroku(var_name)

# -------------------
# --- SECRET DATA ---
# -------------------

# Example of your code beginning
#           Config vars
TOKEN = fetchEnvVar('TELEGRAM_TOKEN') # id:str
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

DATABASE_URL = fetchEnvVar('DATABASE_URL') # postgres://user:pass@host:pass/dbname
