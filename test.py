import os
import shutil

from selenium import webdriver

import data
from profile_dir_worker import ProfileDirWorker1


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
        # options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument(f'--profile-directory={data.chrome_profile_name}-copy')
        options.add_argument('--disable-blink-features=AutomationControlled')

        # options.add_argument(r'user-data-dir=C:\Users\Sergey\AppData\Local\Google\Chrome\User Data\A_User')

        self.driver = webdriver.Chrome(options=options)


ProfileDirWorker1.create_copy()
driver1 = ChromeDriver()
#
# ProfileDirWorker1.del_copy()
# path_to_chrome_user_dir = r'C:\Users\Sergey\AppData\Local\Google\Chrome\User Data\Default'
#
# dst = r'D:\\dir12'
#
# copytree(path_to_chrome_user_dir, dst)
