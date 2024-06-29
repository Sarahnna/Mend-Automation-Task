# Bitbucket Automation Testing

This project automates tasks on Bitbucket, covering both UI testing using Selenium and API testing using the Bitbucket REST API. The tests are written in Python and use the `pytest` framework.

## Dependencies

To run this project, you need to install the following dependencies:


- `pytest`
- `selenium`
- `requests`
- `pytest-html`

You can install these dependencies using `pip` by using requirements.txt:

```sh
pip install -r requirements.txt
```

## Configuration

The `config.ini` file in the project root directory should be updated with your configuration details.
Consider changing `API_TOKEN` to your bitbucket token and the `driver_path` to point to your chromedriver executable.

## Running the Tests
To run all tests, use the following command:
```sh
pytest --html=report.html
```

This command will generate an HTML report named `report.html` in the project root directory.