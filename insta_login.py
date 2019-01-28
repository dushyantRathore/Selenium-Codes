import time
import re
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

username = raw_input("Enter your fb email : ")
password = getpass.getpass("Enter your password : ")

driver = webdriver.Chrome("C:/Users/39400/Desktop/chromedriver") # Link to the downloaded chrome driver
driver.get("https://instagram.com/")  # URL for navigation
time.sleep(5)
elem = driver.find_element_by_xpath("//*[@class='_0mzm- sqdOP  L3NKy       ']")
elem.click()
time.sleep(5)
element_id = driver.find_element_by_id("email")
element_id.send_keys(username)
element_pass = driver.find_element_by_id("pass")
element_pass.send_keys(password)
element_btn = driver.find_element_by_id("loginbutton")
element_btn.click()
time.sleep(5)
elem_not_now_btn_1 = driver.find_element_by_xpath("//*[@class='_3m3RQ _7XMpj']")
elem_not_now_btn_1.click()
time.sleep(5)
elem_not_now_btn_2 = driver.find_element_by_xpath("//*[@class='aOOlW   HoLwm ']")
elem_not_now_btn_2.click()
driver.close()