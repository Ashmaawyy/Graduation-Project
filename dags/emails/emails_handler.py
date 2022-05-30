from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pandas import read_csv, DataFrame
from os import getcwd
import smtplib, email, imaplib, traceback#, mysql.connector

admin_creds = read_csv(getcwd() + '/airflow/dags/admin_creds.csv')
from_addr = admin_creds['value'][0]

def send_email(subject, to_addrs, message_text, files_names = None):
    """
    Sends e-mails
    subject -> str
    to_addrs -> []
    message_text -> str
    filesnames -> []
    """
    message = email.mime.text.MIMEText(message_text)
    message['subject'] = subject
    message['from'] = from_addr
    message['to'] = email.utils.COMMASPACE.join(to_addrs)

    if files_names is not None:
        message = attach_files(subject , to_addrs, message_text, files_names)

    connect_to_ssl_server(to_addrs, message)
    print('Message sent successfully :)')

def attach_files(subject , to_addrs, message_text, files_names):
    """
    Attaches files for outgoing e-mails
    subject -> str
    to_addrs -> []
    filesnames -> []
    """
    message_attached = email.mime.multipart.MIMEMultipart()
    message_attached['From'] = from_addr
    message_attached['To'] = email.utils.COMMASPACE.join(to_addrs)
    message_attached['Date'] = email.utils.formatdate(localtime = True)
    message_attached['Subject'] = subject
    message_attached.attach(email.mime.text.MIMEText(message_text))

    for path in files_names:
        part = email.mime.base.MIMEBase('application', "octet-stream")
        with open(path, 'r') as file:
            part.set_payload(file.read())
        email.encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path(path).name))
        message_attached.attach(part)
    return message_attached

def connect_to_ssl_server(to_addrs, message):
    """
    Handels e-mail sending protocols
    to_addrs -> []
    message -> MIMEmessage object
    """
     # connect with Google's servers
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465

    # use username or email to log in
    username = admin_creds['value'][0]
    password = admin_creds['value'][1]

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    # to interact with the server, first we log in
    server.login(username, password)
    # and then we send the message
    server.sendmail(username, to_addrs, message.as_string())
    server.quit()

def recieve_emails_into_df():
    """
    Recieves and saves messages into a pandas dataframe for analysis,
    returns the created df
    """
    try:
        mail = connect_to_imap_server()
        latest_email_id, first_email_id = get_email_ids(mail)
        messages_df = DataFrame.from_dict(
            create_messages_dict(latest_email_id, first_email_id, mail), orient = 'columns')
        print('Messages saved into a dataframe successfully :)')

        return messages_df
    except Exception as e:
        traceback.print_exc()
        return str(e)

def connect_to_imap_server():
    """
    Handles recieve protocols, returns mail -> IMAP object
    """
    username = admin_creds['value'][0]
    password = admin_creds['value'][1]
    server = 'imap.gmail.com'

    # connect to the server and go to its inbox
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    mail.select('Inbox')
    return mail

def get_email_ids(mail):
    """
    Returns e-mail id's to determin lengh of list to search within
    mail -> IMAP object
    """
    data = mail.search(None, 'ALL')
    mail_ids = data[1]
    id_list = mail_ids[0].split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    return latest_email_id, first_email_id

def create_messages_dict(latest_email_id, first_email_id, mail):
    """
    Creates messages dictionary in order to be made into a dataframe
    latest_email_id, first_email_id -> int
    mail -> IMAP object
    """
    messages_dict = {'subject': [], 'from': [], 'body': []}

    for i in range(latest_email_id, first_email_id, -1):
        data = mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1],'utf-8'))
                messages_dict['subject'].append(msg['subject'])
                messages_dict['from'].append(msg['from'])
                messages_dict['body'].append(msg.get_payload(decode = True))
    return messages_dict

teaching_staff_emails = [
    'SEHAM.MOAWAD@eng.modern-academy.edu.eg',
    'SABRY.AMOATY@eng.modern-academy.edu.eg',
    'muhammad.alashmaawy@gmail.com']

#students_emails = [
#   'al_ashmawy@outlook.com',
#   'medo333best@gmail.com']

doctor_submission_message = '''This Message is sent to you by the QC Department to remind you to submit the required docs : )
                                \nSincerly,\nAshmawy ©'''

student_survey_message = '''This survey is sent to you from the Quality Control department to insure the quality of the education you recieve.
                            \nhttps://forms.gle/U585CaruQtVMFXoE7
                            
                            \nSincerly,\nAshmawy ©'''

with DAG(dag_id = "emails_handler",
         start_date = datetime(2022,5,30),
         schedule_interval = "@daily",
         catchup = False) as dag:

        doctor_submission = PythonOperator(
            task_id = "send_submission_email_to_doctors",
            python_callable = send_email,
            op_kwargs = {
                'subject': "Annual docs subbmission email for the teaching staff",
                'to_addrs': teaching_staff_emails,
                'message_text': doctor_submission_message }
                )

        student_survey = PythonOperator(
            task_id = 'send_survey_to_students',
            python_callable = send_email,
            op_kwargs = {
                'subject' : 'A survey to insure education quality for Modern Academy Maadi Students',
                'to_addrs': teaching_staff_emails,
                'message_text': student_survey_message }
        )

student_survey
#doctor_submission