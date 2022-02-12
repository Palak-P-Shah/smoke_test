import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


url_21ninety = "https://staging.21ninety.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
   'os_version': '10',
   'resolution': '1920x1080',
   'browser': 'Chrome',
   'browser_version': '94.0',
   'os': 'Windows',
   'name': 'BStack-[Python] Smoke Test for 21ninety.com featured video is as expected or not on desktop',
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


def verify_featured():
    print("in the function verify_featured")
    featured = driver.find_element(By.XPATH, "//h3[normalize-space()='FEATURED VIDEOS']")
    actions = ActionChains(driver)
    actions.move_to_element(featured).perform()
    assert featured.is_displayed(), "'Featured' heading is not displayed"
    tmp = driver.find_elements(
      By.XPATH,
      "(//button[@class='video-card__play btn bg-white border-circle border-0 font-size-0 p-0 text-teal'])")
    temp_articles = len(tmp)
    assert temp_articles > 0 , "No videos are present under Featured videos section"
    print(temp_articles)
    video = driver.find_element(
      By.XPATH,
      "(//button[@class='video-card__play btn bg-white border-circle border-0 font-size-0 p-0 text-teal'])[1]")
    video.click()
    time.sleep(5)


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
      '{"status":"passed", "reason": ", for desktop, on 21ninety.com featured video do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_featured()
set_status()
driver.quit()
