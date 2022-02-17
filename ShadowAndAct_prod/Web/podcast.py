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


url_shadowandact = "https://shadowandact.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
   'os_version': '10',
   'resolution': '1920x1080',
   'browser': 'Chrome',
   'browser_version': '94.0',
   'os': 'Windows',
   'name': 'BStack-[Python] Smoke Test for shadowandact.com for podcast is as expected on desktop',
   'build': 'BStack Build Number'
}

desired_cap["chromeOptions"] = {}
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def environment():
    driver.maximize_window()
    driver.get(url_shadowandact)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 20).until(ec.title_is("SHADOW & ACT"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for shadowandact.com, for web, '
          'took too long but no response, checking title"}}')
        driver.quit()


def verify_podcast():
    print("in the function verify_podcast")
    podcast = driver.find_element(By.XPATH, "//a[normalize-space()='PODCAST']")
    actions = ActionChains(driver)
    actions.move_to_element(podcast).perform()
    assert podcast.is_displayed(), "'PODCAST' heading is not displayed"
    podcast.click()
    # switch to the new tab being opened.
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 10).until(ec.title_is("Opening Act Podcast"))
    assert "Opening Act Podcast" in driver.title, "title of podcast website does not match"
    time.sleep(2)
    # WebDriverWait(driver, 10).until(ec.presence_of_element_located((
    #   By.CSS_SELECTOR, "(//img[@class='summary-thumbnail-image loaded'])[1]"
    # )))
    listen_to_podcast = driver.find_element(By.XPATH, "//div[@class='sqs-block-button-container--left']//a")
    actions = ActionChains(driver)
    actions.move_to_element(listen_to_podcast).perform()
    listen_to_podcast.click()
    driver.switch_to.window(driver.window_handles[2])
    WebDriverWait(driver, 10).until(ec.title_contains("Blog"))
    time.sleep(2)
    first_podcast = driver.find_element(
      By.XPATH,
      "(//article[@class='blog-basic-grid--container entry blog-item is-loaded']//div//a//img)[1]")
    actions = ActionChains(driver)
    actions.move_to_element(first_podcast).perform()
    assert first_podcast.is_displayed(), "'Listen To Podcast' heading is not displayed"
    text = driver.find_element(By.XPATH, "(//div[@class='blog-basic-grid--text']//h1//a)[1]")
    tmp_text = text.text
    first_podcast.click()
    # time.sleep(7)
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((
      By.XPATH, "//div[@class='blog-item-top-wrapper']//div//h1"
    )))
    frame = driver.find_element(By.XPATH, "//iframe[@title='Libsyn Player']")
    driver.switch_to.frame(frame)
    time.sleep(2)
    play = driver.find_element(By.XPATH, "//i[@class='play center-block fa fa-play-circle-o']")
    actions = ActionChains(driver)
    actions.move_to_element(play).perform()
    play.click()
    # WebDriverWait(driver, 10).until(ec.title_contains("Opening Act Podcast"))
    # time.sleep(2)
    # frame = driver.find_element(By.XPATH, "//iframe[@title='Libsyn Player']")
    # play = driver.find_element(By.XPATH, "play center-block fa fa-play-circle-o")
    # play.click()
    # time.sleep(2)

    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    # print("Instagram Link in Footer of TravelNoire Website is working as expected")


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
        print("shadowandact footer cookies pop-up does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for desktop, on shadowandact.com podcast do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_podcast()
set_status()
driver.quit()
