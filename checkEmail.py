import sys
import imaplib
import email
import email.header
import time
import json

def init():
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    with open("gmailCreds.json") as f:
        creds = json.load(f)

    EMAIL_ACCOUNT = str(creds["email"])
    PASSWORD = str(creds["password"])

    # Use 'INBOX' to read inbox.  Note that whatever folder is specified,
    # after successfully running this script all emails in that folder
    # will be marked as read.

    EMAIL_FOLDER = "INBOX"

    main(EMAIL_ACCOUNT,PASSWORD,EMAIL_FOLDER,M)

def process_mailbox(M):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        subject = str(hdr)
        #print('Message %s: %s' % (num, subject))
        parseEmail(msg,subject,M)

def parseEmail(msg,subject,M):
    if str(subject).lower() == "program" and "start program" in str(msg).lower():
        print("Subject: " + str(subject))
        print("Body: " + str(msg))
        print("Starting program...")
        M.store('1:*', '+X-GM-LABELS', '\\Trash')
        M.expunge()
        M.logout()
        reset = __import__("reset")
        reset.main()

        googleSheetsScraper = __import__("Google Sheets Scraper")
        googleSheetsScraper.main()

def main(EMAIL_ACCOUNT,PASSWORD,EMAIL_FOLDER,M):
    try:
        rv, data = M.login(EMAIL_ACCOUNT, PASSWORD)
    except imaplib.IMAP4.error:
        print("LOGIN FAILED!!! ")
        sys.exit(1)

    while True:
        rv, data = M.select(EMAIL_FOLDER)
        if rv == 'OK':
            #print("Processing mailbox...\n")
            process_mailbox(M)

        else:
            print("ERROR: Unable to open mailbox ", rv)

        time.sleep(1)