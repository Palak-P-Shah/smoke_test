import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

desired_cap = {
 'os_version': '10.0',
  'device': 'Google Pixel 3',
  'real_mobile': 'true',
  'browserstack.local': 'false',
  'browserName': 'Chrome',
  # 'resolution': '1920x1080',
  # 'browser': 'Chrome',
  'browser_version': 'latest',
  'os': 'Android',
 'build': 'Python Sample Build',
 'name': 'Pop-ups testing mobile android'
}
desired_cap["chromeOptions"] = {}
# desired_cap["chromeOptions"]["excludeSwitches"] = ["disable-popup-blocking"]
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]

url_blavity = "https://blavity.com/"
driver = webdriver.Remote(
    command_executor='https://palakshah_rcAxD5:s2rqmyxFs8r999bzvGXJ@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap
    )


def environment():
    # driver.maximize_window()
    driver.get(url_blavity)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": in android chrome for blavity.com, took too long but no response, checking title"}}')
        driver.quit()


def post_page_load_pop_up():
    print("accept popups in mobile view")
    try:
        btn_close = driver.find_element(By.XPATH, "(//button[@type='button'][normalize-space()='×'])[1]")
        btn_close.click()
    except NoSuchElementException:
        print("event promo pop-up does not exist")
    try:
        footer_xpath = driver.find_element(By.XPATH, "//button[text()='Accept']")
        driver.execute_script("arguments[0].click();", footer_xpath)
    except NoSuchElementException:
        print("blavity footer cookies pop-up does not exist")
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("blavity footer adv does not exist")



environment()
page_load()
post_page_load_pop_up()
driver.quit()
