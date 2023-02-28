# code licenced and written by Raf 2022 | all rights reserved
# insta: raf_hm_    discord: raffert#4643    email: rafhermans07@gmail.com    github: Raf-hm
# automatic instagram mass dm bot using python and selenium. V1.0.0 dec.23.22-dec.30.22

try:
    import os
    import time
    import json
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("Import Error | Please make sure all module requirements are met.")
    exit()
 
try:
    config = json.loads(open("./config.json", "r", encoding="utf-8").read())
except ImportError:
    print("Import Error | cannot locate config.json file.")
    exit()


driver = webdriver.Chrome(ChromeDriverManager().install())
 

targetlist = open("./usernames/usernames.txt").readlines()


class bot:
    def __init__(self, username, password, user, message):
        self.username = username
        self.password = password
        self.user = user
        self.message = message
        self.base_url = 'https://www.instagram.com/'
        self.bot = driver
        self.bot.set_window_position(0, 0)
        self.bot.set_window_size(600, 936)
        self.login()
 
    def login(self):
        self.bot.get(self.base_url)
        accept_cookies = WebDriverWait(self.bot, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//button[text()="Essentiële en optionele cookies toestaan"]')))
        accept_cookies.click()
        time.sleep(2)
        enter_username = WebDriverWait(self.bot, 20).until(expected_conditions.presence_of_element_located((By.NAME, 'username')))
        enter_username.send_keys(self.username)
        enter_password = WebDriverWait(self.bot, 20).until(expected_conditions.presence_of_element_located((By.NAME, 'password')))
        enter_password.send_keys(self.password)
        enter_password.send_keys(Keys.RETURN)
        os.system("cls" if os.name == "nt" else "clear")
        print("login succesfull!")
        print("clearing popups...")
        accept_cookies = WebDriverWait(self.bot, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//button[text()="Niet nu"]')))
        accept_cookies.click()
        time.sleep(1)
        accept_cookies = WebDriverWait(self.bot, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//button[text()="Niet nu"]')))
        accept_cookies.click()
        print("done, initializing messages...")
        for i in range(len(targetlist)):
            target = targetlist[i].replace("\n", "")

            self.bot.get("https://www.instagram.com/direct/inbox/")

            try:
                find_name = WebDriverWait(self.bot, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//button[text()="Chatbericht sturen"]')))
                find_name.click()
            except TimeoutException:
                self.bot.get("https://www.instagram.com/direct/inbox/")

            try:
                Zoeken = WebDriverWait(self.bot, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@placeholder='Zoeken...']"))) 
                Zoeken.send_keys(target)
            except TimeoutException:
                self.bot.get("https://www.instagram.com/direct/inbox/")

            try:
                select_username = WebDriverWait(self.bot, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//div[text()="' + target + '"]')))
                select_username.click()
            except TimeoutException:
                self.bot.get("https://www.instagram.com/direct/inbox/")

            try:
                confirm_name = WebDriverWait(self.bot, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//div[text()="Volgende"]')))
                confirm_name.click()
            except TimeoutException:
                self.bot.get("https://www.instagram.com/direct/inbox/")
            
            try:
                input_element_send = WebDriverWait(self.bot, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Chatbericht sturen...']"))) 
                input_element_send.send_keys(self.message)
                input_element_send.send_keys(Keys.ENTER)
            except TimeoutException:
                self.bot.get("https://www.instagram.com/direct/inbox/")

            with open("./usernames/done.txt", "a") as done_file:
                done_file.write(target + "\n")

            with open("./usernames/usernames.txt", 'r+') as f:
                firstLine = f.readline()
                data = f.read()
                f.seek(0)
                f.write(data)
                f.truncate()

            print("message to " + target)

            time.sleep(int(config["data"]["delay"]))

def init():
    bot(config["data"]["username"], config["data"]["password"], targetlist, config["data"]["message"])

init()

