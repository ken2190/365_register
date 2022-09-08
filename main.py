import random
import time
import datetime

from selenium.webdriver import ActionChains

import data
from chromdriver_class import ChromeDriverProxy
# from get_users_data_from_google_sheets import sheet_user_values, number_of_list2_lines
from random_for_registration import RandomDateRegister
# from google_sheets_writer import GoogleWriter1

from google_api_new import GoogleSheet
# CURENT_NUMBER = 1000

# try:
#     GoogleWriter1.write_row(["Дата", "№", "Логин", "Пароль", "Пин", "Строка", "e-mail", "Статус"])
# except Exception as er:
#     print(er)
#     print('Ошибка, откройте доступ к странице')
#     exit()

#
# # c какой позиции читаем данные   1 -> вторая запись в таблице поле заголовков :)
# start_line = 1
# # c какой позиции записываем данные  1 -> вторая запись в таблице поле заголовков
# GoogleWriter1.current_row = 2

# start_line = data.start_google_sheets_line - 1
# GoogleWriter1.current_row = number_of_list2_lines+1

while True:
    google_api = GoogleSheet()

    user_data = google_api.get_row_to_work()
    if user_data == []:
        print('Нет аккаутов для обработки')


    print(f'Обработка аккаунта: {user_data}')


    driver1 = ChromeDriverProxy()

    driver1.driver.get('https://www.bet365.com/#/HO/')
    time.sleep(11)
    try:
        # Cookies
        driver1.driver.find_element_by_class_name('ccm-CookieConsentPopup_Accept ').click()
    except:
        time.sleep(10)
        try:
            # Cookies
            driver1.driver.find_element_by_class_name('ccm-CookieConsentPopup_Accept ').click()
        except:
            pass
    # input('k')
    try:
        driver1.start_registration()
    except:
        print('Не удолось начать регистрировать аккаунт')
        driver1.driver.close()
        driver1.driver.quit()
        continue

    # выбор страны UK
    select_obj = driver1.driver.find_element_by_id('country_residence')
    driver1.select_element(select_obj, el_visible_text='United Kingdom')
    time.sleep(3)
    # driver1.driver.find_element_by_id('Confirm').click()
    try:
        driver1.driver.find_element_by_class_name('oam-ConfirmButton ').click()
    except Exception as er:
        print(f'Не удалось изменит страну: {er}')
    time.sleep(3)

    # поле обращение Mr/Mrs
    if user_data[0] == 'MISS':
        select_obj = driver1.driver.find_element_by_id('title')
        driver1.select_element(select_obj, el_visible_text='Miss')

    time.sleep(4)
    # ввод 1 имени
    element_fisrstName = driver1.driver.find_element_by_id('first_name')
    driver1.human_input2_new(user_data[1], element_fisrstName)
    # driver1.driver.find_element_by_id('FirstName').send_keys('123')
    # driver1.driver.find_element_by_id('FirstName').click()
    # driver1.human_input(user_data[1])
    # print(user_data)
    # print(user_data[1])
    # input('123')

    # ввод 2 имени
    elemen_Surname = driver1.driver.find_element_by_id('last_name')
    driver1.human_input2_new(user_data[2], elemen_Surname)
    # driver1.driver.find_element_by_id('Surname').click()
    # driver1.human_input(user_data[2])

    # ввод даты рождения
    day, month, year = user_data[3].split('.')
    day = str(int(day))
    month = str(int(month))

    select_obj_day = driver1.driver.find_elements_by_class_name('oam-DateSelectComponent-1 ')[0]
    if len(day) == 1:
        day = '0' + day
    driver1.select_element(select_obj_day, el_value=day)

    select_obj_month = driver1.driver.find_elements_by_class_name('oam-DateSelectComponent-1 ')[1]
    if len(month) == 1:
        month = '0' + month
    driver1.select_element(select_obj_month, el_value=month)

    select_obj_year = driver1.driver.find_elements_by_class_name('oam-DateSelectComponent-1 ')[2]
    driver1.select_element(select_obj_year, el_value=year)

    # генерация случайных данных
    r = RandomDateRegister(user_data[1], user_data[2])
    email_ = r.get_email()
    phone_ = r.get_phone()
    password_ = r.get_password()
    pincode_ = r.get_pincode()

    # заполнение email
    driver1.driver.find_element_by_id('email').send_keys('')
    time.sleep(random.randint(10, 20)/10)
    element_email = driver1.driver.find_element_by_id('email')
    driver1.human_input2_new(email_, element_email)
    # driver1.human_input(email_)
    print(f'email: {email_}')

    # заполнение номера
    driver1.driver.find_element_by_id('tel').send_keys('')
    time.sleep(random.randint(10, 20)/10)
    element_phone = driver1.driver.find_element_by_id('tel')
    driver1.human_input2_new(phone_, element_phone)
    print(f'phone: {phone_}')


    # не соглащаемся с уведомлениями
    driver1.driver.find_elements_by_class_name('oam-OARadioButton_Radio ')[1].click()
    time.sleep(3)
    # для скрола
    driver1.driver.find_element_by_id('password').send_keys('')
    time.sleep(random.randint(2, 5))

    # заполнение адреса
    adress_text = user_data[4]
    element_CurrentBuildingNumberSearch = driver1.driver.find_element_by_id('addr_bld_no')
    driver1.driver.find_element_by_id('addr_bld_no').send_keys('')
    driver1.human_input2_new(adress_text, element_CurrentBuildingNumberSearch)
    # driver1.human_input(adress_text)
    time.sleep(2)
    # input('1')
    # street
    # adress_text = user_data[4].split(' ')[1:]
    # adress_text = ' '.join(adress_text)
    # # print(adress_text)
    # element_CurrentStreetNameSearch = driver1.driver.find_element_by_id('CurrentStreetNameSearch')
    # driver1.human_input2_new(adress_text, element_CurrentStreetNameSearch)
    # time.sleep(2)

    # index адреса
    # input('Вводим postcode:')
    driver1.driver.find_element_by_id('addr_pst_zip').click()
    element_CurrentPostcodeSearch = driver1.driver.find_element_by_id('addr_pst_zip')
    driver1.human_input2_new(user_data[6], element_CurrentPostcodeSearch)
    # driver1.human_input(user_data[6])
    # нажимаем на кнопку поиска адреса
    driver1.driver.find_element_by_id('find_address').click()
    time.sleep(random.randint(10, 12))
    try:
        driver1.driver.find_elements_by_class_name('oam-AddressLabel ')[1].click()
        time.sleep(4)
    except:
        pass

    # новое (17.12.2021) ввод города
    try:
        element_CurrentTownCity = driver1.driver.find_element_by_id('addr_twn_cty')
        print(element_CurrentTownCity.get_attribute("value"))
        if element_CurrentTownCity.get_attribute("value") == '':
            driver1.human_input2_new(user_data[5], element_CurrentTownCity)
    except:
        print('Не удалось ввести город')

    time.sleep(random.randint(1, 3))

    # для скрола
    el1 = driver1.driver.find_element_by_id('password')
    # ActionChains(driver1.driver).move_to_element(el1).click(el1).perform()
    driver1.driver.find_element_by_id('password').send_keys('')
    time.sleep(random.randint(2, 3))

    # login + password
    driver1.driver.find_element_by_id('username').click()
    login_ = r.get_login()
    # driver1.human_input(login_)
    element_login = driver1.driver.find_element_by_id('username')
    driver1.human_input2_new(login_, element_login)
    driver1.driver.find_element_by_id('password').click()
    time.sleep(2)
    # ввод логина
    while True:
        try:
            # ввод нового логина
            driver1.driver.find_element_by_xpath("//div[text()='Username taken.']")
            driver1.driver.find_element_by_id('username').clear()
            driver1.driver.find_element_by_id('username').send_keys('')
            login_ = r.get_more_random_login()
            # driver1.human_input(login_)
            driver1.human_input2_new(login_, element_login)
            time.sleep(1)
            driver1.driver.find_element_by_id('password').click()
            time.sleep(2)
        except:
            break
    print(f'login: {login_}')

    time.sleep(random.randint(40, 50)/10)
    # ввод пароля
    driver1.driver.find_element_by_id('password').click()
    element_password = driver1.driver.find_element_by_id('password')
    driver1.human_input2_new(password_, element_password)
    # driver1.human_input(password_)
    time.sleep(random.randint(40, 50)/10)
    print(f'password: {password_}')


    # проматываем вниз
    # try:
    #     driver1.driver.find_element_by_id('Submit').send_keys('')
    # except Exception as er:
    #     print(er)


    # мне больше 18
    driver1.driver.find_element_by_class_name('oam-FieldInputCheckboxTerms_Checkbox ').click()
    time.sleep(random.randint(15, 25)/10)

    # конец регистрации !
    driver1.driver.find_element_by_class_name('oam-FieldSubmitButtonWithModal').click()
    time.sleep(45)

    # is_good = False
    driver1.driver.switch_to.default_content()

    # новая проверка на успешность <-
    is_good_account = True
    try:
        frame = driver1.driver.find_element_by_id('MembersIframe')
        driver1.driver.switch_to.frame(frame)
        frame2 = driver1.driver.find_element_by_id('MembersHostFrame')
        driver1.driver.switch_to.frame(frame2)
        driver1.driver.find_element_by_class_name('accept-button')
        print('Порезан')
        is_good_account = False
    except:
        print('Готов к работе')

    # новая проверка на успешность ->

    # try:
    #     frame = driver1.driver.find_element_by_id('MembersIframe')
    #     driver1.driver.switch_to.frame(frame)
    #     driver1.driver.find_element_by_class_name('nh-NavigationHeaderModule_Title ')
    #     no_valid_flag = False
    #
    #     try:
    #         frame2 = driver1.driver.find_element_by_id('MembersHostFrame')
    #         driver1.driver.switch_to.frame(frame2)
    #
    #         # уже есть аккаунт
    #         try:
    #             driver1.driver.find_element_by_class_name('duplicateAccountLightBox')
    #             print('уже есть аккаунт')
    #             no_valid_flag = True
    #             raise Exception('Не рабочий аккунт')
    #         except:
    #             pass
    #
    #         try:
    #             driver1.driver.find_element_by_class_name('payment-header-details-title')
    #             print('блок внесите деньги - есть')
    #         except:
    #             print('блок внесите деньги - нет')
    #             no_valid_flag = True
    #             raise Exception('Не рабочий аккунт')
    #
    #         driver1.driver.find_element_by_class_name('withdrawal-restriction')
    #         print('порезан2')
    #         no_valid_flag = True
    #     except:
    #         pass
    #
    #     if no_valid_flag:
    #         raise Exception('Не рабочий аккунт')
    #     print('Рабочий аккаунт')
    #     is_good = True
    # except:
    #     print('Порезан')

    if is_good_account:
        status_ = 'Готов к работе'
    else:
        status_ = 'Порезан'

    input()
    driver1.driver.close()
    driver1.driver.quit()


    # время
    current_date = datetime.datetime.now()
    current_date_string = current_date.strftime('%m.%d.%Y')

    data_ = [
        str(current_date_string), # time now
        login_, # login
        password_, # password
        ' '.join(user_data), # строка с информацией о пользователе
        email_, # email
        status_
    ]
    print(data_)
    google_api.add_row_to_second_table(data_)
    google_api.update_info_finish_row()

    print(f'Аккаунт успешно обработан', '-'*100)
    # input()


print('End.')

