# Welcome To Graduation Project : )

## Modules in our ETL

### The EmailHandler:  
#### It sends and recieves e-mails through two sets of functions:

#### Functions used to send e-mails:
- send_email()
- attach_file()
- connect_to_ssl_server()

#### Functions used to recieve e-mails:
- recieve_emails_into_df()
- connect_to_imap_server()
- get_email_ids()
- create_messages_dict()

### The GoogleFormsHandler:  
#### It recieves Google Forms responces through two functoins:
- access_drive(),
- get_form_responces_df()

### The EmailAnalyzer (In Development):  
#### It analyzes recieved emails.

### The GoogleFormsAnalyzer (In Development):  
#### It analyzes GoogleForm responses.
