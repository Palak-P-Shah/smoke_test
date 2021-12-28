import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = False
options.add_argument("--disable-notifications")
url_blavity = "https://blavity.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
   'os_version': '10',
   'resolution': '1920x1080',
   'browser': 'Chrome',
   'browser_version': '94.0',
   'os': 'Windows',
   'name': 'BStack-[Python] Smoke Test for blavity.com in carousel for left and right arrows',  # test name
   'build': 'BStack Build Number'  # CI/CD job or build name
}
desired_cap['browserstack.debug'] = True
desired_cap["chromeOptions"] = {}
# desired_cap["chromeOptions"]["excludeSwitches"] = ["disable-popup-blocking"]
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


def verify_scroll_right(count):
    print("inside function verify_scroll_right")
    temp = 0
    while temp < (count + 1):
        print("inside the while temp variable value is ", temp)
        # click on the left click button (temp) number of times
        # time.sleep(3)
        right_arrow = driver.find_element(By.XPATH, "//button[@id='home-hero-slick-arrow-next']")
        right_arrow.click()
        # driver.execute_script("arguments[0].click();", right_click)
        time.sleep(1)
        temp += 1
        print("clicked the right icon number of times :- ", temp)


def verify_scroll_left(count):
    print("inside function verify_scroll_left")
    temp = 0
    while count > temp:
        print("inside the while temp variable value is ", temp)
        # click on the left click button (temp) number of times
        # time.sleep(3)
        left_arrow = driver.find_element(By.XPATH, "//button[@id='home-hero-slick-arrow-prev']")
        left_arrow.click()
        # driver.execute_script("arguments[0].click();", right_click)
        time.sleep(1)
        temp += 1
        print("clicked the left arrow icon number of times :- ", temp)


def verify_scroll_carousel():
    print("function called scroll_carousel")
    number_of_entries = driver.find_elements(By.CLASS_NAME, "home-hero-card__title-wrapper")
    assert len(number_of_entries) > 0, "articles are not present in carousel"
    print("number of entries in Carousel are :- ", len(number_of_entries))
    left_click_button = driver.find_element(By.XPATH, "//button[@id='home-hero-slick-arrow-prev']")
    assert left_click_button.is_displayed(), "left click arrow button is not displayed in carousel"
    right_click_button = driver.find_element(By.XPATH, "//button[@id='home-hero-slick-arrow-next']")
    assert right_click_button.is_displayed(), "right click arrow button is not displayed in carousel"
    if left_click_button.is_displayed() and right_click_button.is_displayed():
        print("both right and left click buttons are displayed on this page")
    count = 0
    temp_num = len(number_of_entries)
    while count < len(number_of_entries):
        # time.sleep(2)
        verify_scroll_right(count)
        count += 1
        # print("temp_num :", temp_num)
    print("after while loop 1, count", count)
    while temp_num > 0:
        left_arrow = driver.find_element(By.XPATH, "//button[@id='home-hero-slick-arrow-prev']")
        left_arrow.click()
        time.sleep(1)
        # print("clicked the left arrow icon number of times :- ", temp_num)
        temp_num -= 1
        print("second while loop temp_num :", temp_num)
    print("after while loop 2, temp_num", temp_num)


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


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for desktop, in carousel left and right arrow '
      'Links for blavity do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_scroll_carousel()
set_status()
driver.quit()
