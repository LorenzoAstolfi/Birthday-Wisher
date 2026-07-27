##################### Extra Hard Starting Project ######################
import pandas as pd
import random
import pathlib
from datetime import datetime
import smtplib
import os

#TODO: get Email and Password from external environment
my_email = os.environ.get("MY_EMAIL")
my_pw = os.envin.get("MY_PASSWORD")

#TODO: 1. Update the birthdays.csv
date_list = pd.read_csv("birthdays.csv")
date_list = date_list.to_dict("records")

#TODO: 2. Check if today matches a birthday in the birthdays.csv
def check_birthday():
    now = datetime.now()
    birthdays = []
    for date in date_list:
        if date['month'] == now.month and date['day'] == now.day:
            birthdays.append(date)
    return birthdays

#TODO: 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
for date_birthday in check_birthday():
    if date_birthday:
        msg_email = pathlib.Path(f"letter_templates/letter_{random.randint(1, 3)}.txt").read_text()
        msg_email = msg_email.replace("[NAME]", date_birthday['name'])

        #TODO: 4. Send the letter generated in step 3 to that person's email address.
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(my_email, my_pw)
            connection.sendmail(from_addr=my_email, to_addrs=date_birthday['email'], msg=f"Subject: Happy Birthday\n\n{msg_email}")
