from __future__ import unicode_literals, absolute_import

import subprocess
import os

def fetchEnvVarFromHeroku(var_name):
	process = subprocess.Popen(['heroku', 'config:get', var_name], stdout=subprocess.PIPE)
	out, err = process.communicate()
	if err:
		print(err)
		exit(1)
	else:
		return out[-1]

def fetchEnvVar(var_name):
	try:
		return os.environ[var_name]
	except KeyError:
		return fetchEnvVarFromHeroku(var_name)

# Example of your code beginning
#           Config vars
TOKEN = fetchEnvVar('TELEGRAM_TOKEN') # id:str
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

DATABASE_URL = fetchEnvVar('DATABASE_URL') # postgres://user:pass@host:pass/dbname
