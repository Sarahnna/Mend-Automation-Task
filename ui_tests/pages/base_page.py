import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class BasePage:
    driver = None

    @classmethod
    def set_driver(cls, driver):
        cls.driver = driver

    @classmethod
    def get_driver(cls):
        if cls.driver is None:
            raise Exception("Driver is not set!")
        return cls.driver

    @classmethod
    def wait_for_element(cls, by_locator):
        element = WebDriverWait(cls.get_driver(), 10).until(
            EC.visibility_of_element_located(by_locator)
        )
        WebDriverWait(cls.get_driver(), 10).until(
            EC.element_to_be_clickable(by_locator)
        )
        return element

    @classmethod
    def click_on_element(cls, by_locator):
        element = cls.wait_for_element(by_locator)
        element.click()

    @classmethod
    def send_keys_to_element(cls, by_locator, keys):
        element = cls.wait_for_element(by_locator)
        element.clear()
        element.send_keys(keys)

    @classmethod
    def get_element_text(cls, by_locator):
        element = cls.wait_for_element(by_locator)
        return element.text

    @classmethod
    def is_element_present(cls, by_locator):
        try:
            cls.wait_for_element(by_locator)
            return True
        except:
            return False

    @classmethod
    def scroll_until_element_is_found(cls, by_locator, timeout=10):
        driver = cls.get_driver()
        wait = WebDriverWait(driver, timeout)

        for attempt in range(timeout):
            try:
                element = wait.until(EC.presence_of_element_located(by_locator))
                # Move to the element to ensure it's visible
                ActionChains(driver).move_to_element(element).perform()
                return element
            except TimeoutException:
                # Scroll down a bit and retry
                driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(1)

        raise NoSuchElementException(f"Element with locator {by_locator} not found after {timeout} seconds")

    @classmethod
    def click_element_if_exists(cls, by_locator, timeout=5):
        driver = cls.get_driver()
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(by_locator)
            )
            element.click()
        except (NoSuchElementException, TimeoutException):
            pass  # Element not found or not visible within the timeout period, move on
