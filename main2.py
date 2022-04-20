import random
import time
import datetime

from selenium.webdriver import ActionChains

import data
from chromdriver_class import ChromeDriver
from get_users_data_from_google_sheets import sheet_user_values
from random_for_registration import RandomDateRegister
from google_sheets_writer import GoogleWriter1


CURENT_NUMBER = 1000

try:
    GoogleWriter1.write_row(["Дата", "№", "Логин", "Пароль", "Пин", "Строка", "e-mail", "Статус"])
except Exception as er:
    print(er)
    print('Ошибка, откройте доступ к странице')
    exit()


# c какой позиции читаем данные   1 -> вторая запись в таблице поле заголовков :)
start_line = 1
# c какой позиции записываем данные  2 -> вторая запись в таблице поле заголовков
GoogleWriter1.current_row = 2


while True:
    if start_line >= len(sheet_user_values):
        print('Все аккаунты зарегистрированы!')
        break

    user_data = sheet_user_values[start_line]
    print(f'Обработка аккаунта {start_line}/{len(sheet_user_values)-1}', '-'*100)

    driver1 = ChromeDriver()

    driver1.driver.get('https://www.bet365.com/#/HO/')
    time.sleep(10)
    try:
        # Cookies
        driver1.driver.find_element_by_class_name('ccm-CookieConsentPopup_Accept ').click()
    except:
        pass

    try:
        driver1.start_registration()
    except:
        print('Не удолось начать регистрировать аккаунт')
        driver1.driver.close()
        driver1.driver.quit()
        continue
    try:
        driver1.driver.find_element_by_xpath("//span[text()='Username taken.']")
    except:
        pass

    # поле обращение Mr/Mrs
    if user_data[0] == 'Ж':
        select_obj = driver1.driver.find_element_by_id('Title')
        driver1.select_element(select_obj, el_visible_text='Mrs')

    # ввод 1 имени
    element_fisrstName = driver1.driver.find_element_by_id('FirstName')
    driver1.human_input2_new(user_data[1], element_fisrstName)
    # driver1.driver.find_element_by_id('FirstName').send_keys('123')
    # driver1.driver.find_element_by_id('FirstName').click()
    # driver1.human_input(user_data[1])
    # print(user_data)
    # print(user_data[1])
    # input('123')

    # ввод 2 имени
    elemen_Surname = driver1.driver.find_element_by_id('Surname')
    driver1.human_input2_new(user_data[2], elemen_Surname)
    # driver1.driver.find_element_by_id('Surname').click()
    # driver1.human_input(user_data[2])

    # ввод даты рождения
    day, month, year = user_data[3].split('.')
    day = str(int(day))
    month = str(int(month))

    select_obj_day = driver1.driver.find_element_by_id('DateOfBirthDay')
    driver1.select_element(select_obj_day, el_value=day)

    select_obj_month = driver1.driver.find_element_by_id('DateOfBirthMonth')
    driver1.select_element(select_obj_month, el_value=str(int(month)-1))

    select_obj_year = driver1.driver.find_element_by_id('DateOfBirthYear')
    driver1.select_element(select_obj_year, el_value=year)

    # генерация случайных данных
    r = RandomDateRegister(user_data[1], user_data[2])
    email_ = r.get_email()
    phone_ = r.get_phone()
    password_ = r.get_password()
    pincode_ = r.get_pincode()

    # заполнение email
    driver1.driver.find_element_by_id('EmailAddress').send_keys('')
    time.sleep(random.randint(10, 20)/10)
    element_email = driver1.driver.find_element_by_id('EmailAddress')
    driver1.human_input2_new(email_, element_email)
    # driver1.human_input(email_)
    print(f'email: {email_}')

    # заполнение номера
    driver1.driver.find_element_by_id('PhoneNumber').send_keys('')
    time.sleep(random.randint(10, 20)/10)
    element_phone = driver1.driver.find_element_by_id('PhoneNumber')
    driver1.human_input2_new(phone_, element_phone)
    # driver1.human_input(phone_)
    # для скрола
    driver1.driver.find_element_by_id('Password').send_keys('')
    time.sleep(random.randint(2, 5))

    # заполнение адреса
    adress_text = user_data[4].split(' ')[0]
    element_CurrentBuildingNumberSearch = driver1.driver.find_element_by_id('CurrentBuildingNumberSearch')
    driver1.driver.find_element_by_id('CurrentBuildingNumberSearch').send_keys('')
    driver1.human_input2_new(adress_text, element_CurrentBuildingNumberSearch)
    # driver1.human_input(adress_text)
    time.sleep(2)
    # input('1')
    # street
    adress_text = user_data[4].split(' ')[1]
    # print(adress_text)
    element_CurrentStreetNameSearch = driver1.driver.find_element_by_id('CurrentStreetNameSearch')
    driver1.human_input2_new(adress_text, element_CurrentStreetNameSearch)
    time.sleep(2)

    # index адреса
    # input('Вводим postcode:')
    driver1.driver.find_element_by_id('CurrentPostcodeSearch').click()
    element_CurrentPostcodeSearch = driver1.driver.find_element_by_id('CurrentPostcodeSearch')
    driver1.human_input2_new(user_data[6], element_CurrentPostcodeSearch)
    # driver1.human_input(user_data[6])
    # нажимаем на кнопку поиска адреса
    driver1.driver.find_element_by_id('CurrentFindAddress').click()
    time.sleep(random.randint(5, 7))
    try:
        driver1.driver.find_element_by_id('CurrentAddress_0').click()
        time.sleep(2)
    except:
        pass
    # новое (17.12.2021) ввод города
    # time.sleep(1)
    # try:
    #     driver1.driver.find_element_by_id('CurrentTownCity').click()
    #     time.sleep(random.randint(2, 3))
    # except:
    #     pass
    # driver1.human_input(user_data[5])
    try:
        element_CurrentTownCity = driver1.driver.find_element_by_id('CurrentTownCity')
        driver1.human_input2_new(user_data[5], element_CurrentTownCity)
    except:
        print('Не удалось ввести город')

    time.sleep(random.randint(1, 3))

    # для скрола
    el1 = driver1.driver.find_element_by_id('Password')
    # ActionChains(driver1.driver).move_to_element(el1).click(el1).perform()
    driver1.driver.find_element_by_id('Password').send_keys('')
    time.sleep(random.randint(2, 3))

    # login + password
    driver1.driver.find_element_by_id('UserName').click()
    login_ = r.get_login()
    # driver1.human_input(login_)
    element_login = driver1.driver.find_element_by_id('UserName')
    driver1.human_input2_new(login_, element_login)
    driver1.driver.find_element_by_id('Password').click()
    time.sleep(2)
    # ввод логина
    while True:
        try:
            # ввод нового логина
            driver1.driver.find_element_by_xpath("//span[text()='Username taken.']")
            driver1.driver.find_element_by_id('UserName').clear()
            driver1.driver.find_element_by_id('UserName').send_keys('')
            login_ = r.get_more_random_login()
            # driver1.human_input(login_)
            driver1.human_input2_new(login_, element_login)
            time.sleep(1)
            driver1.driver.find_element_by_id('Password').click()
            time.sleep(2)
        except:
            break
    print(f'login: {login_}')

    time.sleep(random.randint(40, 50)/10)
    # ввод пароля
    driver1.driver.find_element_by_id('Password').click()
    element_password = driver1.driver.find_element_by_id('Password')
    driver1.human_input2_new(password_, element_password)
    # driver1.human_input(password_)
    time.sleep(random.randint(40, 50)/10)
    print(f'password: {password_}')


    # проматываем вниз
    try:
        driver1.driver.find_element_by_id('Submit').send_keys('')
    except Exception as er:
        print(er)

    # ввод и повторение пина
    driver1.driver.find_element_by_id('FourDigitPin').click()
    time.sleep(random.randint(10, 30)/10)
    element_pincode = driver1.driver.find_element_by_id('FourDigitPin')
    driver1.human_input2_new(pincode_, element_pincode)
    # driver1.human_input(pincode_)
    time.sleep(random.randint(5, 20)/10)

    driver1.driver.find_element_by_id('FourDigitPinConfirmed').click()
    time.sleep(random.randint(10, 30)/10)
    # driver1.human_input(pincode_)
    element_pincode2 = driver1.driver.find_element_by_id('FourDigitPinConfirmed')
    driver1.human_input2_new(pincode_, element_pincode2)
    time.sleep(random.randint(20, 50)/10)

    print(f'pin: {pincode_}')

    # NoThanksRadio
    driver1.driver.find_element_by_id('NoThanksRadio').click()
    time.sleep(random.randint(20, 30)/10)

    # мне больше 18
    driver1.driver.find_element_by_id('PoliciesAcceptance').click()
    time.sleep(random.randint(15, 25)/10)

    # конец регистрации !
    driver1.driver.find_element_by_id('Submit').click()
    time.sleep(45)

    is_good = False
    driver1.driver.switch_to.default_content()

    try:
        frame = driver1.driver.find_element_by_id('MembersIframe')
        driver1.driver.switch_to.frame(frame)
        driver1.driver.find_element_by_class_name('nh-NavigationHeaderModule_Title ')
        no_valid_flag = False

        # try:
        #     frame2 = driver1.driver.find_element_by_id('MembersHostFrame')
        #     driver1.driver.switch_to.frame(frame2)
        #     driver1.driver.find_element_by_class_name('pm-debitcard')
        #     print('порезан1')
        #     no_valid_flag = True
        # except:
        #     pass
        try:
            frame2 = driver1.driver.find_element_by_id('MembersHostFrame')
            driver1.driver.switch_to.frame(frame2)
            driver1.driver.find_element_by_class_name('withdrawal-restriction')
            print('порезан2')
            no_valid_flag = True
        except:
            pass

        if no_valid_flag:
            raise Exception('Не рабочий аккунт')
        print('Рабочий аккаунт')
        is_good = True
    except:
        print('Порезан')

    if is_good:
        status_ = 'Готов к работе'
    else:
        status_ = 'Порезан'


    driver1.driver.close()
    driver1.driver.quit()
    start_line += 1

    # время
    current_date = datetime.datetime.now()
    current_date_string = current_date.strftime('%m.%d.%Y')

    data_ = [
        str(current_date_string), # time now
        CURENT_NUMBER + start_line, # number
        login_, # login
        password_, # password
        pincode_, # pin
        ' '.join(user_data), # строка с информацией о пользователе
        email_, # email
        status_
    ]
    print(data_)
    GoogleWriter1.write_row(data_)

    print(f'Аккаунт {start_line-1}/{len(sheet_user_values)-1} успешно обработан', '-'*100)


print('End.')
# driver1.select_in_selection()

