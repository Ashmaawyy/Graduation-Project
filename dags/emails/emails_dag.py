from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from emails.email_handler import send_email

teaching_staff_emails = ["SEHAM.MOAWAD@eng.modern-academy.edu.eg",
"SABRY.AMOATY@eng.modern-academy.edu.eg"]
message_text = '''This Message is sent to you by the QC Department
    to submit the required docs : )
    \n Sincerly, \n Ashmawy ©'''
with DAG(dag_id="emails_dag",
         start_date = datetime(2023,7,1),
         schedule_interval = "@yearly",
         catchup=False) as dag:

         task1 = PythonOperator(
             task_id = "send_subbmission_email_to_doctors",
             python_callable = send_email(
                 "Annual docs subbmission email for the teaching staff",
                 teaching_staff_emails, message_text))

task1