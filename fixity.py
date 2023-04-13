from xml.etree.ElementTree import parse
import sys
import hashlib

aip = sys.argv[1]
pointerfile = sys.argv[2]

root = parse(pointerfile).getroot()
hashfrompointerfile = root.findall(".//{info:lc/xmlns/premis-v2}messageDigest")[0].text

BUF_SIZE = 65536
sha256 = hashlib.sha256()

with open(aip, 'rb') as f:
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        sha256.update(data)

print("hash fron aip:         " + hashfrompointerfile)
print("hash from pointerfile: " + sha256.hexdigest())

if hashfrompointerfile == sha256.hexdigest():
    exit(0)
else:
    print("hashes do not match!")
    exit(1)
