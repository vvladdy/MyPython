from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome(executable_path='c:/Users/User/PycharmProjects/chromedriver.exe')
try:
    link = "http://suninjuly.github.io/registration1.html"
    browser.get(link)

    arrayFields = browser.find_elements(By.CSS_SELECTOR, '.first_block input')

    firstName = browser.find_element(By.CSS_SELECTOR, '.form-group.first_class .form-control.first')
    firstName.send_keys("Ivan")

    lastName = browser.find_element(By.CSS_SELECTOR, '.form-group.second_class [placeholder="Input your last name"]')
    lastName.send_keys("Petrov")

    email = browser.find_element(By.CSS_SELECTOR, '.form-group.third_class [placeholder="Input your email"]')
    email.send_keys("cat@cat.ru")

    # Отправляем заполненную форму
    button = browser.find_element(By.XPATH, "//button")
    button.click()

    # Проверяем, что смогли зарегистрироваться
    # ждем загрузки страницы
    time.sleep(1)

    # находим элемент, содержащий текст
    welcome_text_elt = browser.find_element(By.TAG_NAME, "h1")
    # записываем в переменную welcome_text текст из элемента welcome_text_elt
    welcome_text = welcome_text_elt.text

    # с помощью assert проверяем, что ожидаемый текст совпадает с текстом на странице сайта
    assert "Congratulations! You have successfully registered!" == welcome_text

finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(2)
    # закрываем браузер после всех манипуляций
    browser.quit()
