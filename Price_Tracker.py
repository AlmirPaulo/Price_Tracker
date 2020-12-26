from email.message import EmailMessage
from requests_html import HTMLSession
import smtplib, time

#variables
url = ''
loop = True
price_target = ''
sender = open('note_sender', 'r').read()
receiver = open('note_receiver', 'r').read()
password = open('note_password', 'r').read()

s = HTMLSession()
r = s.get(url)
r.html.render(sleep=1)

while loop == True:
    #scrap
    price = r.html.find('', first=True)

    #Send E-mail 
        #Attention to the price string!
    if float(price.text[3:6]) <= float(price_target):
        email = EmailMessage()
        email["Subject"] = 'Bot Test'
        email["From"] = sender 
        email["To"] = receiver
        email.set_content('Check it out!\n' + url)
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(sender, password)

            smtp.send_message(email)
            loop = False
    time.sleep(3600)
