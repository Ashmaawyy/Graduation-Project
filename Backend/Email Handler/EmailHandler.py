import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import datetime
import email
import imaplib
import os

def send_email(subject = '', from_addr = '', to_addrs = [], filesnames = []):

    message = MIMEText('This Message is sent to you from The QC System :)')
    message['subject'] = subject 
    message['from'] = from_addr
    message['to'] = COMMASPACE.join(to_addrs)

    if filesnames != []:
        attach_files(subject , from_addr, to_addrs, filesnames)

    connect_to_ssl_server(from_addr, to_addrs, message)

def attach_files(subject , from_addr, to_addrs, filesnames):

    message = MIMEMultipart()
    message['From'] = from_addr
    message['To'] = COMMASPACE.join(to_addrs)
    message['Date'] = formatdate(localtime = True)
    message['Subject'] = subject
    message.attach(MIMEText(message))

    for path in filesnames:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path(path).name))
        message.attach(part)

def connect_to_ssl_server(from_addr, to_addrs, message):
     # connect with Google's servers
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465

    # use username or email to log in
    username = 'mohamed204798@gmail.com'
    password = 'kerwnobnjdxkroah'

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    # to interact with the server, first we log in
    server.login(username, password)
    # and then we send the message
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()

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
def search(key, value, mail):

    result, data = mail.search(None, key, '"{}"'.format(value))
    return data

# Function to get the list of emails under this label
def get_emails(result_bytes, mail):

    msgs = [] # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        msgs.append(data)
 
    return msgs

def recieve_email():

    mail = connect_to_imap_server()
    msgs = get_emails(search('FROM', 'ANOTHER_GMAIL_ADDRESS', mail), mail)
    
def clean_bloated_mailbox():

    imaplib._MAXLINE = 1000000

    mail = connect_to_imap_server()
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


send_email('Testing' ,'mohamed204798@gmail.com', ['mona.arafat71@gmail.com'], ['Test.xls'])