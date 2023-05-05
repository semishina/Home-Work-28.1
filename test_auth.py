import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from settings import valid_email, valid_password, valid_region, valid_firstname, valid_lastname
from settings import invalid_email, invalid_password
import settings

# проверяем, что все страницы открываются успешно
# тест-кейс RT-001 открываем страницу авторизации
@pytest.mark.openpage
@pytest.mark.positive
def test_open_auth_page(browser):
    auth = browser.find_element(By.CLASS_NAME, 'card-container__title')
    assert auth.text == 'Авторизация', 'Fail'

# тест-кейс RT-002 открываем страницу пользовательского соглашения
@pytest.mark.openpage
@pytest.mark.positive
def test_open_users_agreement(browser):
    browser.find_element(By.XPATH, '//div[@class="auth-policy"]/a').click()
    browser.switch_to.window(browser.window_handles[1])
    title = browser.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('Публичная оферта'), 'FAIL'

# тест-кейсы RT-003 и RT-004 открываем страницу восстановления пароля и возвращаемся на станицу авторизации.
@pytest.mark.openpage
@pytest.mark.positive
def test_open_password_recovery_and_return(browser):
    browser.find_element(By.ID, 'forgot_password').click()
    assert browser.find_element(By.CLASS_NAME, 'card-container__title').text == 'Восстановление пароля'
    browser.find_element(By.ID, 'reset-back').click()
    auth = browser.find_element(By.CLASS_NAME, 'card-container__title')
    assert auth.text == 'Авторизация', 'Fail'

# тест-кейс RT-005 открываем страницу регистрации нового пользователя
@pytest.mark.openpage
@pytest.mark.positive
def test_open_registration(browser):
    browser.find_element(By.ID, 'kc-register').click()
    assert browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text == 'Регистрация'

# тест-кейсы RT-006, RT-007, RT-008, RT-009, RT-010, RT-011 открываем страницы авторизации через соцсети
@pytest.mark.openpage
@pytest.mark.positive
def test_open_vk_auth(browser):
    browser.find_element(By.ID, 'oidc_vk').click()
    assert 'vk.com' in browser.find_element(By.XPATH, '//div[@class="oauth_head"]/a').get_attribute('href')
    assert 'vk' in browser.current_url

@pytest.mark.positive
@pytest.mark.openpage
def test_open_ok_auth(browser):
    browser.find_element(By.ID, 'oidc_ok').click()
    assert 'Одноклассники' == browser.find_element(By.XPATH, '//div[@class="ext-widget_h_tx"]').text
    assert 'ok' in browser.current_url

@pytest.mark.positive
@pytest.mark.openpage
def test_open_mailru_auth(browser):
    browser.find_element(By.ID, 'oidc_mail').click()
    assert 'mail.ru' in browser.find_element(By.XPATH, '//span[@class="header__logo"]').text.lower()
    assert 'mail' in browser.current_url

@pytest.mark.positive
@pytest.mark.openpage
def test_open_google_auth(browser):
    browser.find_element(By.ID, 'oidc_google').click()
    assert 'google' in browser.current_url

@pytest.mark.positive
@pytest.mark.openpage
def test_open_yandex_auth(browser):
    browser.find_element(By.ID, 'oidc_ya').click()
    browser.find_element(By.ID, 'oidc_ya').click()
    assert 'yandex' in browser.current_url
# какой-то глюк, в ручном режиме кнопка страница открывается с одного клика,
# а в автоматизированном только со второго клика

# RT-011 и RT-012 открытие страниц по ссылкам в футере
@pytest.mark.positive
@pytest.mark.openpage
def test_privacy_policy_footer(browser):
    browser.find_elements(By.XPATH, '//a[@id="rt-footer-agreement-link"]/span')[0].click()
    browser.switch_to.window(browser.window_handles[1])
    title = browser.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('Публичная оферта'), 'FAIL'

@pytest.mark.positive
@pytest.mark.openpage
def test_open_users_agreement_footer(browser):
    browser.find_elements(By.XPATH, '//a[@id="rt-footer-agreement-link"]/span')[1].click()
    browser.switch_to.window(browser.window_handles[1])
    title = browser.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('Публичная оферта'), 'FAIL'

# ----------------------------------------------------------

# RT-013, RT-014, RT-015 регистрация
@pytest.mark.reg
@pytest.mark.negatvie # Помечаем тест как негативный, так как такой пользователь уже есть
@pytest.mark.xfail(reason='Учетная запись уже существует') # Помечаем тест как падающий
def test_reg_with_old_valid_data(browser):
    browser.find_element(By.ID, 'kc-register').click()
    inputs = browser.find_elements(By.XPATH, '//input[contains(@class, "rt-input__input")]')
    inputs[0].send_keys(valid_firstname)
    inputs[1].send_keys(valid_lastname)
    inputs[2].send_keys(valid_region)
    inputs[3].send_keys(valid_email)
    inputs[4].send_keys(valid_password)
    inputs[5].send_keys(valid_password)
    browser.find_element(By.NAME, 'register').click()
    assert browser.find_element(By.XPATH,
                                '//h1[@class="card-container__title"]').text == 'Учетная запись уже существует'
    print('Сообщение об ошибке: "Учётная запись уже существует"')

# Чтобы провести позитивный тест, необходимо удалить учетную запись данного пользователя
# или подготовить файл с новыми данными, не зарегистрированными в системе.
# @pytest.mark.reg
# @pytest.mark.positive
# def test_reg_with_new_valid_data(browser):
#     browser.find_element(By.ID, 'kc-register').click()
#     inputs = browser.find_elements(By.XPATH, '//input[contains(@class, "rt-input__input")]')
#     inputs[0].send_keys('новое имя')
#     inputs[1].send_keys('новая фамилия')
#     inputs[2].send_keys('Москва')
#     inputs[3].send_keys('новый email')
#     inputs[4].send_keys('новый пароль')
#     inputs[5].send_keys('новый пароль')
#     browser.find_element(By.NAME, 'register').click()
#     assert 'main' in browser.current_url

@pytest.mark.reg
@pytest.mark.negatvie # негативная проверка
def test_reg_empty_form(browser):
    browser.find_element(By.ID, 'kc-register').click()
    browser.find_element(By.NAME, 'register').click()
    error = browser.find_elements(By.XPATH, '//span[contains(@class, "rt-input-container__meta--error")]')
    assert len(error) == 5

# ----------------------------------------------------------
# RT-016, RT-017, RT-018 автоматическое переключение TAB между полями ввода информации в форме регистрации
@pytest.mark.auth
@pytest.mark.positive
def test_change_tab_on_mail(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.valid_email)
    browser.find_element(By.ID, 'password').click()
    assert browser.find_element(By.XPATH, '//div[contains(@class, "rt-tab--active")]').text == 'Почта'

@pytest.mark.auth
@pytest.mark.positive
def test_change_tab_on_login(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.valid_login)
    browser.find_element(By.ID, 'password').click()
    assert browser.find_element(By.XPATH, '//div[contains(@class, "rt-tab--active")]').text == 'Логин'

@pytest.mark.auth
@pytest.mark.positive
def test_change_tab_on_personal_account(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.valid_personal_account)
    browser.find_element(By.ID, 'password').click()
    assert browser.find_element(By.XPATH, '//div[contains(@class, "rt-tab--active")]').text == 'Лицевой счёт', 'FAIL'

# ----------------------------------------------------------

# RT-019, RT-020, RT-021 авторизация
@pytest.mark.auth
@pytest.mark.positive
def test_auth_by_valid_mail(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.valid_email)
    browser.find_element(By.ID, 'password').send_keys(settings.valid_password)
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.ID, 'logout-btn')

@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.xfail(reason='Появилась капча') # Помечаем тест как падающий, так как запрашивают текст с картинки
def test_auth_by_invalid_mail(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.invalid_email)
    browser.find_element(By.ID, 'password').send_keys(settings.valid_password)
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'
    assert browser.find_element(By.ID, 'form-error-message').text == 'Неверно введен текст с картинки'
# если заменить на
   # assert browser.find_element(By.ID, 'form-error-message').text == 'Неверно введен текст с картинки'
   # то при появлении капчи тест падать не будет, подходит для проверки наличия капчи

@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.xfail(reason='Появилась капча') # Помечаем тест как падающий, так как запрашивают текст с картинки
def test_auth_by_invalid_password(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.valid_email)
    browser.find_element(By.ID, 'password').send_keys(settings.invalid_password)
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'
# если заменить на
   # assert browser.find_element(By.ID, 'form-error-message').text == 'Неверно введен текст с картинки'
   # то при появлении капчи тест падать не будет, подходит для проверки наличия капчи
