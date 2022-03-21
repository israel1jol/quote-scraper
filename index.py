import requests
from bs4 import BeautifulSoup
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
now = datetime.datetime.now()

categories = ["Age", "Experience", "Religion", "Knowledge", "Leadership", "Respect", "Science", "Smile", "Society", "Space", "Sports", "Strength", "Success", "Teen", "Technology", "Truth", "Hope"]


def main():
    command = sys.argv[1]
    resolve_command(command)


def resolve_command(cmd):
    if(cmd == "-h" or cmd == "help" or cmd == "c"):
        print("Here are a list of categories")
        for i in range(len(categories)):
            print(categories[i])
    elif(cmd == "-g" or cmd == "get"):
        topic = sys.argv[2]
        resolve_category(topic)

def resolve_category(topic):
    flag = False
    cat=""
    for category in categories:
        if(category == topic.capitalize()):
            flag = True
            cat=category
            break
    if(flag):
        fetch_data(cat)
    else:
        print("Category not available")
    

def fetch_data(topic):
    body = "<h2>Here are some insightful Quotes on "+topic+"</h2><br><hr><br>"
    print("Fetching data."+"\n"+"Please Wait...")
    res = requests.get("https://www.brainyquote.com/topics/"+topic.lower()+"-quotes")
    data = res.content
    soup = BeautifulSoup(data, "html.parser")
    for i, quote in enumerate(soup.find_all("div", {"class":"grid-item qb clearfix bqQt"})):
        body +="<p>Quote " + str(i+1) + ": " + " ".join(quote.text.strip("\n\n").split("\n\n")) + "</p><br>"

    print("Data fetched successfully")
    sendmail(body, topic)


def sendmail(mail_body, mail_topic):
    FROM = os.getenv("FROM")
    TO = os.getenv("TO")
    PASS = os.getenv("PASS")
    HOST = "smtp.gmail.com"

    print("Sending mail...")
    mail = MIMEMultipart()
    mail["Subject"] = "Quotes for " + mail_topic + " on " + str(now)
    mail["From"] = FROM
    mail["To"] = TO
    mail.attach(MIMEText(mail_body, "html"))

    transport = smtplib.SMTP_SSL(HOST, 465)
    transport.set_debuglevel(0)
    transport.ehlo()
    transport.login(FROM, PASS)
    transport.sendmail(FROM, TO, mail.as_string())

    print("Mail sent, check your inbox.")



if __name__ == "__main__":
    main()