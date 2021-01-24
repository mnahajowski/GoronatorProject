from selenium import webdriver
from selenium.webdriver.common.keys import Keys

BASE_URL = "http://localhost:5000/"
CHROMEDRIVER_PATH = r"C:\Users\ewa-m\Desktop\chromedriver.exe"


def test_browser_full_point_name():
    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)
        browser = chrome.find_element_by_id("tags")
        browser.send_keys("Rysy")
        browser.send_keys(Keys.ENTER)

        point_name = chrome.find_element_by_class_name("importantLabel").text
        url = chrome.current_url

    assert point_name == "Rysy"
    assert url == BASE_URL + "point/3"


def test_browser_selection():
    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)
        browser = chrome.find_element_by_id("tags")
        browser.send_keys("Rys")

        chrome.implicitly_wait(1)

        chrome.find_element_by_class_name("ui-menu-item").click()

        point_name = chrome.find_element_by_class_name("importantLabel").text
        url = chrome.current_url

    assert point_name == "Rysy"
    assert url == BASE_URL + "point/3"


def test_browser_selection_invalid_data():
    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)
        browser = chrome.find_element_by_id("tags")
        browser.send_keys("Invalid data")

        browser.send_keys(Keys.ENTER)

        url = chrome.current_url

    assert url == BASE_URL

