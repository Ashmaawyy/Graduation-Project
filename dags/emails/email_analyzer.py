# pylint: disable=invalid-name
# pylint: disable=missing-module-docstring
# pylint: disable=import-error
# pylint: disable=wildcard-import
# pylint: disable=undefined-variable
from email_handler import recieve_emails_into_df
from html.parser import HTMLParser

messages_df = recieve_emails_into_df()

class Parser(HTMLParser):
    '''
    A class that parses HTML junk :)
    '''
    # method to append the data between the tags to the list all_data.
    def handle_data(self, data):
        global all_data
        all_data.append(data)
    # method to append the comment to the list comments.
    def handle_comment(self, data):
        global comments
        comments.append(data)

all_data = []
comments = []
# Creating an instance of our class.
parser = Parser()
# Poviding the input.
for i in range(len(messages_df['body'])):
    parser.feed(str(messages_df['body'][i]))
