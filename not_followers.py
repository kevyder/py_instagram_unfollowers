import pickle
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from constants import INSTAGRAM_URL, COOKIE_PATH


class NotUnfollowers:

    def set_chrome_options(self) -> Options:
        """Sets chrome options for Selenium.
        Chrome options for headless browser is enabled.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("enable-automation")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--dns-prefetch-disable")
        chrome_options.add_argument("--disable-gpu")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        return chrome_options

    def __init__(self, username: str, password: str, account: str) -> None:
        self.driver = webdriver.Chrome(options=self.set_chrome_options())
        self.username = username
        self.password = password
        self.account_url = f'{INSTAGRAM_URL}/{account}'
        self.not_following_back = list()

    def check(self) -> None:
        try:
            cookie_path = f'{COOKIE_PATH}{self.username}.pickle'
            cookies = pickle.load(open(cookie_path, "rb"))
            self.__go_to_home()
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except (OSError, IOError) as e:
            self.__login()
        finally:
            self.__get_unfollowers()
            self.driver.close()

    # Private methods

    def __login(self) -> None:
        try:
            self.__go_to_login()
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

    def __get_unfollowers(self) -> list:
        # Get following people
        self.__go_to_profile()
        following_element = self.driver.find_element(By.PARTIAL_LINK_TEXT, "following")
        following_element.click()
        following_list = self.__get_people()
        # Get followers
        self.__go_to_profile()
        followers_element = self.driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
        followers_element.click()
        followers_list = self.__get_people()
        # Get not following people in list
        not_following_back = [user for user in following_list if user not in followers_list]
        # data in ordered list
        not_following_back.sort()

        self.not_following_back = not_following_back

        return not_following_back

    def __get_people(self) -> list:
        # Access scroll-box
        sleep(10)
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

    def __go_to_home(self) -> None:
        self.driver.get(INSTAGRAM_URL)
        sleep(10)

    def __go_to_login(self) -> None:
        self.driver.get(f'{INSTAGRAM_URL}/accounts/login/')
        sleep(10)

    def __go_to_profile(self) -> None:
        self.driver.get(self.account_url)
        sleep(10)

    def __save_cookies(self) -> None:
        cookie_path = f'{COOKIE_PATH}{self.username}.pickle'
        pickle.dump(self.driver.get_cookies(), open(cookie_path, "wb"))

