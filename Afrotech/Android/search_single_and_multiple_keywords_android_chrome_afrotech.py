import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver


url_afrotech = "https://afrotech.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
    'os_version': '10.0',
    'device': 'Google Pixel 3',
    'real_mobile': 'true',
    'browserstack.local': 'false',
    'browserName': 'Chrome',
    'browser_version': 'latest',
    'os': 'Android',
    'name': 'BStack-[Python] Smoke Test for travelnoire.com '
           'search functionality do work as expected or not on android chrome',  # test name
    'build': 'BStack Build Number'
}

desired_cap["chromeOptions"] = {}
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)


def environment():
    driver.get(url_afrotech)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 40).until(ec.title_is("AfroTech"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for afrotech.com, for android chrome, '
          'took too long but no response, checking title"}}')
        driver.quit()


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
        print("afrotech cookies footer pop-up does not exist")


def verify_nav_search_bar(search_text):
    search_bar = driver.find_element(
      By.XPATH,
      "(//button[@class='btn bg-transparent border-0 color-black font-size-0 p-0 position-absolute'])[1]")
    post_page_load_pop_up()
    assert search_bar.is_displayed(), "Search Bar is not displayed"
    search_bar.click()
    input = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    input.send_keys(search_text)
    post_page_load_pop_up()
    search_bar.click()
    time.sleep(2)
    if driver.title == "Error - AfroTech":
        post_page_load_pop_up()
        print("Current window title for Search Page is: " + driver.title)
        page_header_error = driver.find_element(
          By.XPATH,
          "//h1[normalize-space()='Something went wrong, we will update soon']")
        if page_header_error.is_displayed():
             driver.execute_script(
             'browserstack_executor: {"action": "setSessionStatus", "arguments": '
             '{"status":"failed", "reason": ", for android chrome, for the search text : ' + search_text +
             ' on afrotech.com does not work as expected."}}')
    else:
        print("Title does not contain error, test pass")
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"passed", "reason": ", for android chrome, for the search text : ' + search_text +
          ' on afrotech.com work as expected."}}')

    main_page = driver.find_element(
      By.XPATH,
      "(//div[@class='navbar__brand d-flex align-items-center justify-content-center "
      "justify-content-desktop-start'])[1]")
    main_page.click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(ec.title_is("AfroTech"))


environment()
page_load()
post_page_load_pop_up()
verify_nav_search_bar("google")
verify_nav_search_bar("google microsoft")
driver.quit()
