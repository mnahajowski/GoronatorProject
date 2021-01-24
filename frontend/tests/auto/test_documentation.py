from selenium import webdriver

import requests
import json

TEST_ROUTE = "Trasa testowa"

TEST_ROUTE_ID = 52
BASE_URL = f"http://localhost:5000/route/1/{TEST_ROUTE_ID}/documentation"
API_URL = 'http://localhost:5001'
CHROMEDRIVER_PATH = r"C:\Users\ewa-m\Desktop\chromedriver.exe"


def test_documentation_display():
    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)

        response = requests.get(API_URL + f"/documentation/{TEST_ROUTE_ID}")
        images_count = len(json.loads(response.content)['documentation'])

        displayed_images_count = len(chrome.find_elements_by_class_name("grid-elem")) - 1

    assert images_count == displayed_images_count


def test_documentation_menu():
    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)

        menu_items = chrome.find_elements_by_css_selector(".menu a")
        [test_route_link] = [item for item in menu_items if item.text == TEST_ROUTE]
        test_route_link.click()

        url = chrome.current_url

    assert url == BASE_URL.replace(str(TEST_ROUTE_ID), str(53))
