import os
import platform
import subprocess
import shutil

def exec(cmd: str, log: bool = False):
    out = os.popen(cmd).read()
    if log:
        print(out)
    
def build_server():
    cp_cmd = "cp -r"
    if platform.system() == "Windows":
        cp_cmd = "copy"
    os.chdir("../server")
    exec("dotnet restore", True)
    exec("dotnet build", True)
    shutil.copytree("./compiled", "../mp/dotnet/resources/", dirs_exist_ok=True)
    shutil.copy("./Config/meta.xml", "../mp/dotnet/resources/netcoreapp3.1/meta.xml")
    shutil.copy("./Config/settings.xml", "../mp/dotnet/settings.xml")
    shutil.copy("./Config/conf.json", "../mp/conf.json")
    print("Server was successfully built!")

def build_client():
    os.chdir("../client")
    exec("tsc", True)
    exec("cd ui && ng build", True)
    shutil.copytree("./build", "../mp/client_packages/cs", dirs_exist_ok=True)
    shutil.copytree("./ui/dist", "../mp/client_packages/ui", dirs_exist_ok=True)
    print("Client was successfully built!")

def clean_server():
    shutil.rmtree("../mp/dotnet/resources", ignore_errors=True)
    shutil.rmtree("../client/ui/dist", ignore_errors=True)
    shutil.rmtree("../client/build", ignore_errors=True)
    print("Server was successfully cleaned!")

def start_server():
    exec_name = "ragemp-server"
    if platform.system() == "Windows":
        exec_name + ".exe"
    subprocess.Popen(f"cd ../mp && ./{exec_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    

clean_server()
build_client()
build_server()

