import smtplib
from email.message import EmailMessage
from pathlib import Path  # os.path similar
from string import Template

html = Template(Path('index.html').read_text())
# For this test work I am turn ou Access for less secure apps on Gmail
email = EmailMessage()
email['from'] = 'Kiril'
email['to'] = 'for.services.it.t@gmail.com'
email['subject'] = 'Hello, it\'s me!'

email.set_content(html.substitute({'name': 'Jack'}), 'html')

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
    smtp.send_message(email)
    print('Yayyy!')
