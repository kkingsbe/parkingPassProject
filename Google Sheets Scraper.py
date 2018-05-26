import gspread
from oauth2client.service_account import ServiceAccountCredentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,time

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

thresholdScore = 100 #The lowest score to be able to apply for a parking pass

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
        if person.get("Are you an elected SGA official?").lower() == "yes": #100 points if SGA official
            score += 100
        if person.get("Are you the captain of a varsity team that is CURRENTLY in season?").lower() == "yes": #100 points if varsity captian
            score += 100
        if person.get("Is there currently a school bus route in your neighborhood that you can take to school?").lower() == "no" and int(person.get('If you answered "NO" to the previous question, approximately how long does it typically take you to get to school, in minutes? Please enter a number.')) > 0: #If no bus services the neighborhood
            score += int(person.get('If you answered "NO" to the previous question, approximately how long does it typically take you to get to school, in minutes? Please enter a number.')) * 10
        if person.get("Do you go DIRECTLY to a job after school?").lower() == "yes" and int(person.get("If you answered yes to the previous question, how many days per week do you work?")) <= 7:  #If they work after school
            score += 4 + int(person.get("If you answered yes to the previous question, how many days per week do you work?"))
        if person.get("Do you go directly to an extracurricular activity after school?").lower() == "yes" and int(person.get("If you answered yes to the previous question, how many days do you participate in extracurriculars per week?")) > 0 :  #If they participate in extracurricular activities
            score += 2 + int(person.get("If you answered yes to the previous question, how many days do you participate in extracurriculars per week?"))
        if int(person.get("How many people would you carpool with if you receive the pass? (0 if it's just you)")) > 0:  #How many people would carpool with the person answering
            score += int(person.get("How many people would you carpool with if you receive the pass? (0 if it's just you)")) * 10

        if score > thresholdScore:
            parkingPass = True
        else:
            parkingPass = False

        f.write(person.get("Email Address") + '\n') #Adds the persons email to the email list with a new line at the end
        f.close()

        scorePass = []
        scorePass.append(score)
        scorePass.append(parkingPass)
        return scorePass

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


def stripNewLineFromList(List):
    for x in range(len(List)):
        List[x] = List[x].strip("\n")
    return List


while True:
    try:
        if list_of_hashes != sheet.get_all_records(): #If there is a change in the spreadsheet
            list_of_hashes = sheet.get_all_records()
            print("New Response!")
            alreadyEvaluated = open("emailList.txt","r+").readlines()
            for x in range(len(list_of_hashes)):
                alreadyEvaluated = stripNewLineFromList(alreadyEvaluated)
                recieve = list_of_hashes[x].get("Email Address") #Gets current persons email address
                print("Already Evaluated: " + str(alreadyEvaluated))
                if recieve not in alreadyEvaluated: #If the current persons email is not in the email list
                    scorePass = getScore(list_of_hashes[x])
                    parkingPass = scorePass[1]
                    score = scorePass[0]
                    if parkingPass == True:
                        body = "You are eligible for a parking pass. SCORE: " + str(score)  #Email for if you are eligible
                    else:
                        body = "You are not eligible for a parking pass. SCORE: " + str(score) #Email for if you are not eligible

                    sendEmail("Parking Pass Update",body,recieve)

    except Exception as e:
        print("Error: " + str(e))
        if "nonetype" in str(e).lower():
            print("Maybe the text for one of the questions was changed?")

    time.sleep(1)