from time import sleep
import pytest
from selenium.webdriver.common.keys import Keys
from base_class import AuthPage, CodePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from settings import valid_email, valid_password, valid_number, valid_login, valid_account
from selenium.webdriver.support import expected_conditions as EC


def test_screen_auth_page(selenium):  # открыть страницу авторизации и сделать скриншот
    form = AuthPage(selenium)
    form.driver.save_screenshot('scr_1.jpg')


def test_phone_default_page(selenium):  # страница авторизации должна открыться на вкладке "Телефон"
    form = AuthPage(selenium)
    assert form.placeholder.text == 'Мобильный телефон'


def test_automatic_switch(selenium):  # автоматическое переключение вкладок на странице авторизации
    form = AuthPage(selenium)
    form.username.send_keys('+79174586955')
    form.password.send_keys('hgfjgfjhmghg')
    sleep(5)
    assert form.placeholder.text == 'Мобильный телефон'

    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)
    form.username.send_keys('hkgkhgh@mail.ru')
    form.password.send_keys('jhjhvjfjgfjhghg')
    sleep(5)
    assert form.placeholder.text == 'Электронная почта'

    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)
    form.username.send_keys('Ziliboba')
    form.password.send_keys('chxjchdd')
    sleep(5)
    assert form.placeholder.text == 'Логин'

    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)
    form.username.send_keys('012345678910')
    form.password.send_keys('hbdsjvbdjfbv')
    sleep(5)
    assert form.placeholder.text == 'Лицевой счёт'


def test_auth_wrong_phone(selenium):  # авторизация по невалидным номеру и паролю
    form = AuthPage(selenium)
    form.username.send_keys('+79993454568')
    form.password.send_keys('akdakdjghbfj')
    sleep(20)  # время для ручного ввода с Captcha
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


def test_auth_true_phone(selenium):  # авторизация по валидным номеру и паролю
    form = AuthPage(selenium)
    form.username.send_keys(valid_number)
    form.password.send_keys(valid_password)
    sleep(20)
    form.btn_click()
    assert form.get_current_url() == '/account_b2c/page'


def test_auth_true_email(selenium):  # авторизация по валидным почте и паролю
    form = AuthPage(selenium)
    form.username.send_keys(valid_email)
    form.password.send_keys(valid_password)
    sleep(20)
    form.btn_click()
    assert form.get_current_url() == '/account_b2c/page'


def test_auth_true_login(selenium):  # авторизация по валидным логину и паролю
    form = AuthPage(selenium)
    form.username.send_keys(valid_login)
    form.password.send_keys(valid_password)
    sleep(20)
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


def test_auth_wrong_email(selenium):  # авторизация по невалидным почте и паролю
    form = AuthPage(selenium)
    form.username.send_keys('ljdneljwdvn@gmail.com')
    form.password.send_keys('dadawqvacczcfjhvjff')
    sleep(20)
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


def test_auth_wrong_login(selenium):  # авторизация по валидному паролю и невалидному логину
    form = AuthPage(selenium)
    form.username.send_keys('ratavza@yandex.com')
    form.password.send_keys(valid_password)
    sleep(20)
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


def test_auth_true_account(selenium):  # авторизация по валидным лицевому счету и паролю
    form = AuthPage(selenium)
    form.username.send_keys(valid_account)
    form.password.send_keys(valid_password)
    sleep(20)
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


def test_auth_wrong_account(selenium):  # авторизация по невалидным счету и паролю
    form = AuthPage(selenium)
    form.username.send_keys('4311256458965')
    form.password.send_keys('zczqbwwcvbkfv')
    sleep(20)
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


def test_auth_by_phone_code(selenium):  # авторизация по паролю на номер телефона
    form = CodePage(selenium)
    form.address.send_keys(valid_number)
    sleep(20)
    form.get_click()
    otc = form.driver.find_element(By.ID, 'rt-code-0')
    assert otc


def test_scr_page_code_form(selenium):  # авторизация по коду и скриншот
    form = CodePage(selenium)
    form.driver.save_screenshot('scr_2.jpg')


def test_reg_form(selenium):  # проверка формы регистрации
    form = AuthPage(selenium)
    form.register.click()
    sleep(5)
    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')
    assert reset_pass.text == 'Регистрация'


def test_recovery_form(selenium):  # проверка восстановления доступа
    form = AuthPage(selenium)
    form.forgot.click()
    sleep(5)
    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')
    assert reset_pass.text == 'Восстановление пароля'


def test_user_document(selenium):  # доступность пользов. соглашения
    form = AuthPage(selenium)
    original_window = form.driver.current_window_handle
    form.agree.click()
    sleep(5)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    title_page = form.driver.execute_script("return window.document.title")
    assert title_page == 'User agreement'


def test_auth_by_mail(selenium):  # авторизация через mail.ru
    form = AuthPage(selenium)
    form.mail_ru_btn.click()
    sleep(5)
    assert form.get_base_url() == 'connect.mail.ru'


def test_auth_by_vk(selenium):  # авторизация через vk.ru
    form = AuthPage(selenium)
    form.vk_btn.click()
    sleep(5)
    assert form.get_base_url() == 'id.vk.com'


def test_auth_by_ok(selenium):  # авторизация через Одноклассники
    form = AuthPage(selenium)
    form.ok_btn.click()
    sleep(5)
    assert form.get_base_url() == 'connect.ok.ru'


def test_auth_by_yandex(selenium):  # авторизация через ЯндексID
    form = AuthPage(selenium)
    form.yandex_btn.click()
    sleep(5)
    assert form.get_base_url() == 'passport.yandex.ru'
