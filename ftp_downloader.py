import os
import ftplib


def download_ftp(server, remote_dir, local_dir):
    ftp = ftplib.FTP(server)
    ftp.login("anonymous", "")

    with open(local_dir, "wb") as f:
        ftp.retrbinart(f"RETY {remote_dir}", f.write)
    
    ftp.quit()


server = "127.0.0.1"
username = "THOMAS"
password = ""
remote_dir = "C:/KEYLOGFTP/Uploaded_Logs"
local_dir = "C:/Users/thoma/Desktop/Zuyd/Security/Logs"

download_ftp(server, remote_dir, local_dir)