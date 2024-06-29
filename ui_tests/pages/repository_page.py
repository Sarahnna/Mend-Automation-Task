from selenium.common.exceptions import TimeoutException

from .base_page import BasePage
from selenium.webdriver.common.by import By


class RepositoryPage(BasePage):
    def __init__(self):
        self.create_branch_button = (By.ID, "open-create-branch-modal")
        self.branch_name_input = (By.NAME, "branchName")
        self.add_file_button = (By.XPATH, '//span[text()="Add file"]')
        self.filename_input = (By.ID, "filename")
        self.file_content_area = (By.CLASS_NAME, 'CodeMirror')
        self.commit_button = (By.CLASS_NAME, "save-button")
        self.changes_commit_button = (By.CLASS_NAME, "commit-button")
        self.merge_button = (By.ID, "merge-button")
        self.branches_link = (By.LINK_TEXT, "Branches")
        self.source_link = (By.LINK_TEXT, "Source")
        self.create_branch_submit_button = (By.CSS_SELECTOR, 'button[type="submit"]')
        self.three_dots_button = (By.CSS_SELECTOR, 'span[aria-label="Repository actions"]')
        self.branch_selector = (By.CSS_SELECTOR, 'button[data-testid="ref-selector-trigger"]')
        self.branches_type_selector = (By.XPATH, '//div[text()="Active branches"]')
        self.all_branches = (By.XPATH, '//*[text()="All branches"]')
        self.three_dots = (By.CSS_SELECTOR, 'span[aria-label="more"]')
        self.merge_button = (By.XPATH, '//span[text()="Merge"]')
        self.readme_container = (By.CSS_SELECTOR, 'article[data-qa="readme-container"]')

    def create_branch(self, branch_name):
        self.click_on_element(self.branches_link)
        self.click_element_if_exists((By.XPATH, '//span[text()="Accept all"]'))
        self.click_on_element(self.create_branch_button)
        self.send_keys_to_element(self.branch_name_input, branch_name)
        self.click_on_element(self.create_branch_submit_button)
        self.wait_for_element((By.XPATH, f'//h1[text()="{branch_name}"]'))

    def select_branch(self, branch_name):
        self.click_on_element(self.source_link)
        self.click_on_element(self.branch_selector)
        elem_locator = (By.XPATH, f'//a[text()="{branch_name}"]')
        self.click_on_element(elem_locator)

    def add_readme(self, content):
        self.click_on_element(self.source_link)
        self.click_on_element(self.three_dots_button)
        self.click_on_element(self.add_file_button)
        self.set_code_mirror_content(content)
        self.send_keys_to_element(self.filename_input, "README.md")
        self.click_on_element(self.commit_button)
        self.click_on_element(self.changes_commit_button)
        self.wait_for_element(self.branch_selector)

    def merge_branch(self, branch_name):
        self.click_on_element(self.branches_link)
        self.click_on_element(self.branches_type_selector)
        self.click_on_element(self.all_branches)
        elem_locator = (By.XPATH, f'//a[text()="{branch_name}"]')
        self.click_on_element(elem_locator)
        self.click_on_element(self.three_dots)
        self.click_on_element(self.merge_button)
        self.click_on_element(self.merge_button)

    def set_code_mirror_content(self, content):
        code_mirror = self.wait_for_element(self.file_content_area)
        self.get_driver().execute_script("""
            var codeMirror = arguments[0].CodeMirror;
            codeMirror.setValue(arguments[1]);
        """, code_mirror, content)

    def verify_branch_creation(self, branch):
        try:
            self.wait_for_element((By.XPATH, f'//h1[text()="{branch}"]'))
        except TimeoutException:
            return False
        return True

    def verify_readme_exists(self, text):
        try:
            element = self.wait_for_element(self.readme_container)
            if element.text == text:
                return True
        except TimeoutException:
            return False
        return False
