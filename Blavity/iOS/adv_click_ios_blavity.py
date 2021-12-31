import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


url_blavity = "https://blavity.com/"
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
   'name': 'BStack-[Python] Smoke Test for blavity.com ads working as expected on ios safari',  # test name
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
        WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for blavity.com, for ios safari, took too long but no response, checking title"}}')
        driver.quit()


def verify_adv():
    print("function called verify_adv")
    time.sleep(2)
    number_of_entries = driver.find_elements(By.CLASS_NAME, "home-hero-card__title-wrapper")
    print(len(number_of_entries))
    # time.sleep(3)
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((
      By.TAG_NAME,
      "iframe")))
    iframe = driver.find_element(
      # By.XPATH,
      # "(//iframe[@id='google_ads_iframe_/11462305847/bla/home_0'])[1]")
       By.TAG_NAME,
       "iframe")
    # driver.execute_script("arguments[0].scrollIntoView();", iframe)
    # actions = ActionChains(driver)
    # actions.move_to_element(iframe[0]).perform()
    time.sleep(1)
    # iframe[1].click()

    driver.execute_script('''window.open("", "_blank");''')

    driver.execute_script("arguments[0].click();", iframe)
    time.sleep(2)
    # driver.switch_to.frame(iframe)
    # img = driver.find_element(By.XPATH, "//img[@class='img_ad']")
    # driver.execute_script("arguments[0].scrollIntoView();", img)
    # actions = ActionChains(driver)
    # actions.move_to_element(img).perform()
    # img.click()
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 40).until(ec.presence_of_element_located((By.XPATH, "/html/head/title")))
    print("Current window title: " + driver.title)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.default_content()
    print("initial adv tested")
    second_iframe = driver.find_element(By.XPATH, "(//iframe[@id='google_ads_iframe_/11462305847/bla/home_1'])[1]")
    driver.switch_to.frame(second_iframe)
    img_second = driver.find_element(By.XPATH, "//img[@class='img_ad']")
    actions = ActionChains(driver)
    actions.move_to_element(img_second).perform()
    img_second.click()
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 40).until(ec.presence_of_element_located((By.XPATH, "/html/head/title")))
    print("Current window title: " + driver.title)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("second adv tested")


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
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("blavity footer adv does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", ads on the '
      ' blavity.com do work as expected on ios safari."}}')


environment()
page_load()
post_page_load_pop_up()
verify_adv()
set_status()
driver.quit()
