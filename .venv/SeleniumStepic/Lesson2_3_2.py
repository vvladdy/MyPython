import time
import math
import decimal
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
    driver.get("http://suninjuly.github.io/redirect_accept.html")
    fly_link = driver.find_element(By.CSS_SELECTOR,
                                   'button[type="submit"]')
    fly_link.click()
    time.sleep(1)
    first_window = driver.window_handles[0]
    new_window = driver.window_handles[1]
    driver.switch_to.window(new_window)
    for_attr = driver.find_element(By.ID, 'input_value')
    x = int(for_attr.text)
    y = calc(x)
    answ_input = driver.find_element(By.ID, 'answer')
    answ_input.send_keys(y)
    submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit.click()
    allert = driver.switch_to.alert
    print(allert.text)
    time.sleep(2)
    text_al = str(allert.text).split(':')[-1]
    answer = decimal.Decimal(text_al)
    print(decimal.Decimal(text_al))
except Exception as err:
    print(err)
finally:
    time.sleep(1)
    driver.quit()