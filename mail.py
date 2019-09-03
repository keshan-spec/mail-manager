import email
import email.header
import imaplib
import datetime
import sys
import os
import re
from getpass import getpass
import smtplib
import quopri

# GLOBAL VARIABLES
regex_pattern = r'(\\n)'

# TRY TO CONNECT TO HOST : GMAIL
try:
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
except Exception as e:
    print(f"[-] Connection Error : {e}")
    sys.exit()


# login to mail
def mail_login(email='', passwd=''):
    LoggedIn = False
    try:
        print(f'[+] Logging in to : {email}')
        mail.login(email, passwd)
        LoggedIn = True
        print(f'[+] Authenticated as {email} \n')

    except Exception as e:
        print(f"[-] ERROR: {e}")
        pass
    return LoggedIn


# logs out of mail
def logout():
    print("\n[+] Logging out.....")
    if mail.logout():
        print('[+] Logged out')
    else:
        print('[-] Error logging out')


# Converts the raw time to local time
def convert_local_date(msg_date):
    local_date = ''
    date_tuple = email.utils.parsedate_tz(msg_date)
    try:
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
    except Exception:
        pass
    return local_date


# decode the msg from raw encoded html to decoded string
def decode_message_to_str(msg):
    msg = str(msg.get_payload()[0])
    decoded_msg = quopri.decodestring(msg)
    # make the text more readable using regex
    decoded_msg = re.sub(regex_pattern, '\n', str(decoded_msg.decode('utf-8')))
    return decoded_msg


# gets the mail
def process_mailbox(M):
    rv, data = M.search(None, "ALL")

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("[-] Error getting message", num)
            return

    try:
        # get the message
        msg = email.message_from_bytes(data[0][1])

        # Now convert to local date-time
        local_date = convert_local_date(msg['Date'])
        local_date = local_date.strftime("%a, %d %b %Y %H:%M:%S")

        # Now decode the header
        hdr = email.header.make_header(
            email.header.decode_header(msg['Subject']))
        subject = str(hdr)

        # Now decode the msg
        decoded_msg = decode_message_to_str(msg)
        # Print the whole email
        print(f"From : {msg['From']}\nTo : {msg['To']}\nDate : {local_date}")
        print(f'Subject : {subject}')

        print(f'Message : {decoded_msg}')
    except IndexError:
        print("[-] No messages found!")
        pass
    except Exception as e:
        print(f"\nError : {e}\n")
        pass

# Checks for any new unseen mails and returns a count
def check_new_mails():
    return_code, mail_ids = mail.search(None, 'UnSeen')
    string_data = str(mail_ids[0])
    no_new_mails = "b''"
    counts = len(string_data.split(" ")) if string_data != no_new_mails else 0
    return counts

# Basic options 
def functions():
    print(f"You have {check_new_mails()} new emails")
    print("-----------------------------------")
    print("1 . Send mail")
    print("2 . Show last email")
    print("3 . Show all drafts")
    print("-----------------------------------")
    option = input("Choose an option : ")
    if option == '2':
        process_mailbox(mail)

# main function
def main():
    isEmpty = True
    try:
        # Get user creds
        while isEmpty:
            email = input("Enter email : ")
            pwd = getpass("Enter password : ")
            # validate user input
            if email != '' and pwd != '':
                isEmpty = False
            else:
                print("[-] Email or password is empty")

        # pass in the creds to login function
        if mail_login():
            rv, data = mail.select('Inbox')
            if rv == 'OK':
                print("[+] Processing mailbox...\n")

                functions()
                mail.close()
            else:
                print("[-] ERROR: Unable to open mailbox ", rv)
    except Exception as ex:
        print(f'[-] Error : {ex}')


# call the main function
if __name__ == '__main__':
    main()

# logsout after processesa re completed
logout()


# Content-Type: text/plain; charset="UTF-8"
