import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

API_KEY = '6b0b682c00a2658ebcbcda512cc346ab'

driver = webdriver.Chrome("C:/Users/39400/Desktop/chromedriver") # Link to the downloaded chrome driver
driver.get("https://www.google.com/recaptcha/api2/demo")  # URL for navigation

elem = driver.find_element_by_class_name("g-recaptcha")

# Get the current url
current_url = driver.current_url

# Get the site key
data_sitekey = elem.get_attribute("data-sitekey")

# Make the request to 2captcha endpoint to get the captcha ID
request_url = "http://2captcha.com/in.php?key=" + API_KEY + "&method=userrecaptcha&googlekey=" + data_sitekey + "&pageurl=" + current_url 
resp = requests.get(request_url)
captcha_id = resp.text.split("|")[1]

print("Captcha ID : " + captcha_id)

# Get the valid token using the capctha ID
fetch_url = "http://2captcha.com/res.php?key="+ API_KEY + "&action=get&id=" + captcha_id
recaptcha_answer = requests.get(fetch_url).text

while 'CAPCHA_NOT_READY' in recaptcha_answer:
    print (recaptcha_answer)  # debug
    time.sleep(5)
    recaptcha_answer = requests.get(fetch_url).text

recaptcha_answer = requests.get(fetch_url).text.split("|")[1]
print("Recaptcha Answer : " + recaptcha_answer)

elem = driver.find_element_by_xpath('//*[@id="g-recaptcha-response"]')
driver.execute_script('arguments[0].setAttribute("style", "width: 250px; height: 40px; border: 1px solid #c1c1c1; margin: 10px 25px; padding: 0px; resize: none; ");', elem) #unhide recaptcha response input
elem.send_keys(recaptcha_answer) # types recaptcha answer in the input
element = driver.find_element_by_id('g-recaptcha-response')

# Make the payload for the post data here, use something like mitmproxy or fiddler to see what is needed
payload = {
    'key': 'value',
    'gresponse': recaptcha_answer  # This is the response from 2captcha, which is needed for the post request to go through.
    }

# Send the post request to the url
response = requests.post(current_url, payload)
print(response.text)

driver.find_element_by_xpath("//input[@type='submit' and @value='Submit']").send_keys(Keys.ENTER)
time.sleep(5)
driver.close()