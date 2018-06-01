import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def sendEmail(subject,body,reciever):
    msg = MIMEMultipart()
    msg['From'] = "bccparkingpass@gmail.com"
    msg['To'] = reciever
    password = "n0AhRoX$U9!i"
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html')) #Converts body into correct format
    print(msg)

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(msg['From'],password)
    server.sendmail("parkingpassadmin",msg['To'],msg.as_string())
    server.quit()

def getLen():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Make sure you use the right name here.
    sheet = client.open("Parking Pass Application (Responses)").worksheet("Accepted")

    # Extract all of the values
    list_of_hashes = sheet.get_all_records()
    return len(list_of_hashes)

def main():
    sortSheet = __import__("sortSheet")
    sortSheet.main()

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Make sure you use the right name here.
    sheet = client.open("Parking Pass Application (Responses)").worksheet("Accepted")

    # Extract all of the values
    list_of_hashes = sheet.get_all_records()

    namesList = []
    body = "<p>" #Initializes body as empty string
    body += "<h3> Below are the top 75 parking pass applicants: </h3> <br />"

    for row in list_of_hashes:
        if list_of_hashes.index(row) <= 75:
            nameDict = {"name" : row.get("Full Name"), "email" : row.get("Email Address"), "score" : row.get("Score"), "Pass" : row.get("Pass")}
            namesList.append(nameDict)

    for name in namesList:
        body += name.get("name")
        body += " "
        body += name.get("email")
        body += "<br />"

    body += "</p>"
    reciever = "kkingsbe@gmail.com" #Email of reciever

    sendEmail("Your list of top 75 parking pass applicants is complete",body,reciever)