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
import traceback
import pandas as pd

def send_email(subject, from_addr, to_addrs, filesnames):
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
    username = 'user@gmail.com'
    password = '****************'

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    # to interact with the server, first we log in
    server.login(username, password)
    # and then we send the message
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()

def recieve_emails_into_df():
    try:
        mail = connect_to_imap_server()
        latest_email_id, first_email_id = get_email_ids(mail)
        messages_df = pd.DataFrame.from_dict(create_messages_dict(latest_email_id, first_email_id, mail), orient = 'columns')
        print('Messages saved to dataframe successfully :)')

        return messages_df
            
    except Exception as e:
        traceback.print_exc() 
        print(str(e))

def connect_to_imap_server():
    EMAIL = 'user@gmail.com'
    PASSWORD = '**************'
    SERVER = 'imap.gmail.com'

    # connect to the server and go to its inbox
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('Inbox')
    return mail

def get_email_ids(mail):
    data = mail.search(None, 'SENTON 23-Nov-2021')
    mail_ids = data[1]
    id_list = mail_ids[0].split()   
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    return latest_email_id, first_email_id
   
def create_messages_dict(latest_email_id, first_email_id, mail):
    messages_dict = {'Subject': [], 'From': []}

    for i in range(latest_email_id, first_email_id, -1):
        data = mail.fetch(str(i), '(RFC822)' )
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1],'utf-8'))
                messages_dict['Subject'].append(msg['subject'])
                messages_dict['From'].append(msg['from'])
                #messages_dict['Body'].append(get_body(msg))
    return messages_dict

def get_body(email_contents):
    message = email.message_from_string(email_contents)
    for payload in message.get_payload():
        return payload.get_payload()
