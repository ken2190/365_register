from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
import time
import data
import random
from multiprocessing.dummy import Pool


# def open_window(driver):
#     time.sleep(1)
#     driver.open_new_window_2ip()
#     time.sleep(7)


class FireFoxDriverWithVPN():
    def __init__(self):
        self.is_VPN = True
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True


        fp = webdriver.FirefoxProfile(data.firefox_profile_path)
        fp.set_preference("browser.privatebrowsing.autostart", True)

        options = webdriver.FirefoxOptions()
        options.add_argument("-private")
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("dom.webnotifications.enabled", False)
        binary = data.firefox_binary
        options.binary = binary

        driver = webdriver.Firefox(capabilities=firefox_capabilities, firefox_profile=fp,
                                   firefox_binary=data.firefox_binary,
                                   executable_path=data.path_to_geckodriver,
                                   options=options)

        self.driver = driver
        self.driver.set_page_load_timeout(30)
        time.sleep(10)

        self.driver.get('https://2ip.ru/')
        # t1 = Thread(target=open_window, args=(self,))
        # t1.start()

        try:
            self.driver.get('https://www.bet365.com/')
        except:
            print('Сайт не загружен')
            self.open_new_window_2ip()
            time.sleep(15)
            print('open-close')

        # закрываем 2 окно
        # print('Закрываем 2 окно')
        # self.close_last_window()

        self.driver.set_page_load_timeout(75)

        try:
            self.driver.get('https://www.bet365.com/')
        except:
            self.driver.close()
            self.driver.quit()
            print('Сайт bet365 не загрузился')
            raise Exception('Сайт bet365 не загрузился')

    def start_registration(self):
        time.sleep(4)
        self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_Join').click()
        time.sleep(10)
        self.driver.switch_to.frame(self.driver.find_element_by_class_name('mim-MembersIframeModule_Iframe '))
        time.sleep(1)
        self.driver.switch_to.frame(self.driver.find_element_by_class_name('lm-LegacyModule_IFrame '))
        time.sleep(1)

    def human_input(self, input_text):
        '''Вводит текс, предварительно нужно нажать на форму'''

        time.sleep(0.3)
        for simvol in str(input_text):
            self.driver.find_element_by_tag_name("body").send_keys(simvol)
            time.sleep(random.randint(15, 40)/100)
        time.sleep(random.randint(1, 4))

    def select_element(self, selection_obj, el_value='', el_visible_text=''):
        from selenium.webdriver.support.ui import Select

        select = Select(selection_obj)

        if el_visible_text != '':
            select.select_by_visible_text(el_visible_text)
        else:
            select.select_by_value(el_value)
        time.sleep(random.randint(1,4))


    def select_in_selection(self):
        from selenium.webdriver.support.ui import Select
        select = Select(self.driver.find_element_by_id('Title'))
        select.select_by_visible_text('Mrs')

        print(1)
        time.sleep(5)
        select = Select(self.driver.find_element_by_id('DateOfBirthDay'))
        select.select_by_value('1')
        print(1)

        time.sleep(5)
        select = Select(self.driver.find_element_by_id('DateOfBirthMonth'))
        select.select_by_value('2')
        print(1)

        time.sleep(5)
        select = Select(self.driver.find_element_by_id('DateOfBirthMonth'))
        select.select_by_value('1975')
        # select.select_by_index(index)
        # select.select_by_visible_text("text")
        # select.select_by_value(value)

    def open_new_window_2ip(self):
        current_window = self.driver.current_window_handle
        print('open site 2ip.ru')
        self.driver.execute_script(f"window.open('https://2ip.ru/', '_blank')")
        time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.close()
        self.driver.switch_to.window(current_window)


    def close_last_window(self):
        current_window = self.driver.current_window_handle
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.close()
        # self.driver.switch_to.window(current_window)
        self.driver.switch_to.default_content()


class GetWorkAccounts:
    def __init__(self, number_of_accounts, path_to_firefox_profile):
        self.firefox_profile = path_to_firefox_profile
        self.number_of_accounts = number_of_accounts

        def check_bet365(driver):
            # провепка правильно ли открылся сайт bet365
            try:
                time.sleep(2)
                driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
                return True
            except Exception as er:
                return False

        def open_new_window_2ip(driver):
            current_window = driver.current_window_handle
            driver.execute_script(f"window.open('https://2ip.ru/', '_blank')")
            time.sleep(7)
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(current_window)

        def get_driver():
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True

            fp = webdriver.FirefoxProfile(self.firefox_profile)
            fp.set_preference("browser.privatebrowsing.autostart", True)

            options = webdriver.FirefoxOptions()
            options.add_argument("-private")
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference("dom.webnotifications.enabled", False)
            binary = data.firefox_binary
            options.binary = binary

            driver = webdriver.Firefox(capabilities=firefox_capabilities, firefox_profile=fp,
                                       firefox_binary=data.firefox_binary,
                                       executable_path=data.path_to_geckodriver,
                                       options=options)

            time.sleep(10)

            driver.get('https://2ip.ru/')
            driver.set_page_load_timeout(15)
            try:
                driver.get('https://www.bet365.com/')
                driver.set_page_load_timeout(25)
                if check_bet365(driver):
                    return driver, 'OK'
            except:
                pass

            driver.set_page_load_timeout(25)
            for i in range(2):
                open_new_window_2ip(driver)
                time.sleep(0.3)

            try:
                driver.get('https://www.bet365.com/')
                if check_bet365(driver):
                    return driver, 'OK'
                else:
                    return driver, 'Сайт bet365 не загрузился'
            except:
                return driver, 'Сайт bet365 не загрузился'

        def add_accounts_to_list(Browsers_List=[]):
            # задержка
            time_to_sleep = random.randint(1, 1000) / 500
            time.sleep(time_to_sleep)
            driver, info = get_driver()
            if info == 'OK':
                Browsers_List.append(driver)
                print('+1 browser')
            else:
                try:
                    driver.close()
                    driver.quit()
                except:
                    pass

        # число браузеров, которое будет открыто
        number_of_tries = 6
        try:
            number_of_tries = data.number_of_tries
        except:
            pass
        Browser_List = []

        while len(Browser_List) < self.number_of_accounts:
            try:
                with Pool(processes=number_of_tries) as p:
                    p.map(add_accounts_to_list, [Browser_List for i in range(number_of_tries)])
            except Exception as er:
                print(f'Ошибка при выполнениии Poll: {er}')

            # check_counter_i = 0
            # while check_counter_i < len(Browser_List):
            #     if check_bet365(Browser_List[check_counter_i]):
            #         check_counter_i += 1
            #     else:
            #         print('Браузер не работает!')
            #         Browser_List.pop(check_counter_i)

            print(f'Открыто {len(Browser_List)} из {self.number_of_accounts} аккаунтов')


        while len(Browser_List) > self.number_of_accounts:
            Browser_List.pop(-1).quit()
            print('1 лишний аккаунт удалён')

        self.Browser_List = Browser_List

    def return_Browser_List(self):
        return self.Browser_List



class FireFoxDriverWithVPN_multipotok_open(FireFoxDriverWithVPN):
    def __init__(self, path_to_firefox_profile):
        self.is_VPN = True
        get_accounts_class = GetWorkAccounts(number_of_accounts=1, path_to_firefox_profile=path_to_firefox_profile)
        self.driver = get_accounts_class.return_Browser_List()[0]


