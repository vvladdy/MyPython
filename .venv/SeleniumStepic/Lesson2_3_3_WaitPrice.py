import time
import math
import decimal
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_service = Service(executable_path='c:/Users/User/PycharmProjects/chromedriver.exe')

driver = webdriver.Chrome(
    service=driver_service
)
# говорим WebDriver ждать все элементы в течение 5 секунд
driver.implicitly_wait(5)

def calc(x):
  return str(math.log(abs(12*math.sin(int(x)))))

try:
    driver.get('http://suninjuly.github.io/explicit_wait2.html')
    time.sleep(1)
    price = driver.find_element(By.ID, 'price').text
    # while price != '$100':
    #     price = driver.find_element(By.ID, 'price').text
    #     time.sleep(0.3)
    #     print(price)
    # print('Price')

    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element((By.ID, "price"), '100'))

    book = driver.find_element(By.ID, 'book')
    book.click()
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
    time.sleep(2)
    driver.quit()
