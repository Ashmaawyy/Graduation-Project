import smtplib
from email.mime.text import MIMEText
from datetime import date
import email
import imaplib

def connect_to_ssl_server():
     # connect with Google's servers
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465

    # use username or email to log in
    username = 'username@gmail.com'
    password = 'password'

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    # to interact with the server, first we log in
    server.starttls() # Enable Security
    server.login(username, password)
    # and then we send the message
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()

def send_email(subject, from_addr, to_addrs, filename = ''):

    message = MIMEText('This Message is sent to you from The QC System :)' + datetime.now())
    message['subject'] = subject 
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)

    connect_to_ssl_server()

def connect_to_imap_server():

    EMAIL = 'mymail@mail.com'
    PASSWORD = 'password'
    SERVER = 'imap.gmail.com'

    # connect to the server and go to its inbox
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('Inbox')
    return mail

# Function to extract body-part of mail   
def get_body(msg):

    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

# Function to search for a key value pair
def search(key, value):

    con = connect_to_imap_server()

    result, data = con.search(None, key, '"{}"'.format(value))
    return data

# Function to get the list of emails under this label
def get_emails(result_bytes):

    msgs = [] # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
 
    return msgs

def recieve_email():

    mail = connect_to_imap_server()
    msgs = get_emails(search('FROM', 'ANOTHER_GMAIL_ADDRESS'))
    

def clean_bloated_mailbox():

    imaplib._MAXLINE = 1000000

    EMAIL = 'mymail@gmail.com'
    PASSWORD = 'password'
    SERVER = 'imap.gmail.com'

    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    # select the box you want to clean
    mail.select('bloated_box')

    status, search_data = mail.search(None, 'ALL')

    mail_ids = []

    for block in search_data:
        mail_ids += block.split()

    # define the range for the operation
    start = mail_ids[0].decode()
    end = mail_ids[-1].decode()

    # move the emails to the trash
    # this step is Gmail specific because
    # it doesn't allow excluding messages
    # outside the trash
    mail.store(f'{start}:{end}'.encode(), '+X-GM-LABELS', '\\Trash')

    # access the Gmail trash
    mail.select('[Gmail]/Trash')
    # mark the emails to be deleted
    mail.store("1:*", '+FLAGS', '\\Deleted')

    # remove permanently the emails
    mail.expunge()

    # close the mailboxes
    mail.close()
    # close the connection
    mail.logout()


