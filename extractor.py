import sys
import json
from urllib.parse import urlparse
import os
import base64

data = json.loads(sys.stdin.read())

title = data["log"]["pages"][0]["title"]



print(title)

hostnames = ("travel.mynavi.jp", "wedding.mynavi.jp")

def replace_hostname(content):
    for line in content.split("\n"):
        if "travel.mynavi.jp" in line:
            print("*", line)
    return content

for entry in data["log"]["entries"]:
    url = entry["request"]["url"]
    u = urlparse(url)
    if u.netloc in hostnames:
        response_size = entry["response"]["content"]["size"]
        response_encoding = entry["response"]["content"].get("encoding")
        path = u.netloc + u.path
        dirpath = os.path.dirname(path)
        filepath = os.path.basename(path)
        if filepath == "":
            filepath = "index.html"
        print(dirpath, filepath, response_size, response_encoding)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath) 
        destpath = os.path.join(dirpath, filepath)
        content = entry["response"]["content"]["text"]
        if response_encoding == "base64":
            bytes_content = base64.b64decode(content)
        else:
            content = replace_hostname(content)
            bytes_content = content.encode("utf-8")
        open(destpath, "wb").write(bytes_content)

