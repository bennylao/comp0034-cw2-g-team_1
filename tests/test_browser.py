import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
