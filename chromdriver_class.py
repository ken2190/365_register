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


class ChromeDriver:
    def __init__(self,
                 user_data_dir=data.path_to_chrome_user_dir,
                 profile_directory=data.chrome_profile_name,
                 ):
        self.user_data_dir = user_data_dir
        self.profile_directory = profile_directory

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f'user-data-dir={self.user_data_dir}')
        options.add_argument(f"profile-directory={self.profile_directory}")
        # options.add_argument(f"--incognito")
        # options.add_argument(f'allow-profiles-outside-user-dir')

        # options.add_argument('--allow-profiles-outside-user-dir')
        # options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument('--profile-directory=Default-copy')
        options.add_argument('--disable-blink-features=AutomationControlled')

        # options.add_argument(r'user-data-dir=C:\Users\Sergey\AppData\Local\Google\Chrome\User Data\A_User')


        self.driver = webdriver.Chrome(options=options)

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
            print(simvol)
            time.sleep(random.randint(15, 40) / 100)
        time.sleep(random.randint(1, 4))

    def human_input2_new(self, input_text, element):
        '''Вводит текс, предварительно нужно нажать на форму'''

        time.sleep(0.3)
        for simvol in str(input_text):
            element.send_keys(simvol)
            print(simvol)
            time.sleep(random.randint(15, 40) / 100)
        time.sleep(random.randint(1, 4))

    def select_element(self, selection_obj, el_value='', el_visible_text=''):
        from selenium.webdriver.support.ui import Select

        select = Select(selection_obj)

        if el_visible_text != '':
            select.select_by_visible_text(el_visible_text)
        else:
            select.select_by_value(el_value)
        time.sleep(random.randint(1, 4))

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

