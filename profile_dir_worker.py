import os
import shutil

import data


class ProfileDirWorker:
    def __init__(self, path_to_profile_dir, profile_name, postfix='-copy'):
        self.path_to_profile_dir = path_to_profile_dir
        self.profile_name = profile_name
        self.postfix = postfix

        self.path_to_default_profile = os.path.join(path_to_profile_dir, profile_name)
        self.path_to_new_profile = os.path.join(path_to_profile_dir, profile_name+postfix)

        # print(self.path_to_new_profile)

    def create_copy(self):
        print(f'Создаём копию профиля {self.profile_name}')
        copytree(self.path_to_default_profile, self.path_to_new_profile)
        print('Копия профиля успешно создана')

    def del_copy(self):
        shutil.rmtree(self.path_to_new_profile)
        print('Копия профиля успешно удалена')


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            # try:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)
            # except:
            #     pass


ProfileDirWorker1 = ProfileDirWorker(path_to_profile_dir=data.path_to_chrome_user_dir,
                                     profile_name=data.chrome_profile_name)

# пытаемся удалить директорию, если она есть
try:
    ProfileDirWorker1.del_copy()
except Exception as er:
    print(f'dir: {er}')
# ProfileDirWorker1.create_copy()
# ProfileDirWorker1.del_copy()
# path_to_chrome_user_dir = r'C:\Users\Sergey\AppData\Local\Google\Chrome\User Data\Default'
#
# dst = r'D:\\dir12'
#
# copytree(path_to_chrome_user_dir, dst)

