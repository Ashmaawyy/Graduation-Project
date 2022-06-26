# Welcome To My Graduation Project : )

## *A piece of art for managing quality assurance department in Modern Academy (Data wise of course).*

Technical Tools Used:

- Apache Airflow.
- SSL Protocols.
- IMAP Protocols.
- GoogleDrive API

## Modules in our ETL

### The emails_handler()

### It sends and recieves e-mails through two sets of functions

#### Functions used to send e-mails

- send_email()
- attach_file()
- connect_to_ssl_server()

#### Functions used to recieve e-mails

- recieve_emails_into_df()
- connect_to_imap_server()
- get_email_ids()
- create_messages_dict()

### The google_forms_handler()

#### It recieves google form responces through these functoins

- get_drive_access()
- download_form_responses_excel()
- get_form_responces_df()

### The emails_analyzer (In Development)

- #### It analyzes the content of recieved emails

- #### It triggers the emails_handler to respond to the emails depending on the content (needs to be developed)

### The google_forms_analyzer (In Development)

- #### It analyzes the survey responses and comes up with insights from survey response data

- #### It analyzes google form responses

- #### It triggers the emails_handler to send a congratulations or warrant emails to professors depending on the insights from survey responses (needs to be developed)

- #### It can diffrentiate between fake (random) survey responses and honest (real) ones (needs to be developed)
