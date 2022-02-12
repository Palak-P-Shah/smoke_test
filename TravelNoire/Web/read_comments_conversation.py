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

url_travelnoire = "https://travelnoire.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
   'os_version': '10',
   'resolution': '1920x1080',
   'browser': 'Chrome',
   'browser_version': '94.0',
   'os': 'Windows',
   'name': 'BStack-[Python] Smoke Test for travelnoire.com '
           'read comments and conversation functionality do work as expected',  # test name
   'build': 'BStack Build Number'
}
# desired_cap['browserstack.debug'] = True
desired_cap["chromeOptions"] = {}
# desired_cap["chromeOptions"]["excludeSwitches"] = ["disable-popup-blocking"]
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
# driver = webdriver.Remote(
#     command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
#     desired_capabilities=desired_cap)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def environment():
    driver.maximize_window()
    driver.get(url_travelnoire)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 40).until(ec.title_is("Travel Noire"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for travelnoire.com, for web, '
          'took too long but no response, checking title"}}')
        driver.quit()


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


def smoke_test_landing_page():
    print("function called smoke_test_landing_page")
    article_link = driver.find_element(
      By.XPATH,
      "(//div[@class='slick-slide slick-active slick-current']//div//a)[1]")
    article = article_link.get_attribute("title")
    print(article)
    article_link.click()
    WebDriverWait(driver, 5).until(ec.title_is(article+" - Travel Noire"))
    time.sleep(2)
    read_full_article_btn = driver.find_element(
      By.XPATH,
      "//button[normalize-space()='Read Full Article']")
    actions = ActionChains(driver)
    actions.move_to_element(read_full_article_btn).perform()
    read_full_article_btn.click()
    shadow_str = "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > article:nth-child(1) > div:nth-child(1) > div:nth-child(2) > main:nth-child(1) > div:nth-child(7) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((
      By.CSS_SELECTOR, shadow_str
      )))
    time.sleep(2)
    root1 = driver.find_element(By.CSS_SELECTOR, shadow_str)
    time.sleep(1)
    last = driver.execute_script("return arguments[0].shadowRoot", root1)
    time.sleep(1)
    text_ele = last.find_element(By.CSS_SELECTOR, ".ql-editor.ql-blank")
    actions = ActionChains(driver)
    actions.move_to_element(text_ele).perform()
    text_ele.click()
    text_ele.send_keys("Nice Read")
    time.sleep(2)
    text_ele.send_keys(Keys.ENTER)
    print("wrote the comments for article as:"+article)

environment()
page_load()
post_page_load_pop_up()
smoke_test_landing_page()
driver.quit()
