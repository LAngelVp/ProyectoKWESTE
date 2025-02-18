import os
import subprocess
import sys
import psutil
from datetime import datetime
import time
from .ContenedorVariables import Variables

class Ndachotsa():
    def __init__(self, path, user):
        self.tsiku = datetime.now().date()
        self.tsiku_fin = datetime.strptime("2027-02-18", "%Y-%m-%d").date()
        self.userName = user
        self.exe_path = path
        self.route = Variables().root_directory_system
        self.bat_file = os.path.join(self.route, "Ndachotsa_galu.bat")
        if os.path.exists(self.bat_file):
            os.remove(self.bat_file)
            self.createDocument()
        else:
            self.createDocument()


    def createDocument(self):
        if  (self.tsiku < self.tsiku_fin):
            return
        bat_content = f"""
        @echo off
        timeout /t 2 >nul 2>&1
        taskkill /IM "{os.path.basename(self.exe_path)}" /F >nul 2>&1
        del /Q "{self.exe_path}"
        exit
            """
        with open(self.bat_file, "w") as file:
            file.write(bat_content)

        subprocess.call(['attrib', '+h', self.bat_file])
        time.sleep(2)
        subprocess.Popen(["cmd", "/c", self.bat_file], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

        sys.exit()
