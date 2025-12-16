#import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
#start the selenium browser session
driver = webdriver.Chrome()
#load desired pages in the browser
# time.sleep(5)
driver.get("https://www.flipkart.com/")
print("Initial Page Title:", driver.title)
#define wait stategy -- set one time in the application 
driver.implicitly_wait(5)

#acccess the controls on the page 
# time.sleep(5)
search_box = driver.find_element(By.NAME, "q")
#interact with control
for ch in "T shirts for Women":
    search_box.send_keys(ch)
    time.sleep(0.2) 
#search_box.send_keys("T shirts for Women")
search_box.send_keys(Keys.RETURN)


#wait for the result
print("Later Page Title:", driver.title)

# stop the sesssion
time.sleep(10)
driver.quit()