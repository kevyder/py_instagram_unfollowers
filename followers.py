import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_URL = "https://instagram.com"
IGUSERNAME = os.environ.get("IGUSERNAME")
IGPASSWORD = os.environ.get("IGPASSWORD")
IGACCOUNT = os.environ.get("IGACCOUNT")


class InstagramUnfollowers:
    def __init__(self, username, password, account):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.username = username
        self.password = password
        self.account_url = f'{INSTAGRAM_URL}/{account}'

    def check(self):
        try:
            cookies = pickle.load(open(f"{self.username}.pickle", "rb"))
            self.driver.get(INSTAGRAM_URL)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except (OSError, IOError) as e:
            self.__login()
        finally:
            self.__get_unfollowers()
            self.driver.close()

    # Private methods

    def __login(self):
        try:
            self.driver.get(INSTAGRAM_URL)
            sleep(10)

            username_type = self.driver.find_element(
                By.CSS_SELECTOR,
                "input[name='username'][type='text']"
            )
            username_type.send_keys(self.username)

            password_type = self.driver.find_element(
                By.CSS_SELECTOR,
                "input[name='password'][type='password']"
            )
            password_type.send_keys(self.password)

            log_in = self.driver.find_element(
                By.CSS_SELECTOR,
                "button[type='submit']"
            )
            log_in.click()
            sleep(10)
            if self.driver.current_url == INSTAGRAM_URL:
                raise Exception("Login unsuccessful")
            self.__save_cookies()
        except Exception as e:
            print(e.message)
            self.driver.close()

    def __get_unfollowers(self):
        # Get following people
        print("Getting following people, this might take a while...")
        following_element = self.driver.find_element(By.PARTIAL_LINK_TEXT, "following")
        following_element.click()
        following_list = self.__get_people()
        # Get followers
        print("Getting followers, this might take a while...")
        followers_element = self.driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
        followers_element.click()
        followers_list = self.__get_people()
        # Get not following people in list
        not_following_back = [user for user in following_list if user not in followers_list]
        # print data in ordered list
        not_following_back.sort()
        print("These people are not following you:")
        for name in not_following_back:
            print(name)
        print(f"Total: {len(not_following_back)}")

    def __get_people(self):  # Get people in list, return as list
        self.driver.get(self.account_url)
        sleep(10)
        # Access scroll-box
        scroll_box = self.driver.find_element(By.CLASS_NAME, "_aano")
        prev_height, height = 0, 1
        # Execute while there are more people to load
        while prev_height != height:
            prev_height = height
            sleep(3)
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        # Get people by anchor elements
        links = scroll_box.find_elements(By.TAG_NAME, 'a')
        names = [name.text.splitlines()[0] for name in links if name.text != '']
        return names

    def __save_cookies(self):
        pickle.dump(self.driver.get_cookies(), open(f"{self.username}.pickle", "wb"))


# Entry-Point
print("--------------------------------")
print("Instagram Unfollow-Checker")
print("--------------------------------\n")

# Run bot
print("Initializing WebDriver Manager")
print("--------------------------------")
sleep(1)
my_bot = InstagramUnfollowers(
    username=IGUSERNAME,
    password=IGPASSWORD,
    account=IGACCOUNT
)
my_bot.check()
