import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver_service = Service(executable_path='c:/Users/User/PycharmProjects/chromedriver.exe')


driver = webdriver.Chrome(
    service=driver_service
)

try:
    driver.get("http://suninjuly.github.io/find_xpath_form")
    button = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[6]/button[3]')
    print(driver.page_source)
    time.sleep(1)
    input1 = driver.find_element(By.TAG_NAME, 'input')
    input1.send_keys('Ivan')
    input2 = driver.find_element(By.NAME, 'last_name')
    input2.send_keys('Ivan')
    input3 = driver.find_element(By.CLASS_NAME, 'form-control.city')
    input3.send_keys('Kiev')
    input4 = driver.find_element(By.ID, 'country')
    input4.send_keys('Ukraine')
    button.click()
except Exception as err:
    print(err)
finally:
    time.sleep(30)
    driver.quit()
    driver.close()
