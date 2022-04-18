# pylint: disable=invalid-name
# pylint: disable=missing-module-docstring
# pylint: disable=import-error
# pylint: disable=wildcard-import
# pylint: disable=undefined-variable
import re
from email_handler import recieve_emails_into_df
from html.parser import HTMLParser

messages_df = recieve_emails_into_df()

class Parser(HTMLParser):
  # method to append the start tag to the list start_tags.
    def handle_starttag(self, tag, attrs):
        global start_tags
        start_tags.append(tag)
        # method to append the end tag to the list end_tags.
    def handle_endtag(self, tag):
        global end_tags
        end_tags.append(tag)
    # method to append the data between the tags to the list all_data.
    def handle_data(self, data):
        global all_data
        all_data.append(data)
    # method to append the comment to the list comments.
    def handle_comment(self, data):
        global comments
        comments.append(data)

start_tags = []
end_tags = []
all_data = []
comments = []
# Creating an instance of our class.
parser = Parser()
# Poviding the input.
for i in range(len(messages_df['body'])):
    parser.feed(str(messages_df['body'][i]))

for i in range(len(all_data)):
    all_data.append(re.sub(r'^\\r\\n *', '', all_data[i]))
