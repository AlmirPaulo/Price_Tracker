#! env/bin/python3
from selenium import webdriver
from email.message import EmailMessage
import smtplib, time

#variables
url = open('product', 'r').read()
price_target = open('price_target', 'r').read()
loop = True

driver_path = open('geckodriver', 'r').read()
sender = open('sender', 'r').read()
receiver = open('receiver', 'r').read()
password = open('password', 'r').read()

# #Test E-mail
# email_test = EmailMessage()
# email_test["Subject"] = 'Price Tracker Bot Test'
# email_test["From"] = sender 
# email_test["To"] = receiver
# email_test.set_content("Hello! \n\n I am the Price Tracker Bot you hired! \n This is just a test email to check if it's all right. For now on, I will be tracking the price of the products you ask. When they were cheap enough I'll tell you! \n\n See you!")
# with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.ehlo()
#     smtp.login(sender, password)
#     smtp.send_message(email_test)
    
#Email
email = EmailMessage()
email["Subject"] = 'Price Tracker Bot'
email["From"] = sender 
email["To"] = receiver
email.set_content("Hey! \n\n The product you are tracking get cheaper! \n\n Check it out: "+url)

#Email back
email_back = EmailMessage()
email_back["Subject"] = 'Price Tracker Bot'
email_back["From"] = sender 
email_back["To"] = sender
email_back.set_content("The bot work is finished for "+ receiver)

while loop == True:
    #scrap 
    #Need Firefox in the server!
    driver_options = webdriver.FirefoxOptions()
    driver_options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path=driver_path, firefox_options=driver_options)
    driver.get(url)
    price = driver.find_element_by_css_selector('#priceblock_ourprice')
#Send E-mail 
    #Attention to the price string!
    if float(price.text[1:9]) <= float(price_target):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sender, password)
            smtp.send_message(email)
            smtp.send_message(email_back)
        loop = False
    driver.close()
    time.sleep(60)
