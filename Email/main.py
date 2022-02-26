import pprint
import re
import smtplib
from email.message import EmailMessage
from pathlib import Path  # os.path similar
from random import randint
from string import Template
from time import sleep

html = Template(Path('index.html').read_text())
# For this test work I am turn ou Access for less secure apps on Gmail
email = EmailMessage()
email['from'] = 'Ua'
email['to'] = 'for.services.it.t@gmail.com'
email['subject'] = 'Hello, it\'s me!'

email.set_content(html.substitute({'name': 'Jack'}), 'html')

# You can just convert Ctrl + C, Ctrl + V, to line, that's all.
emails_in_text = """
should we use regex more often? let me know at  321dsasdsa@dasdsa.com.lol or dadaads@dsdds.com
"""

found_emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', emails_in_text)

d = {}
with open('email.properties', mode='r') as my_file:
    for line in my_file:
        (key, value) = line.split('=')
        value = value.strip('\n')
        d[key] = value

with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(d['login'], d['password'])
    for item in match:
        try:
            email['to'] = item
            smtp.send_message(email)
            sleep(randint(5, 10))
        except Exception as ex:
            pprint.pprint(ex)
    print('Yayyy!')
