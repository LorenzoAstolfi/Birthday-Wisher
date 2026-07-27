##################### Extra Hard Starting Project ######################
import pandas as pd
import random
import pathlib
from datetime import datetime
import smtplib
import os

#TODO: 0. Get Email & Password
my_email = os.environ.get("MY_EMAIL")
my_pw = os.environ.get("MY_PASSWORD")

#TODO: 1. Update the birthdays.csv
date_list = pd.read_csv("birthdays.csv")
date_list = date_list.to_dict("records")

if not my_email or not my_pw:
    raise ValueError(
        "ERRORE: Credenziali vuote. Assicurati che MY_EMAIL e MY_PASSWORD siano configurati nei Secrets di GitHub."
    )

#TODO: 2. Check if today matches a birthday in the birthdays.csv
def check_birthday():
    now = datetime.now()
    birthdays = []
    for date in date_list:
        if date['month'] == now.month and date['day'] == now.day:
            birthdays.append(date)
    return birthdays

todays_birthdays = check_birthday()

#TODO: 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
if todays_birthdays:
    print(f"Trovati {len(todays_birthdays)} compleanni oggi! Connessione a Gmail...")

    #TODO: Open connection SMTP a single time
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(my_email, my_pw)

        for date_birthday in todays_birthdays:
            template_path = (
                f"letter_templates/letter_{random.randint(1, 3)}.txt"
            )
            msg_email = pathlib.Path(template_path).read_text()
            msg_email = msg_email.replace("[NAME]", date_birthday["name"])

            #TODO: Sending email
            connection.sendmail(
                from_addr=my_email,
                to_addrs=date_birthday["email"],
                msg=f"To: {date_birthday['email']}\nSubject: Happy Birthday!\n\n{msg_email}",
            )
            print(f"Email inviata con successo a {date_birthday['name']}!")
else:
    print("Nessun compleanno trovato per la data di oggi.")
