import os
import platform
import urllib.request
from zipfile import ZipFile 
import shutil

blobsVersion = "v1.1"
mpLinuxURL = f"https://github.com/WaylandProject/ragemp-blobs/releases/download/{blobsVersion}/rage-server-linux.tar.gz"
mpWindowsURL = f"https://github.com/WaylandProject/ragemp-blobs/releases/download/{blobsVersion}/rage-server-windows.zip"
doneFile = ".init"

def exec(cmd: str, log: bool = False):
    out = os.popen(cmd).read()
    if log:
        print(out)

if os.path.exists(doneFile):
    exit(0)

os.mkdir("../temp")

if platform.system() == "Linux":
    urllib.request.urlretrieve(mpLinuxURL, "../temp/mp.zip")
elif platform.system() == "Windows":
    urllib.request.urlretrieve(mpWindowsURL, "../temp/mp.zip")

print('Server blobs downloaded!') 

with ZipFile("../temp/mp.zip", 'r') as zip:   
    # extracting all the files
    zip.extractall("../mp") 
    print('Server blobs extracted!') 

shutil.rmtree("../temp")
with open(".init", "w") as f:
    f.write("")
    f.close()

# Download NPM dependencies for clientside
exec("cd ../client && npm i", True)
exec("cd ../client/ui && npm i", True)