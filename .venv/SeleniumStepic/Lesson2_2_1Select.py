import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver_service = Service(
    executable_path='c:/Users/User/PycharmProjects/chromedriver.exe'
)

driver = webdriver.Chrome(service=driver_service)

def calculate(a, b, sign):
    if sign == '+':
        return a+b
    elif sign == '*':
        return a*b
    elif sign == '-':
        return a*b
    elif sign == '/':
        return a*b

try:
    driver.get('https://suninjuly.github.io/selects1.html')
    a = driver.find_element(By.ID, 'num1').text
    b = driver.find_element(By.ID, 'num2').text
    sign = driver.find_element(By.XPATH,
                            '/html/body/div[1]/form/h2/span[3]').text
    print(int(a), sign, int(b))
    result = calculate(int(a), int(b), sign)
    print(result)
    dropdown = driver.find_element(By.ID, 'dropdown')
    dropdown.click()
    select = Select(driver.find_element(By.TAG_NAME, 'select'))
    choice = select.select_by_value(f'{result}')
    submit = driver.find_element(By.CLASS_NAME, 'btn.btn-default')
    submit.click()
except Exception as err:
    print(err)
finally:
    time.sleep(15)
    driver.quit()