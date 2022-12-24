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
    driver.get("http://SunInJuly.github.io/execute_script.html")
    for_attr = driver.find_element(By.ID, 'input_value')
    x = int(for_attr.text)
    y = calc(x)
    answ_input = driver.find_element(By.ID, 'answer')
    answ_input.send_keys(y)
    driver.execute_script('window.scrollBy(0, 100);')
    chekbox = driver.find_element(By.ID, 'robotCheckbox')
    chekbox.click()
    driver.execute_script('window.scrollBy(0, 100);')
    time.sleep(0.2)
    radiobutton = driver.find_element(By.ID, 'robotsRule')
    radiobutton.click()
    submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit.click()
except Exception as err:
    print(err)
finally:
    time.sleep(6)
    driver.quit()