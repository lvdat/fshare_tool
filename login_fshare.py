#
# Created on Thu Apr 21 2022
#
# 2022 (c) levandat
#

from ast import parse
import configparser
from distutils.command.config import config
import requests
import sys
import json

# sys func
def exit(err):
  sys.exit(err)

# read config file
parser = configparser.ConfigParser()
parser.read('config.ini')

# get data from config
USER_API_URL = parser.get('API', 'USER_API_URL')
MAIL = parser.get('Auth', 'MAIL')
PASSWORD = parser.get('Auth', 'PASSWORD')
USER_AGENT = parser.get('Auth', 'USER_AGENT')
APP_KEY = parser.get('Auth', 'APP_KEY')

if(MAIL == '' or PASSWORD == '' or USER_AGENT == '' or APP_KEY == ''):
  exit("-> Please fill all Auth fields in config.ini!")

print("-> Connecting to Fshare... ")

# api-endpoint (using Fshare API V2)
URL = USER_API_URL + "/login"
header = {"Content-Type": "application/json", "accept": "application/json", "User-Agent": USER_AGENT}

# defining a params dict for the parameters to be sent to the API
Data = {
  "user_email": MAIL,
  "password": PASSWORD,
  "app_key": APP_KEY
}

# sending get request and saving the response as response object
r = requests.post(url = URL, headers= header, json = Data)

# check status from response
# 200: success
# 405: wrong password
sc = r.status_code
print("Status: ", sc)

if(sc == 405):
  exit("-> Wrong Password, please edit correct information config")
if(sc == 406):
  exit("-> Account not activated")
if(sc == 409):
  exit("-> Account is locked login")
if(sc == 410):
  exit("-> Account is locked")
if(sc == 424):
  exit("-> You entered wrong password 3 times, please enter again after 10 minutes")
if(sc != 200):
  exit("-> Unknown error.")

#get data from response
s1 = json.dumps(r.json())
d = json.loads(s1)
token = d["token"]
ssid = d["session_id"]

parser.set('Login', 'SESSION_ID', ssid)
parser.set('Login', 'TOKEN', token)

with open('config.ini', 'w') as f:
  parser.write(f)
  
print("-> Done!")