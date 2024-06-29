import pytest
from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.project_page import ProjectPage
from ui_tests.pages.repository_page import RepositoryPage
from helper import generate_random_string


@pytest.mark.usefixtures("init", "bitbucket_site_creds")
class TestBitbucketUI:

    @pytest.mark.test
    def test_bitbucket_ui(self, bitbucket_site_creds):
        repo_name = f"test_repo_{generate_random_string()}"
        branch_name = f"test_branch_{generate_random_string()}"
        username = bitbucket_site_creds[0]
        password = bitbucket_site_creds[1]

        login_page = LoginPage()
        project_page = ProjectPage()
        repository_page = RepositoryPage()

        # Login to bitbucket
        login_page.login(username, password)
        assert login_page.verify_login_success(), "Login failed"

        # Navigate to project and create new repo
        project_page.navigate_to_project()
        project_page.create_repository(repo_name)
        assert project_page.verify_repository_exists(repo_name), "Repository creation failed"

        # Create new branch
        project_page.navigate_to_repository(repo_name)
        repository_page.create_branch(branch_name)
        assert repository_page.verify_branch_creation(branch_name), "Branch creation failed"

        # Create README file
        repository_page.select_branch(branch_name)
        content = "This is readme file"
        repository_page.add_readme(content)
        repository_page.select_branch(branch_name)
        assert repository_page.verify_readme_exists(content), "Readme file creation failed"

        # Merge and logout
        repository_page.merge_branch(branch_name)
        login_page.logout()