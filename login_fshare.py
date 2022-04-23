#
# Created on Thu Apr 21 2022
#
# 2022 (c) levandat
#
import configparser, requests, sys, json
from function import *

ps = myParser()
cf = toDict(ps)

# get data from config
USER_API_URL = cf['API']['user_api_url']
MAIL = cf['Auth']['mail']
PASSWORD = cf['Auth']['password']
USER_AGENT = cf['Auth']['user_agent']
APP_KEY = cf['Auth']['app_key']

if(MAIL == '' or PASSWORD == '' or USER_AGENT == '' or APP_KEY == ''):
  exit("-> Please fill all Auth fields in config.ini!")

print("-> Connecting to Fshare... ")

# api-endpoint (using Fshare API V2)
URL = USER_API_URL + "/login"
header = {"Content-Type": "application/json", "accept": "application/json", "User-Agent": USER_AGENT}
Data = {
  "user_email": MAIL,
  "password": PASSWORD,
  "app_key": APP_KEY
}

r = rq_fshare(URL = URL, header = header, Data = Data)

sc = r.status_code
if sc != 200:
  exit(errorInfo(sc))

d = requestToJson(r)
token = d["token"]
ssid = d["session_id"]

ps.set('Login', 'SESSION_ID', ssid)
ps.set('Login', 'TOKEN', token)

with open('config.ini', 'w') as f:
  ps.write(f)
  
print("-> Done!")
