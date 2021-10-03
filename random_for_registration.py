import random


class RandomDateRegister:
    def __init__(self, name, last_name):
        self.name = name.replace(' ', '')
        self.name = self.name.lower()

        self.last_name = last_name.replace(' ', '')
        self.last_name = self.last_name.lower()

    def get_email(self):
        '''Генерирует случайный email на основе имён'''
        post_fix = [
            '@gmail.com',
            '@outlook.com',
            '@hotmail.com',
            '@yahoo.com'
        ]

        post_fix_ = random.choice(post_fix)

        if random.randint(0, 1) == 0:
            email_ = self.name[:random.randint(4, 7)]
            email_ += self.last_name[:random.randint(4, 6)]
        else:
            email_ = self.last_name[:random.randint(4, 6)]
            email_ += self.name[:random.randint(4, 7)]

        for i in range(random.randint(3, 4)):
            email_ += str(random.randint(0, 9))
        email_ += post_fix_

        return email_

    def get_phone(self):
        phone_number = '752'
        for i in range(8):
            phone_number += str(random.randint(0, 9))

        return phone_number

    def get_password(self):
        alphabet = 'qwertyuiopasdfghjklzxcvbnm'

        password = ''

        password += str(random.randint(0, 9))*3

        password += random.choice(alphabet)*3

        return password

    def get_pincode(self):
        pincode = ''

        for i in range(4):
            pincode += str(random.randint(0, 9))

        if len(set(pincode)) < 3:
            return self.get_pincode()

        return pincode

    def get_login(self):
        login = self.name[:3]
        for i in range(3):
            login += str(random.randint(0, 9))

        return login

    def get_more_random_login(self):
        login = ''
        for i in range(3):
            login += str(random.choice(self.name).lower())
        for i in range(3):
            login += str(random.randint(0, 9))

        return login

# r = RandomDateRegister("Sam Narm", 'Stevenson')
# r.get_email()
# r.get_phone()
# print(r.get_password())
# r.get_pincode()



