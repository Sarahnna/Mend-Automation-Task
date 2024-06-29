from selenium.common.exceptions import TimeoutException

from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class LoginPage(BasePage):
    def __init__(self):
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.submit_button = (By.ID, "login-submit")
        self.profile_button = (By.CSS_SELECTOR, 'button[data-testid="profile-button"]')
        self.logout_button = (By.XPATH, '//span[text()="Log out"]')
        self.login_button = (By.XPATH, '//a[text()="Log in"]')

    def login(self, username, password):
        self.click_on_element(self.login_button)
        self.send_keys_to_element(self.username_input, username)
        self.click_on_element(self.submit_button)
        self.send_keys_to_element(self.password_input, password)
        self.send_keys_to_element(self.password_input, Keys.RETURN)

    def logout(self):
        self.click_on_element(self.profile_button)
        self.click_on_element(self.logout_button)

    def verify_login_success(self):
        try:
            self.wait_for_element(self.profile_button)
        except TimeoutException:
            return False
        return True
