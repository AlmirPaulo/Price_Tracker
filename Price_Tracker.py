from selenium import webdriver
from email.message import EmailMessage
import smtplib, time, os

#variables
url = 'https://www.amazon.com/AmazonBasics-Premium-Single-Monitor-Stand/dp/B00MIBN16O/ref=sr_1_1?dchild=1&keywords=amazonbasics&pf_rd_p=9349ffb9-3aaa-476f-8532-6a4a5c3da3e7&pf_rd_r=B862EJWHJFXBNT4G1K65&qid=1609360933&sr=8-1'
price_target = '121'
loop = True

driver_options = webdriver.FirefoxOptions()
driver_options.binary_location = os.environ.get("FIREFOX_BIN")
driver = webdriver.Firefox(executable_path=os.environ.get("GECKODRIVER"), firefox_options = driver_options)

sender = os.environ.get('SENDER')
receiver = os.environ.get('RECEIVER')
password = os.environ.get('PASSWORD')

#Test E-mail
email_test = EmailMessage()
email_test["Subject"] = 'Price Tracker Bot Test'
email_test["From"] = sender 
email_test["To"] = receiver
email_test.set_content("Hello! \n I am the Price Tracker Bot you hired! \n This is just a test email to check if it's all right. For now on, I will be tracking the price of the products you ask. When they were cheap enough I'll tell you! \n See you!")
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(sender, password)
    smtp.send_message(email_test)
    
#Email
email = EmailMessage()
email["Subject"] = 'Price Tracker Bot'
email["From"] = sender 
email["To"] = receiver
email.set_content("Hey! \n The product you are tracking get cheaper! \n Check it out: "+url)

#Email back
email_back = EmailMessage()
email_back["Subject"] = 'Price Tracker Bot'
email_back["From"] = sender 
email_back["To"] = sender
email_back.set_content("The bot work is finished for "+ receiver)

while loop == True:
    #scrap
    driver.get(url)
    price = driver.find_element_by_css_selector('#priceblock_ourprice')
#Send E-mail 
    #Attention to the price string!
    if int(price.text[1:3]) <= int(price_target):
        driver.close()
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sender, password)
            smtp.send_message(email)
            smtp.send_message(email_back)
        loop = False
    driver.close()
    time.sleep(3600)
