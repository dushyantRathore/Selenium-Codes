from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from selenium import webdriver
import requests
import time
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

xlogbutton = '//*[@id="root"]/div/div[2]/nav/div/div[5]/div/div[1]/button'
xuser = '/html/body/div[2]/div/div/div/div[1]/form/div/div[1]/div/div[2]/input'
xpass = 'html/body/div[2]/div/div/div/div[1]/form/div/div[2]/div/div[1]/div[2]/input'
xlogin = '/html/body/div[2]/div/div/div/div[1]/form/div/div[3]/button'
recaptcha = '//*[@id="recaptcha-element-container"]/div/div/iframe'
dest = "https://www.twitch.tv/ninja"
PROXY = "185.202.104.208:4451"
Proxies =""
linenumber = 0
count = 0
temp = ""
accNumber = 0
logLineCount = 0
proxynumber = 0
API_KEY = '6b0b682c00a2658ebcbcda512cc346ab'
site_key=''
amount=10
username = "pareszk"
password = "TwitchPrimes2910@"
chromeoptions = ChromeOptions()
 
def login():
    global driver, proxynumber  
    proxynumber += 1
    driver = webdriver.Chrome("C:/Users/39400/Desktop/chromedriver", options=chromeoptions)
    driver.delete_all_cookies()
    driver.get(dest)  
    if(count >= amount):
            driver.close()
            driver.quit()
            quit()
    else:
        try:
            element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, xlogbutton))
                )
            driver.find_element(By.XPATH, xlogbutton).click()
        except TimeoutException:
            print("Couldn't find LOG IN BUTTON")
        except WebDriverException:
            login()    
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xuser))
                )
            driver.find_element(By.XPATH, xuser).send_keys(username)
        except TimeoutException:
            print("Timed out -> Input username")
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpass))
                )
            driver.find_element(By.XPATH, xpass).send_keys(password)
            driver.find_element(By.XPATH, xpass).send_keys(Keys.ENTER)
            time.sleep(15)
        except TimeoutException:          
            print("Timed out [input pass]")

def getSiteKey():  # Gets the SITE_KEY and sets the variable
    global recaptcha, site_key
    element = driver.find_element(By.XPATH, recaptcha)
    d = element.get_attribute("src")
    trash, rest = d.split("&k=")
    site_key, trash = rest.split("&co")
    print("Site key : " + site_key)
    return site_key


def handleCaptcha():
    global API_KEY, site_key, dest, answer
    s = requests.Session()
    captcha_id = s.post("http://2captcha.com/in.php?key=" + API_KEY + "&method=userrecaptcha&googlekey=" + site_key + "&pageurl=" + dest).text.split('|')[1]
    print ("Request returned captcha ID:" + captcha_id)
    recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
            print (recaptcha_answer)  # debug
            time.sleep(5)
            recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text      
    recaptcha_answer = recaptcha_answer.split('|')[1]
    print("Recaptcha answer is: " + recaptcha_answer)
    answer = recaptcha_answer
 
login()
getSiteKey()
handleCaptcha()
 
elem = driver.find_element_by_xpath('//*[@id="g-recaptcha-response"]')
driver.execute_script('arguments[0].setAttribute("style", "width: 250px; height: 40px; border: 1px solid #c1c1c1; margin: 10px 25px; padding: 0px; resize: none; ");', elem) #unhide recaptcha response input
elem.send_keys(answer) # types recaptcha answer in the input

element = driver.find_element_by_id('g-recaptcha-response')

# Make the payload for the post data here, use something like mitmproxy or fiddler to see what is needed
payload = {
    'key': 'value',
    'gresponse': answer  # This is the response from 2captcha, which is needed for the post request to go through.
    }

current_url = driver.current_url

# Send the post request to the url
response = requests.post(current_url, payload)
print(response.text)

elem = driver.find_element_by_xpath("//*[@class='tw-interactive tw-button tw-button--disabled tw-button--full-width']")
driver.execute_script("arguments[0].setAttribute('class','tw-interactive tw-button tw-button--full-width')", elem)
elem = driver.find_element_by_xpath("//*[@class='tw-interactive tw-button tw-button--full-width']")
driver.execute_script("arguments[0].removeAttribute('disabled')", elem)
print(elem.is_enabled())
elem.send_keys(Keys.ENTER)
elem.click()
