from xml.etree.ElementTree import parse, ParseError
import sys
import hashlib


def gethashfrompointerfile(pointerfile):
    root = parse(pointerfile).getroot()
    try:
        return root.findall(".//{info:lc/xmlns/premis-v2}messageDigest")[0].text
    except:
        pass

    try:
        return root.findall(".//{info:lc/xmlns/premis-v3}messageDigest")[0].text
    except:
        pass

    raise ParseError


aip = sys.argv[1]
try:
    hashfrompointerfile = gethashfrompointerfile(sys.argv[2])
except ParseError:
    print("Hash not found in pointerfile " + sys.argv[2])
    exit(1)

BUF_SIZE = 65536
sha256 = hashlib.sha256()

with open(aip, 'rb') as f:
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        sha256.update(data)

print("hash from aip:         " + hashfrompointerfile)
print("hash from pointerfile: " + sha256.hexdigest())

if hashfrompointerfile == sha256.hexdigest():
    exit(0)
else:
    print("hashes do not match!")
    exit(1)
