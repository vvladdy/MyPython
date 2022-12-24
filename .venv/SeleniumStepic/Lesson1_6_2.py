import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import math

driver_service = Service(executable_path='c:/Users/User/PycharmProjects/chromedriver.exe')


driver = webdriver.Chrome(
    service=driver_service
)

try:
    driver.get('http://suninjuly.github.io/find_link_text')
    text = str(math.ceil(math.pow(math.pi, math.e)*10000))
    link = driver.find_element(By.PARTIAL_LINK_TEXT, f'{text}')
    link.click()
    time.sleep(0.5)
    print(driver.page_source)
    input1 = driver.find_element(By.TAG_NAME, 'input')
    input1.send_keys('Ivan')
    input2 = driver.find_element(By.NAME, 'last_name')
    input2.send_keys('Ivan')
    input3 = driver.find_element(By.CLASS_NAME, 'form-control.city')
    input3.send_keys('Kiev')
    input4 = driver.find_element(By.ID, 'country')
    input4.send_keys('Ukraine')
    button = driver.find_element(By.CLASS_NAME, "btn.btn-default")
    button.click()
except Exception as err:
    print(err)
finally:
    time.sleep(30)
    driver.quit()
    driver.close()




