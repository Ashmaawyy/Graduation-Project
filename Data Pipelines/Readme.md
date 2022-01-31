# The four modules in our ETL

1. The EmailHandler:  
It sends and recieves e-mails through a list of functions:

- send_email()
- attach_file()
- connect_to_ssl_server()

These are the functions used to send e-mails.

- recieve_emails_into_df()
- connect_to_imap_server()
- get_email_ids()
- create_messages_dict()

2. The GoogleFormsHandler:  
It recieves Google Forms responces through two functoins:

- access_drive() and
- read_form_responces()

3. The EmailAnalyzer (In Development):  
It analyzes the recieved emails to perform certain actions depending on the output data of the analysis.

4. The GoogleFormsAnalyzer (In Development):  
It analyzes the responces and comeup with certain insights and generates a brief report with theses insghts and the report is added to each subject.
