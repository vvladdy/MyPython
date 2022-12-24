import time
import math

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver_service = Service(executable_path='c:/Users/User/PycharmProjects/chromedriver.exe')

driver = webdriver.Chrome(
    service=driver_service
)

def calc(x):
  return str(math.log(abs(12*math.sin(int(x)))))

try:
    driver.get("http://suninjuly.github.io/get_attribute.html")
    for_attr = driver.find_element(By.ID, 'treasure')
    x_el = for_attr.get_attribute('valuex')
    x = int(x_el)
    y = calc(x)
    answ_input = driver.find_element(By.ID, 'answer')
    answ_input.send_keys(y)
    chekbox = driver.find_element(By.ID, 'robotCheckbox')
    chekbox.click()
    time.sleep(0.5)
    radiobutton = driver.find_element(By.ID, 'robotsRule')
    radiobutton.click()
    submit = driver.find_element(By.CLASS_NAME, 'btn.btn-default')
    submit.click()
except Exception as err:
    print(err)
finally:
    time.sleep(6)
    driver.quit()
