import pytest
import configparser
import os
from selenium import webdriver
from ui_tests.pages.base_page import BasePage

# Determine the absolute path to the project's root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Read configuration
config = configparser.ConfigParser()
config_path = os.path.join(ROOT_DIR, 'config.ini')
config.read(config_path)


@pytest.fixture(scope="session")
def init():
    driver_path = config.get('selenium', 'driver_path')
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.maximize_window()
    BasePage.set_driver(driver)
    driver.get(config.get('selenium', 'url'))
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def bitbucket_site_creds():
    email = config.get('bitbucket_creds', 'email')
    password = config.get('bitbucket_creds', 'password')
    return email, password


@pytest.fixture(scope="session")
def bitbucket_api_creds():
    username = config.get('bitbucket_api', 'username')
    password = config.get('bitbucket_api', 'password')
    return username, password
