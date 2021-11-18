import smtplib
from email.mime.text import MIMEText
from datetime import date

def connect_to_SSL_server():
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

    connect_to_SSL_server()
    


def recieve_email():
