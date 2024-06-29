import requests


class BitbucketAPI:
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    def get_all_repositories(self, workspace):
        url = f"{self.base_url}/repositories/{workspace}"
        response = requests.get(url, auth=self.auth)
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        repositories = response.json().get('values', [])
        repo_names = [repo['slug'] for repo in repositories]
        return repo_names

    def create_repository(self, workspace, repo_name):
        url = f"{self.base_url}/repositories/{workspace}/{repo_name}"
        payload = {}
        response = requests.post(url, auth=self.auth, json=payload)
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    def delete_repository(self, workspace, repo_name):
        url = f"{self.base_url}/repositories/{workspace}/{repo_name}"
        response = requests.delete(url, auth=self.auth)
        assert response.status_code == 204, f"Expected status code 204 but got {response.status_code}"
