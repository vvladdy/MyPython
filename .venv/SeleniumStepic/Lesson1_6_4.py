import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver_service = Service(executable_path='c:/Users/User/PycharmProjects/chromedriver.exe')

driver = webdriver.Chrome(
    service=driver_service
)

try:
    driver.get("http://suninjuly.github.io/registration1.html")
    button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    print(driver.page_source)
    time.sleep(1)
    input1 = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Input '
                                                  'your first name"]')
    input1.send_keys('Ivan')
    input2 = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Input '
                                                  'your last name"]')
    input2.send_keys('Ivan')
    input3 = driver.find_element(By.CLASS_NAME, 'form-control.third')
    input3.send_keys('jjjinsa@gmail.com')
    button.click()
    # Проверяем, что смогли зарегистрироваться
    # ждем загрузки страницы
    time.sleep(1)

    # находим элемент, содержащий текст
    welcome_text_elt = driver.find_element(By.TAG_NAME, "h1")
    # записываем в переменную welcome_text текст из элемента welcome_text_elt
    welcome_text = welcome_text_elt.text

    # с помощью assert проверяем, что ожидаемый текст совпадает с текстом на странице сайта
    assert "Congratulations! You have successfully registered!" == welcome_text
except Exception as err:
    print(err)
finally:
    time.sleep(3)
    driver.close()
    driver.quit()
    # driver.close()
