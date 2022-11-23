import requests, configparser, sys

# sys func
def exit(err):
    sys.exit(err)

def myParser(path = 'config.ini'):
    ps = configparser.ConfigParser()
    ps.read(path)
    return ps

def toDict(self, get = 'All'):
    d = dict(self._sections)
    for k in d:
        d[k] = dict(self._defaults, **d[k])
        d[k].pop('__name__', None)
    return d if get == 'All' else d[get]

def errorInfo(error_code):
    ec = str(error_code)
    i = {
        '405': '-> Wrong Password, please edit correct information config',
        '406': '-> Account not activated',
        '409': '-> Account is locked login',
        '410': '-> Account is locked login',
        '424': '-> You entered wrong password 3 times, please enter again after 10 minutes',
        '201': '-> Not logged in yet! Please rerun login file!'
    }
    return i[ec] if ec in i else "Unknown Error"

def rq_fshare(type = 'POST', URL = '', header = {}, Data = {}):
    return requests.post(url = URL, headers = header, json = Data)

def requestToJson(self):
    import json
    return json.loads(json.dumps(self.json()))

def chunk_download(furl, name, folder = 'downloaded/'):
    import math, enlighten
    url = furl
    fname = name
    # Should be one global variable
    MANAGER = enlighten.get_manager()
    r = requests.get(url, stream = True)
    assert r.status_code == 200, r.status_code
    dlen = int(r.headers.get('Content-Length', '0')) or None
    print("-> File Size: ", "{:.2f}".format(dlen/(2**20)/1024),"GB (" + str(math.ceil(dlen/2**20)), "MB)")
    with MANAGER.counter(color = 'green', total = dlen and math.ceil(dlen / 2 ** 20), unit = 'MiB', leave = False) as ctr, \
        open(folder + fname, 'wb', buffering = 2 ** 24) as f:
        for chunk in r.iter_content(chunk_size = 2 ** 20):
            # print(chunk[-16:].hex().upper())
            f.write(chunk)
            ctr.update()
    return fname

def pushToDrive(file = '', path = ''):
    import os
    print("gdrive upload -p " + path + " '" + file + "'")
    with os.popen("gdrive upload -p " + path + " '" + file + "'") as f:
        print(f.readlines())
    #debug

def pushToOneDrive(file = '', remotename ='', path = ''):
    import os
    cmd = "rclone copy '" + file + "' " + remotename + ":" + path + " --drive-acknowledge-abuse --drive-keep-revision-forever --drive-use-trash=false"
    print(cmd)
    with os.popen(cmd) as f:
        print(f.readlines())

def removeFile(file = ''):
    import os
    print("-> Deleting local File...")
    print("rm -rf " + "'" + file + "'")
    os.popen("rm -rf " + "'" + file + "'")