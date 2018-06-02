import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
getEmail = __import__("getEmailFromFile")

def main():
    subject = "Program Started Successfully"
    body = "<font size=4>The program has been started successfuly and will be accepting new responses in the google form for the next 5 minutes. Afterwards, an email will be sent an administrator with a list of the top 75 parking pass applicants</font>" #Set this to however long it will run
    reciever = getEmail("Kyle") #Change to admins name
    sendEmail(reciever,subject,body)

def sendEmail(reciever,subject,body):
    msg = MIMEMultipart()
    msg['From'] = "bccparkingpass@gmail.com"
    msg['To'] = reciever
    password = "n0AhRoX$U9!i"
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  # Converts body into correct format
    print(msg)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail("parkingpassadmin", msg['To'], msg.as_string())
    server.quit()
    runMain()

def runMain():
    googleSheetsScraper = __import__("Google Sheets Scraper")
    googleSheetsScraper.main()

#main("kkingsbe@gmail.com")