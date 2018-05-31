#!/usr/bin/env python
#
# Very basic example of using Python 3 and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# This script is example code from this blog post:
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
# This is an updated version of the original -- modified to work with Python 3.4.
#
import sys
import imaplib
import email
import email.header
import time
import json

startMsg = "start program"
endMsg = "get results"
M = imaplib.IMAP4_SSL('imap.gmail.com')

def init():
    with open("gmailCreds.json") as f:
        creds = json.load(f)

    EMAIL_ACCOUNT = str(creds["email"])
    PASSWORD = str(creds["password"])

    # Use 'INBOX' to read inbox.  Note that whatever folder is specified,
    # after successfully running this script all emails in that folder
    # will be marked as read.

    EMAIL_FOLDER = "INBOX"

    main(EMAIL_ACCOUNT,PASSWORD,EMAIL_FOLDER)

def process_mailbox(M):
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """

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
        print('Message %s: %s' % (num, subject))
        #print(msg)
        parseEmail(msg,subject)

def parseEmail(msg,subject):
    if str(subject).lower() == "program" and "start program" in str(msg).lower():
        print("Starting program...")
        M.logout()
        #M.close()
        reset = __import__("reset")
        reset.main()
        mainProgram = __import__("main")
        mainProgram.main()

def main(EMAIL_ACCOUNT,PASSWORD,EMAIL_FOLDER):
    try:
        rv, data = M.login(EMAIL_ACCOUNT, PASSWORD)
    except imaplib.IMAP4.error:
        print("LOGIN FAILED!!! ")
        sys.exit(1)

    while True:
        rv, mailboxes = M.list()
        if rv == 'OK':
            print("Mailboxes:")
            print(mailboxes)
        rv, data = M.select(EMAIL_FOLDER)
        if rv == 'OK':
            print("Processing mailbox...\n")
            process_mailbox(M)

        else:
            print("ERROR: Unable to open mailbox ", rv)

        time.sleep(1)

init()