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
   'os_version': '14',
  'device': 'iPhone 12',
  'real_mobile': 'true',
  'browserstack.local': 'false',
  'browserName': 'safari',
  'browser_version': 'latest',
  'os': 'iOS',
   'name': 'BStack-[Python] Smoke Test for travelnoire.com in '
           'carousel for left and right slides on ios safari',  # test name
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
          '{"status":"failed", "reason": for travelnoire.com, for ios safari, '
          'took too long but no response, checking title"}}')
        driver.quit()


def verify_scroll_carousel():
    print("function called scroll_carousel")
    temp_number = driver.find_elements(By.XPATH, "(//a[@class='article-link home-hero-card__title text-uppercase'])")
    number_of_entries = int(len(temp_number)/3)
    print(number_of_entries)
    assert number_of_entries > 0, "articles are not present in carousel"
    print("number of entries in Carousel are :- ", int(number_of_entries))
    count = 8
    while count < 13:
        time.sleep(1)
        right_slide_button = driver.find_element(
          By.XPATH,
          "(//button[@class='home-hero__slick-arrow home-hero__slick-arrow--next bg-transparent btn font-size-0 p-0 "
          "position-absolute slick-arrow slick-next slick-arrow slick-next'])[1]")
        right_slide_button.click()
        print("clicked :", count)
        count += 1
    print("after while loop 1, count", count)
    count = count - 1
    while count > 7:
        left_slide_button = driver.find_element(
          By.XPATH,
          "(//button[@class='home-hero__slick-arrow home-hero__slick-arrow--prev bg-transparent btn font-size-0 p-0 "
          "position-absolute slick-arrow slick-prev slick-arrow slick-prev'])[1]")
        left_slide_button.click()
        time.sleep(1)
        count -= 1
        print("second while loop temp_num :", count)
    print("after while loop 2, temp_num", count)


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
        print("travelnoire cookies footer pop-up does not exist")
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("travelnoire footer adv does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for ios safari, in carousel left and right slides '
      'for travelnoire do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_scroll_carousel()
set_status()
driver.quit()
