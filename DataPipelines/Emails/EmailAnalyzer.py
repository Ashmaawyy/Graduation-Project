# pylint: disable=invalid-name
# pylint: disable=missing-module-docstring
from EmailHandler import recieve_emails_into_df

messages_df = recieve_emails_into_df()
print(messages_df)
