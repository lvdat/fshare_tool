#
# Created on Thu Apr 21 2022
#
# 2022 (c) levandat
#
# f_dl.py <File URL> [File Password]
import requests, configparser, json, sys, urllib, os
from function import *
from urllib.parse import unquote

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

j = requestToJson(r)

DL_URL = j['location']
FILE_NAME = unquote(DL_URL.split('/')[-1])
FOLDER_DOWNLOAD = cf['Drive']['file_download_path']
FILE_FULL_PATH = FOLDER_DOWNLOAD + FILE_NAME

if not os.path.exists(FOLDER_DOWNLOAD):
    os.makedirs(FOLDER_DOWNLOAD)
### Create directory if it not exist.

print("┌───────────┐")
print("| File Info |")
print("└───────────┘")
print("+-------------+------------------------------------+")
print("-> File Name: " + FILE_NAME)
print("-> Save Folder: " + FOLDER_DOWNLOAD)

chunk_download(DL_URL, FILE_NAME, FOLDER_DOWNLOAD)
print("+--------------------------------------------------+")
print("-> Done! Starting upload to Drive..." if cf['Drive']['gdrive'] == "1" or cf['Drive']['onedrive'] == "1" else "You are in download only mode, if you want upload to Drive please config!")

if(cf['Drive']['gdrive'] == "1"):
    DRIVE_FOLDER = cf['Drive']['folder_id']
    print('-> Uploading to Google Drive...')
    pushToDrive(FILE_FULL_PATH, DRIVE_FOLDER)

if(cf['Drive']['onedrive'] == "1"):
    REMOTE_NAME = cf['Drive']['rclone_remote_name']
    ONEDRIVE_PATH = cf['Drive']['onedrive_folder_path']
    print('-> Uploading to OneDrive...')
    pushToOneDrive(FILE_FULL_PATH, REMOTE_NAME, ONEDRIVE_PATH)

REMOVE_FILE = (cf['Drive']['gdrive'] != "1" and cf['Drive']['onedrive'] != "1") or (cf['Drive']['gdrive'] == "1" or cf['Drive']['onedrive'] == "1" and cf['Drive']['remove_file_after_upload'] == 'True')
if REMOVE_FILE:
    print("-> Done! Removing downloaded file...")
    removeFile(FILE_FULL_PATH)
