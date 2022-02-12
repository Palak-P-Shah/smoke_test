import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.headless = False
options.add_argument("--disable-notifications")
options.add_argument('--start-maximized')
# options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")

user_agent = \
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 PTST/1.0'
options.add_argument('user-agent={0}'.format(user_agent))


url_podcast = "https://playlist.megaphone.fm/?e=HSW1277424227&wmode=opaque"
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
   'name': 'BStack-[Python] Smoke Test for shadowandact.com for podcast is as expected on ios safari',
   'build': 'BStack Build Number'
}

desired_cap["chromeOptions"] = {}
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def environment():
    driver.get(url_podcast)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 20).until(ec.title_is("SHADOW & ACT"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for shadowandact.com, for ios safari, '
          'took too long but no response, checking title"}}')
        driver.quit()


def verify_podcast():
    print("in the function verify_podcast")
    time.sleep(5)
    play = driver.find_element(By.XPATH, "//div[@class='Player__play-btn']")
    # actions = ActionChains(driver)
    # actions.move_to_element(play).perform()
    # post_page_load_pop_up()
    # play.click()
    driver.execute_script("arguments[0].click();", play)
    time.sleep(3)


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
        print("afrotech footer cookies pop-up does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for ios safari, on afrotech.com podcast do work as expected"}}')


environment()
# page_load()
post_page_load_pop_up()
verify_podcast()
set_status()
driver.quit()
