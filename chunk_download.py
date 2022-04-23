import math
import requests, enlighten

url = 'http://download.xs4all.nl/test/10GB.bins'
fname = '1GB.bin'

# Should be one global variable
MANAGER = enlighten.get_manager()

r = requests.get(url, stream = True)
assert r.status_code == 200, r.status_code
dlen = int(r.headers.get('Content-Length', '0')) or None

with MANAGER.counter(color = 'green', total = dlen and math.ceil(dlen / 2 ** 20), unit = 'MiB', leave = False) as ctr, \
     open(fname, 'wb', buffering = 2 ** 24) as f:
    for chunk in r.iter_content(chunk_size = 2 ** 20):
        print(chunk[-16:].hex().upper())
        f.write(chunk)
        ctr.update()