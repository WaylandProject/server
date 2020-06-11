"""
 Copyright (C) 2020 ChronosX88
 
 This file is part of Wayland Project Server.
 
 Wayland Project Server is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 Wayland Project Server is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with Wayland Project Server.  If not, see <http://www.gnu.org/licenses/>.
"""

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
    shutil.copytree("./build", "../mp/client_packages", dirs_exist_ok=True)
    shutil.copytree("./ui/dist", "../mp/client_packages/ui", dirs_exist_ok=True)
    print("Client was successfully built!")

def clean_server():
    shutil.rmtree("../mp/dotnet/resources", ignore_errors=True)
    shutil.rmtree("../mp/client_packages", ignore_errors=True)
    #shutil.rmtree("../client/ui/dist", ignore_errors=True)
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

