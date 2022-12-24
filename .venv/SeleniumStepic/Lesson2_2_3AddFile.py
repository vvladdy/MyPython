import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver_service = Service(executable_path='c:/Users/User/PycharmProjects/chromedriver.exe')

driver = webdriver.Chrome(
    service=driver_service
)


current_dir = os.path.dirname('D:/MyPythonFolder/MyPython/.venv/Parsers/Files/')
file_path = os.path.join(current_dir, 'log.txt')
# os.startfile(file_path)

try:
    driver.get("http://suninjuly.github.io/file_input.html")
    input1 = driver.find_element(By.CSS_SELECTOR,
                                'input[placeholder="Enter first name"')
    input1.send_keys('Ivan')
    input2 = driver.find_element(By.CSS_SELECTOR,
                                 '[placeholder ~= "last"]')
    input2.send_keys('Ivanov')
    input_email = driver.find_element(By.NAME, 'email')
    input_email.send_keys('Ivanov@gmail.com')
    add_file = driver.find_element(By.ID, 'file')
    add_file.send_keys(file_path)
    submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit.click()
except Exception as err:
    print(err)
finally:
    time.sleep(10)
    driver.quit()