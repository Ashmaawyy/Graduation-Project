FROM python:latest
RUN apt-get update
COPY mnt/Learning/Graduation-Project/requirements.txt /
RUN pip3 install -r requirements.txt
ARG src="admin creds.csv"
ARG target="/"
COPY ${src} ${target}
RUN chmod 400 "admin creds.csv"
COPY ./dags/emails/email_analyzer.py /
COPY ./dags/emails/email_handler.py /
CMD [ "python", "./email_analyzer.py"]
