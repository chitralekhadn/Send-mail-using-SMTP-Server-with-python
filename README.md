# Send-mail-using-SMTP-Server-with-python
Problem Statement:
    Create a zip file and send mail using SMTP server in python.

Requirement:
Code is written in Python 3

config.ini:
Update the sender_id and password from which we have to send mail
Update the other values like name_of_destination_archive

encrypt1.py:
Run the script encrypt1.py first so that sender_id and password will get encrypted.

mail.py:
Run the main script mail.py to send mail.
Enter the arguments like --reciepient to whom we have to send mail, --subject, and --directory_of_files whichone we have to zip and attach to mail.
