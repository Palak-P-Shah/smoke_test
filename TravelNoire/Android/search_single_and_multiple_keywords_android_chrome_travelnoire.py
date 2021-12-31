import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver


url_travelnoire = "https://travelnoire.com/"
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
           'search functionality do work as expected for single and multiple keywords',  # test name
   'build': 'BStack Build Number'
}

desired_cap["chromeOptions"] = {}
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)


def environment():
    driver.get(url_travelnoire)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 40).until(ec.title_is("Travel Noire"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for travelnoire.com, for android chrome, '
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
        print("travelnoire cookies footer pop-up does not exist")
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("travelnoire footer adv does not exist")


def verify_nav_search_bar(search_text):
    search_bar = driver.find_element(
      By.XPATH,
      "(//button[@type='submit'])[2]")
    assert search_bar.is_displayed(), "Search Bar is not displayed"
    search_bar.click()
    input = driver.find_element(By.XPATH, "(//input[@placeholder='Search'])[2]")
    input.send_keys(search_text)
    search_bar.click()
    time.sleep(2)
    if driver.title == "Travel Noire - Travel Noire":
        print("Current window title for Search Page is: " + driver.title)
        page_header_error = driver.find_element(
          By.XPATH,
          "//h1[normalize-space()='Something went wrong, we will update soon']")
        if page_header_error.is_displayed():
             driver.execute_script(
             'browserstack_executor: {"action": "setSessionStatus", "arguments": '
             '{"status":"failed", "reason": ", on android chrome, for the search text : ' + search_text +
             ' on travelnoire.com does not work as expected."}}')
        else:
            print("Something went wrong Page Header is not displayed, test pass")
    main_page = driver.find_element(
      By.XPATH,
      "(//a[@class='d-inline-block font-size-0 nuxt-link-active'])[1]")
    main_page.click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(ec.title_is("Travel Noire"))


environment()
page_load()
post_page_load_pop_up()
verify_nav_search_bar("colombia")
verify_nav_search_bar("Puerto Rico")
driver.quit()
