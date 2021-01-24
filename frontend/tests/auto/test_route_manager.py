from selenium import webdriver

import requests
import json
import time

ICON_GREY = "share-icon-grey"
TOURIST = 1
TEST_ROUTE = 52
BASE_URL = f"http://localhost:5000/routes/{TOURIST}/{TEST_ROUTE}"
DOCUMENTATION_URL = f"http://localhost:5000/route/{TOURIST}/{TEST_ROUTE}/documentation"
PLAN_URL = "http://localhost:5000/route"
API_URL = 'http://localhost:5001'
CHROMEDRIVER_PATH = r"C:\Users\ewa-m\Desktop\chromedriver.exe"


def test_route_manager_plan_route():
    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)

        add_route_button = chrome.find_element_by_class_name("menu-plus")
        add_route_button.click()

        url = chrome.current_url

    assert url == PLAN_URL


def test_route_manager_verification():
    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)

        add_route_button = chrome.find_element_by_id("verification-icon")
        add_route_button.click()

        chrome.find_element_by_id("modal-ok-button").click()

        icon_name = chrome.find_element_by_id("verification-icon").get_attribute("src")

    assert ICON_GREY in icon_name


def test_route_manager_documentation():
    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)

        add_route_button = chrome.find_element_by_id("documentation-icon")
        add_route_button.click()

        url = chrome.current_url

    assert url == DOCUMENTATION_URL


def test_route_manager_edit_name():
    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)

        name_input = chrome.find_element_by_id("route-name")
        name_input.clear()
        new_name = f"Trasa na Rysy {time.time_ns()}"
        name_input.send_keys(new_name)

        save = chrome.find_element_by_id("save-icon")
        save.click()

        time.sleep(5)

        response = requests.get(API_URL + f"/route/full/{TEST_ROUTE}")
        route_name = json.loads(response.content)['name']

    assert new_name == route_name

