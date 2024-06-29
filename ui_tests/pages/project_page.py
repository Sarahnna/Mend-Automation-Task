from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class ProjectPage(BasePage):
    def __init__(self):
        self.projects_link = (By.LINK_TEXT, "Projects")
        self.mend_automation_project_link = (By.LINK_TEXT, "Mend Automation")
        self.create_dropdown_button = (By.ID, "createGlobalItem")
        self.create_repo_option = (By.CSS_SELECTOR, '[data-testid="repository-create-item"]')
        self.repo_name_input = (By.NAME, "name")
        self.repo_list = (By.CSS_SELECTOR, 'tbody tr td a[href*="/mend_test"]')
        self.project_dropdown = (By.ID, "s2id_id_project")
        self.readme_dropdown = (By.ID, "s2id_id_readme_type")
        self.mend_automation_option = (By.XPATH, '//span[text()="Mend Automation"]')
        self.no_option = (By.XPATH, '//div[contains(text(), "No")]')
        self.create_repo_button = (By.CSS_SELECTOR, 'button[type="submit"].aui-button-primary')

    def navigate_to_project(self):
        self.click_on_element(self.projects_link)
        self.click_on_element(self.mend_automation_project_link)

    def create_repository(self, repo_name):
        self.click_on_element(self.create_dropdown_button)
        self.click_on_element(self.create_repo_option)
        self.click_on_element(self.project_dropdown)
        self.click_on_element(self.mend_automation_option)
        self.send_keys_to_element(self.repo_name_input, repo_name)
        self.click_on_element(self.readme_dropdown)
        self.click_on_element(self.no_option)
        self.click_on_element(self.create_repo_button)

    def navigate_to_repository(self, repo_name):
        self.navigate_to_project()
        try:
            # Wait for the repository list to be visible
            WebDriverWait(self.get_driver(), 10).until(
                EC.visibility_of_element_located(self.repo_list)
            )
            repo_link = self.scroll_until_element_is_found((By.XPATH, f'//a[contains(@href, "{repo_name.lower()}")]'))
            repo_link.click()
        except TimeoutException:
            raise TimeoutException("Repository list not loaded or repository not found")

    def verify_repository_exists(self, repo_name):
        self.navigate_to_project()
        WebDriverWait(self.get_driver(), 10).until(
            EC.visibility_of_element_located(self.repo_list)
        )
        repos = self.get_driver().find_elements(*self.repo_list)
        return any(repo_name in repo.text for repo in repos)
