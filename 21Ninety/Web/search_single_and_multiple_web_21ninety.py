import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url_21ninety = "https://staging.21ninety.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
   'os_version': '10',
   'resolution': '1920x1080',
   'browser': 'Chrome',
   'browser_version': '94.0',
   'os': 'Windows',
   'name': 'BStack-[Python] Smoke Test for 21ninety.com search functionality is as expected or not on desktop',
   'build': 'BStack Build Number'
}

desired_cap["chromeOptions"] = {}
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)


def environment():
    driver.maximize_window()
    driver.get(url_21ninety)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 20).until(ec.title_is("21Ninety"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for 21ninety.com, for web, took too long but no response, checking title"}}')
        driver.quit()


def verify_search(search_text):
    print("in the function verify_search section")
    search_btn = driver.find_element(By.XPATH, "//nav[@class='navbar position-sticky text-black']//button[2]")
    search_btn.click()
    WebDriverWait(driver, 5).until(
      ec.presence_of_element_located((
        By.XPATH, "//label[normalize-space()='SEARCH']")))
    input_txt = driver.find_element(By.XPATH, "//input[@placeholder='Type search term...']")
    input_txt.clear()
    input_txt.send_keys(search_text)
    input_txt.send_keys(Keys.ENTER)
    WebDriverWait(driver, 20).until(ec.title_is("Search - 21Ninety"))
    driver.back()
    WebDriverWait(driver, 20).until(ec.title_is("21Ninety"))
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for windows desktop, on 21ninety.com search functionality with search text as:'+search_text+
      ' do work as expected"}}')


def post_page_load_pop_up():
    print("close popups in web view")
    try:
        btn_close = driver.find_element(By.XPATH, "(//button[@type='button'][normalize-space()='×'])[1]")
        btn_close.click()
    except NoSuchElementException:
        print("event promo pop-up does not exist")
    try:
        footer_xpath = driver.find_element(By.XPATH, "//button[text()='Accept']")
        driver.execute_script("arguments[0].click();", footer_xpath)
    except NoSuchElementException:
        print("21ninety footer cookies pop-up does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for desktop, on 21ninety.com search section do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_search("culture")
verify_search("black culture")
set_status()
driver.quit()
