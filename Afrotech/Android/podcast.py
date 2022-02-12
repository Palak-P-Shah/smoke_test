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
    'name': 'BStack-[Python] Smoke Test for afrotech.com for podcast is as expected on android chrome',
    'build': 'BStack Build Number'
}

desired_cap["chromeOptions"] = {}
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def environment():
    # driver.maximize_window()
    driver.get(url_afrotech)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 20).until(ec.title_is("AfroTech"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for afrotech.com, for android chrome, '
          'took too long but no response, checking title"}}')
        driver.quit()


def verify_podcast():
    post_page_load_pop_up()
    print("in the function verify_podcast")
    nav_bar = driver.find_element(
      By.XPATH,
      "(//button[@class='navbar__toggler bg-transparent border-0 d-desktop-none text-center'])[1]")
    nav_bar.click()
    podcast = driver.find_element(By.XPATH, "//a[normalize-space()='Podcast']")
    actions = ActionChains(driver)
    actions.move_to_element(podcast).perform()
    assert podcast.is_displayed(), "'PODCAST' heading is not displayed"
    post_page_load_pop_up()
    podcast.click()
    # switch to the new tab being opened.
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 10).until(ec.title_is(
      "Black Tech Green Money — Podcast For Black Techies With A Passion For Capital"))
    assert "Black Tech Green Money — Podcast For Black Techies With A Passion For Capital" in driver.title,\
        "title of podcast website does not match"
    time.sleep(1)
    listen_to_podcast = driver.find_element(By.XPATH, "(//div[@class='sqs-block-button-container--left']//a)[1]")
    actions = ActionChains(driver)
    actions.move_to_element(listen_to_podcast).perform()
    listen_to_podcast.click()
    WebDriverWait(driver, 10).until(
      ec.presence_of_element_located((By.XPATH, "(//div[@class='summary-thumbnail img-wrapper']//img)[1]")))
    time.sleep(2)
    first_podcast = driver.find_element(
      By.XPATH,
      "(//div[@class='summary-thumbnail img-wrapper']//img)[1]")
    actions = ActionChains(driver)
    actions.move_to_element(first_podcast).perform()
    assert first_podcast.is_displayed(), "'Listen To Podcast' heading is not displayed"
    first_podcast.click()
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((
      By.XPATH, "//div[@class='blog-item-title']//h1"
    )))
    frame = driver.find_element(By.XPATH, "//div[@class='sqs-block-content']//iframe")
    driver.switch_to.frame(frame)
    time.sleep(2)
    play = driver.find_element(By.XPATH, "//img[@class='Player__play-icon']")
    actions = ActionChains(driver)
    actions.move_to_element(play).perform()
    play.click()


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
      '{"status":"passed", "reason": ", for android chrome, on afrotech.com podcast do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_podcast()
set_status()
driver.quit()
