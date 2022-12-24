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

def calculate(x):
    return str(math.log(abs(12 * math.sin(int(x)))))


try:
    driver.get("http://suninjuly.github.io/alert_accept.html")
    submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit.click()
    allert = driver.switch_to.alert
    allert.accept()
    x = int(driver.find_element(By.ID, 'input_value').text)
    y = calculate(x)
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
    time.sleep(10)
    driver.quit()