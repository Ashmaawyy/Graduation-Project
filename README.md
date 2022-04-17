# Welcome To Graduation Project : )

## To install required liberaries type in conda prompt: pip install -r requirements.txt

## Modules in our ETL

### The EmailHandler:  
It sends and recieves e-mails through a list of functions:

- send_email()
- attach_file()
- connect_to_ssl_server()

These are the functions used to send e-mails.

- recieve_emails_into_df()
- connect_to_imap_server()
- get_email_ids()
- create_messages_dict()

### The GoogleFormsHandler:  
It recieves Google Forms responces through two functoins:

- access_drive(), and
- read_form_responces()

### The EmailAnalyzer (In Development):  
It analyzes recieved emails.

### The GoogleFormsAnalyzer (In Development):  
It analyzes GoogleForm responses.
