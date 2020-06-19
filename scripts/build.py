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
import sys
import signal
import shlex


def exec(cmd: str, log: bool = False):
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, shell=True)
    signal.signal(signal.SIGINT, lambda sig, frame: _stop_process(process))
    encodings = ['utf-8', 'cp866']
    while True:
        line = process.stdout.readline()
        if not line:
            break
        if log:
            for e in encodings:
                try:
                    print(line.decode("cp866"), end='')
                except UnicodeDecodeError:
                    pass
                else:
                    break

def build_server():
    cp_cmd = "cp -r"
    if platform.system() == "Windows":
        cp_cmd = "copy"
    os.chdir("../server")
    exec("dotnet restore", True)
    exec("dotnet build", True)
    shutil.copytree("./compiled", "../mp/dotnet/resources/",
                    dirs_exist_ok=True)
    shutil.copy("./Config/meta.xml",
                "../mp/dotnet/resources/netcoreapp3.1/meta.xml")
    shutil.copy("./Config/settings.xml", "../mp/dotnet/settings.xml")
    shutil.copy("./Config/conf.json", "../mp/conf.json")
    if not os.path.exists("../mp/s_config.toml"):
        shutil.copy("./Config/s_config.sample.toml", "../mp/s_config.toml")
    print("Server was successfully built!")

def build_client():
    os.chdir("../client")
    exec("tsc", True)
    exec("cd ui && ng build", True)
    shutil.copytree("./build", "../mp/client_packages", dirs_exist_ok=True)
    shutil.copytree("./ui/dist", "../mp/client_packages/ui",
                    dirs_exist_ok=True)
    print("Client was successfully built!")

def clean_server():
    shutil.rmtree("../mp/dotnet/resources", ignore_errors=True)
    shutil.rmtree("../mp/client_packages", ignore_errors=True)
    shutil.rmtree("../client/ui/dist", ignore_errors=True)
    shutil.rmtree("../client/build", ignore_errors=True)
    print("Server was successfully cleaned!")

def start_server():
    os.chdir("../mp")
    exec_name = "ragemp-server"
    if platform.system() == "Windows":
        exec_name + ".exe"
    exec(f"{exec_name}", True)

def start_ui_dev():
    os.chdir("../client/ui")
    exec("ng serve", True)

def _stop_process(process: subprocess.Popen):
    process.send_signal(signal.CTRL_C_EVENT)
    process.wait()
    sys.exit(0)

try:
    operation = sys.argv[1]
except IndexError:
    clean_server()
    build_client()
    build_server()
    sys.exit(0)

if operation == "server":
    build_server()
elif operation == "client":
    build_client()
elif operation == "clean":
    clean_server()
elif operation == "start":
    start_server()
elif operation == "ui_dev":
    start_ui_dev()
else:
    print("Unknown operation! Available only following operations: server, client, clean, ui_dev or start (or just empty - rebuild whole server and client).")
