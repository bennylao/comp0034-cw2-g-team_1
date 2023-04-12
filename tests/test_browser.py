from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import socket
import subprocess


@pytest.fixture(scope="module")
def flask_port():
    """Ask OS for a free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="module")
def run_app_win(flask_port):
    """Runs the Flask app for live server testing on Windows"""
    server = subprocess.Popen(
        [
            "flask",
            "--app",
            "crayfish_analysis_app:create_app('config.TestingConfig')",
            "run",
            "--port",
            str(flask_port),
        ]
    )
    try:
        yield server
    finally:
        server.terminate()

def test_home_page_title(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page title should be "Home"
    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)
    assert chrome_driver.title == "Home"


def test_link_to_dashboard(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page title should be "Home"
    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)
    link_to_dashboard = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]/div/a[2]'))
    )
    link_to_dashboard.click()
    current_url = chrome_driver.current_url
    assert current_url == f"http://localhost:{flask_port}/dashboard/"


def test_dashboard_title(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page title should be "Home"
    """
    url = f"http://localhost:{flask_port}/dashboard/"
    chrome_driver.get(url)
    heading = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="react-entry-point"]/div/div[1]/div/div/div/h1'))
    )
    assert heading.text == "Crayfish Analysis Dashboard"
