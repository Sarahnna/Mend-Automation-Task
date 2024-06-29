import pytest
from api_tests.api_utils import BitbucketAPI
from helper import generate_random_string


@pytest.mark.usefixtures("bitbucket_api_creds")
class TestBitbucketAPI:
    bitbucket_url = "https://api.bitbucket.org/2.0"
    workspace = "mend_test"

    @pytest.mark.test
    def test_api_repositories(self, bitbucket_api_creds):
        # Init api object
        bitbucket_api = BitbucketAPI(self.bitbucket_url, bitbucket_api_creds)

        # Print all repos inside workspace
        repos = bitbucket_api.get_all_repositories(self.workspace)
        print("Repository names:")
        print("\n".join(repos))

        # Create new repo
        repo_name = f"api_repo_{generate_random_string()}"
        bitbucket_api.create_repository(self.workspace, repo_name)

        # Validate the repo is created
        repos = bitbucket_api.get_all_repositories(self.workspace)
        assert repo_name in repos, f"Repository {repo_name} was not created successfully"

        # Delete repo
        bitbucket_api.delete_repository(self.workspace, repo_name)

        # Validate the repo is deleted
        repos = bitbucket_api.get_all_repositories(self.workspace)
        assert repo_name not in repos, f"Repository {repo_name} was not deleted successfully"

    @pytest.mark.test
    def test_delete_repositories(self, bitbucket_api_creds):
        bitbucket_api = BitbucketAPI(self.bitbucket_url, bitbucket_api_creds)
        repos = bitbucket_api.get_all_repositories(self.workspace)
        # Delete each repository
        for repo_name in repos:
            bitbucket_api.delete_repository(self.workspace, repo_name)
