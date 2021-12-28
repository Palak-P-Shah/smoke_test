import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver


url_blavity = "https://afrotech.com/"
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
   'name': 'BStack-[Python] Smoke Test for afrotech.com in carousel for left and right slide',  # test name
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
    driver.get(url_blavity)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 40).until(ec.title_is("AfroTech"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for afrotech.com, for web, took too long but no response, checking title"}}')
        driver.quit()


def verify_scroll_carousel():
    print("function called scroll_carousel")
    temp = driver.find_elements(By.XPATH, "//div[@class='slick-slide slick-cloned']")
    print(len(temp))
    number_of_entries = int((len(temp)-1)/2)
    print(number_of_entries)
    count = 0
    while count < number_of_entries:
        post_page_load_pop_up()
        tmp_str = "(//div[@class='hero-card'])["+str(count+2)+"]"
        print(tmp_str)
        right_article = driver.find_element(By.XPATH, tmp_str)
        actions = ActionChains(driver)
        actions.move_to_element(right_article).perform()
        count += 1
        time.sleep(1)
        print("clicked :", count)
    print("after while loop 1, count", count)
    while count > 0:
        # post_page_load_pop_up()
        left_article = driver.find_element(By.XPATH, "(//div[@class='hero-card'])["+str(count+2)+"]")
        actions = ActionChains(driver)
        actions.move_to_element(left_article).perform()
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
        print("afrotech footer pop-up does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for android on chrome browser, in carousel left and right slide move'
      'for afrotech do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_scroll_carousel()
set_status()
driver.quit()
