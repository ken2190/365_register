import select

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import data
import random
import os
import zipfile
from selenium import webdriver
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
                 user_data_dir,
                 profile_directory,
                 ):
        self.user_data_dir = user_data_dir
        self.profile_directory = profile_directory

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        #options.add_argument(f'user-data-dir={self.user_data_dir}')
        # options.add_argument(f"profile-directory={self.profile_directory}")
        # options.add_argument(f"--incognito")
        # options.add_argument(f'allow-profiles-outside-user-dir')

        # options.add_argument('--allow-profiles-outside-user-dir')
        # options.add_argument('--enable-profile-shortcut-manager')
        #options.add_argument(f'--profile-directory={data.chrome_profile_name}-copy')
        options.add_argument('--disable-blink-features=AutomationControlled')

        # options.add_argument(r'user-data-dir=C:\Users\Sergey\AppData\Local\Google\Chrome\User Data\A_User')
        # 198.244.211.60:10889:avraint5716:698de1
        #http://username@password:196.19.8.88:8000
        #http://avraint5716@698de1:198.244.211.60:10889
        options.add_argument(f'--proxy-server=198.244.211.60:10889')

        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://2ip.ru/')
        input('Введите логин и пароль (avraint5716:698de1):')


    def start_registration(self):
        time.sleep(4)
        self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_Join').click()
        time.sleep(10)

        # self.driver.switch_to.frame(self.driver.find_element_by_class_name('mim-MembersIframeModule_Iframe '))
        # time.sleep(1)
        # self.driver.switch_to.frame(self.driver.find_element_by_class_name('lm-LegacyModule_IFrame '))
        # time.sleep(1)
        self.driver.switch_to.frame(self.driver.find_element_by_id('MembersIframe'))
        time.sleep(1)



    def human_input(self, input_text):
        '''Вводит текс, предварительно нужно нажать на форму'''

        time.sleep(0.3)
        for simvol in str(input_text):
            self.driver.find_element_by_tag_name("body").send_keys(simvol)
            # print(simvol)
            time.sleep(random.randint(15, 40) / 100)
        time.sleep(random.randint(1, 4))

    def human_input2_new(self, input_text, element):
        '''Вводит текс, предварительно нужно нажать на форму'''

        time.sleep(0.3)
        for simvol in str(input_text):
            element.send_keys(simvol)
            # print(simvol)
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


class ChromeDriverProxy(ChromeDriver):
    def __init__(self,):
        PROXY_HOST = data.PROXY_HOST
        PROXY_PORT = data.PROXY_PORT
        PROXY_USER = data.PROXY_USER
        PROXY_PASS = data.PROXY_PASS

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        def get_chromedriver(use_proxy=False, user_agent=None):
            path = os.path.dirname(os.path.abspath(__file__))
            chrome_options = webdriver.ChromeOptions()
            # chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument("--start-maximized")

            if use_proxy:
                pluginfile = 'proxy_auth_plugin.zip'

                with zipfile.ZipFile(pluginfile, 'w') as zp:
                    zp.writestr("manifest.json", manifest_json)
                    zp.writestr("background.js", background_js)
                chrome_options.add_extension(pluginfile)
            if user_agent:
                chrome_options.add_argument('--user-agent=%s' % user_agent)
            driver = webdriver.Chrome(
                os.path.join(path, 'chromedriver'),
                chrome_options=chrome_options)
            return driver


        self.driver = get_chromedriver(use_proxy=True)
        self.driver.get('https://2ip.ru', )  # any url you want to crawl
        time.sleep(2)
        self.driver.get('http://node-gb-10.astroproxy.com:10889/api/changeIP?apiToken=4c02390e9670aef9')
        time.sleep(5)
        self.driver.get('https://2ip.ru')  # any url you want to crawl
        time.sleep(5)


if __name__ == '__main__':
    p1 = ChromeDriverProxy()


