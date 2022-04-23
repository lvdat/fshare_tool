#
# Created on Thu Apr 21 2022
#
# 2022 (c) levandat
#
import requests, configparser, json, sys
from function import *

FILE_PASSWORD = ''
if len(sys.argv) == 1:
    exit("-> Please include file URL")
elif len(sys.argv) == 3:
    FILE_PASSWORD == sys.argv[2]
FILE_URL = sys.argv[1]

ps = myParser()
cf = toDict(ps)

# get data from config
FILE_DL_API_URL = cf['API']['file_dl_api_url']
USER_AGENT = cf['Auth']['user_agent']
APP_KEY = cf['Auth']['app_key']
SESSION_ID = cf['Login']['session_id']
TOKEN = cf['Login']['token']

if(SESSION_ID == '' or TOKEN == ''):
    exit("-> Please login first!")

print("-> Connecting to Fshare...")

header = {"Content-Type": "application/json", "accept": "application/json", "User-Agent": USER_AGENT, "Cookie": "session_id=" + SESSION_ID}
Data = {
  "url": FILE_URL,
  "password": FILE_PASSWORD,
  "token": TOKEN,
  "zipflag": 0
}

r = rq_fshare(URL = FILE_DL_API_URL, header = header, Data = Data)

if r.status_code != 200:
    exit(errorInfo(r.status_code))


print(requestToJson(r))