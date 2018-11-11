from __future__ import unicode_literals, absolute_import

import subprocess
import os

# ---------------
# --- GLOBALS ---
# ---------------

RUSIK_CHAT_ID = -172022743
JEKA_DJ_CHAT_ID = 239745097
DENIS_EMINEM_CHAT_ID = 129085681
VLAD_KULAK_CHAT_ID = 1591398
BODIES = [
    JEKA_DJ_CHAT_ID,        # Jeka_DJ
    DENIS_EMINEM_CHAT_ID,   # Denis_Eminem
    VLAD_KULAK_CHAT_ID,     # Vlad_Kulak
]

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
