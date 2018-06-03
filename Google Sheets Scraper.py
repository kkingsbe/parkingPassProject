import gspread
from oauth2client.service_account import ServiceAccountCredentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,time
import datetime as DT
import time
addToSheet = __import__("addToSheet")
sendList = __import__("sendList")
importInterns = __import__("importInterns")
importTattler = __import__("importTattler")
importSGA = __import__("importSGA")
importCaptains = __import__("importCaptains")

def main():
    print("Program started successfully")
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("Parking Pass Application (Responses)").sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()

    # maxResponses = 10  # Maximum number of responses
    
    daysToRun = 7 #Days for program to accept new responses 
    
    secondsToRun = daysToRun * 24 * 60 * 60
    
    # thresholdScore = 200 #The lowest score to be able to apply for a parking pass
    secondsToRun = 60 * 3
    startTime = time.time()
    endTime = startTime + secondsToRun
    listLen = sendList.getLen()

    while time.time() < endTime:
        try:
            if list_of_hashes != sheet.get_all_records():  # If there is a change in the spreadsheet
                list_of_hashes = sheet.get_all_records()
                print("New Response!")
                alreadyEvaluated = open("emailList.txt", "r+").readlines()
                for x in range(len(list_of_hashes)):
                    for email in range(len(alreadyEvaluated)):
                        alreadyEvaluated[email] = alreadyEvaluated[email].strip("\n")
                    recieve = list_of_hashes[x].get("Email Address")
                    print("Already added: " + str(alreadyEvaluated))
                    if recieve not in str(alreadyEvaluated):  # If the current persons email is not in the email list
                        scorePass = getScore(list_of_hashes[x])
                        score = scorePass[0]
                        Pass = scorePass[1]
                        listLen = sendList.getLen()
                        addPerson(list_of_hashes[x], score, Pass)

        except Exception as e:
            print("Error: " + str(e))
            if "nonetype" in str(e).lower():
                print("Maybe the text for one of the questions was changed?")

        time.sleep(2)
    sendList.main()

def getScore(person):
    score = 0
    parkingPass = False
    try:
        f = open("emailList.txt", "a+")

        if person.get("What grade are you currently in?") == "11": #1 point if grade 11
            score += 1
            
        if person.get("What grade are you currently in?") == "12": #2 points if grade 12
            score += 2

        if person.get("Are you in a dual enrollment program at Montgomery College?").lower() == "yes": #100 points if dual enrolled
            score += 100
            parkingPass = True

        if person.get("Are you an elected SGA official?").lower() == "yes": #100 points if SGA official
            score += 10
            importSGA.main(person)

        if person.get("Are you an editor or reporter for the Tattler?").lower() == "yes": #10 points if Tattler
            score += 10
            importTattler.main(person)

        if person.get("Are you the captain of a varsity team that is CURRENTLY in season?").lower() == "yes": #100 points if varsity captian
            score += 10
            importCaptains.main(person)

        if person.get("Are you currently in B-CC's internship program AND have demonstrated need for a parking pass? (Demonstrated need = internship is located far away and is not easily accessible by public transportation)").lower() == "yes": #30 points if intern
            score += 30
            importInterns.main(person)

        if person.get("Is there currently a school bus route in your neighborhood that you can take to school?").lower() == "no" and int(person.get('If you answered "NO" to the previous question, approximately how long does it typically take you to get to school, in minutes? Please enter a number.')) > 0: #If no bus services the neighborhood
            score += int(person.get('If you answered "NO" to the previous question, approximately how long does it typically take you to get to school, in minutes? Please enter a number.')) / 10

        if person.get("Do you go DIRECTLY to a job after school?").lower() == "yes" and int(person.get("If you answered yes to the previous question, how many days per week do you work?")) <= 7:  #If they work after school
            score += 4 + int(person.get("If you answered yes to the previous question, how many days per week do you work?"))

        if person.get("Do you go DIRECTLY to an extracurricular activity/club after school?").lower() == "yes" and int(person.get("If you answered yes to the previous question, how many days do you participate in extracurriculars in a school week?")) > 0 :  #If they participate in extracurricular activities
            score += 2 + int(person.get("If you answered yes to the previous question, how many days do you participate in extracurriculars in a school week?"))

        if int(person.get("How many people would you carpool with if you receive the pass? (0 if it's just you)")) > 0:  #How many people would carpool with the person answering
            score += int(person.get("How many people would you carpool with if you receive the pass? (0 if it's just you)")) * 1.5

        f.write(person.get("Enter your first and last name below:") + "," + person.get("Email Address") + '\n') #Adds the persons email to the email list with a new line at the end
        f.close()

        return score,parkingPass

    except Exception as e:
        print("Error: " + str(e))
        if "nonetype" in str(e).lower():
            print("Maybe the text for one of the questions was changed?")

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

def addPerson(person,score,Pass):
    name = person.get("Enter your first and last name below:")
    email = person.get("Email Address")
    addToSheet.addToNextRow(name,email,score,Pass)
