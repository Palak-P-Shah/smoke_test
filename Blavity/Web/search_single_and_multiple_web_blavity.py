import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver


url_blavity = "https://blavity.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
   'os_version': '10',
   'resolution': '1920x1080',
   'browser': 'Chrome',
   'browser_version': '94.0',
   'os': 'Windows',
   'name': 'BStack-[Python] Smoke Test for blavity.com for differnt search text working as expected or not on desktop',
   'build': 'BStack Build Number'
}
desired_cap['browserstack.debug'] = True
desired_cap["chromeOptions"] = {}
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)


def environment():
    driver.maximize_window()
    driver.get(url_blavity)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for blavity.com, for web, took too long but no response, checking title"}}')
        driver.quit()


def post_page_load_pop_up():
    print("accept popups in web view")
    try:
        btn_close = driver.find_element(By.XPATH, "(//button[@type='button'][normalize-space()='×'])[1]")
        btn_close.click()
    except NoSuchElementException:
        print("event promo pop-up does not exist")
    try:
        footer_xpath = driver.find_element(By.XPATH, "//button[text()='Accept']")
        driver.execute_script("arguments[0].click();", footer_xpath)
    except NoSuchElementException:
        print("blavity footer pop-up does not exist")


def verify_nav_search_bar(input):
    search_bar = driver.find_element(
      By.CSS_SELECTOR,
      "button[class='btn btn--search bg-transparent border-0 text-right text-white position-absolute']")
    assert search_bar.is_displayed(), "Search Bar is not displayed"
    search_bar.click()
    input_search = driver.find_element(By.XPATH, "//input[@type='text']")
    search_text = input
    input_search.send_keys(search_text)
    search_bar.click()
    if input == 'culture':
        WebDriverWait(driver, 40).until(ec.url_contains(search_text))
        WebDriverWait(driver, 40).until(ec.title_is("Search - Blavity News"))
        assert driver.title == "Search - Blavity News", "title text does not match for search page"
        print("Current window title for Search Page is: " + driver.title)
        print("link for Search is present and working as expected")
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"passed", "reason": ", for desktop, for the search text culture on '
          ' blavity.com do work as expected."}}')
    elif input == 'Yolanda Baruch':
        WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
        print("Current window title for Search Page is: " + driver.title)
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": ", for desktop, for search text Yolanda Baruch on'
          ' blavity.com giving error as page not found."}}')


environment()
page_load()
post_page_load_pop_up()
verify_nav_search_bar("culture")
verify_nav_search_bar("Yolanda Baruch")
driver.quit()
