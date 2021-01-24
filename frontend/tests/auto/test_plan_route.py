from selenium import webdriver

import requests
import json
import time

TOURIST = 1
BASE_URL = "http://localhost:5000/route"
BROWSER_URL = "http://localhost:5000/"
API_URL = 'http://localhost:5001'
CHROMEDRIVER_PATH = r"C:\Users\ewa-m\Desktop\chromedriver.exe"


def test_plan_route():
    response = requests.get(API_URL + f"/routes/{TOURIST}")
    route_count = len(json.loads(response.content)['routes'])

    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)

        for _ in range(3):
            add_segment = chrome.find_element_by_class_name("plusButton")
            add_segment.click()

            time.sleep(3)
            segments = chrome.find_elements_by_class_name("correlledSegments")
            segments[0].click()
            chrome.find_elements_by_class_name("checkbtn")[0].click()

        chrome.find_element_by_id("save-icon").click()

        response = requests.get(API_URL + f"/routes/{TOURIST}")
        route_count_after = len(json.loads(response.content)['routes'])

    assert route_count_after == route_count + 1


def test_plan_route_exit():
    with webdriver.Chrome(CHROMEDRIVER_PATH) as chrome:
        chrome.get(BASE_URL)

        exit_button = chrome.find_elements_by_css_selector("button img")[1]
        exit_button.click()

        chrome.find_element_by_id("modal-ok-button").click()

        url = chrome.current_url

    assert url == BROWSER_URL
