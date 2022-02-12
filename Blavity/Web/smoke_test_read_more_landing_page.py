
import time
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


url_blavity = "https://staging.blavity.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
   'os_version': '10',
   'resolution': '1920x1080',
   'browser': 'Chrome',
   'browser_version': '94.0',
   'os': 'Windows',
   'browserstack.selenium_version' : "3.14.0",
   'build_name': 'BStack-[Python] Smoke Test for blavity.com for initial carousel article checking comments being added',  # test name
   'name': 'BStack-[Python] Smoke Test for blavity.com for initial carousel article checking comments being added',  # test name
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
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    assert driver.current_url == url_blavity, "url does not match for blavity.com"


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


def expand_shadow_element(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root


def smoke_test_landing_page():
    print("function called smoke_test_landing_page")
    article_link = driver.find_element(
      By.XPATH,
      "//div[@class='slick-slide slick-current slick-active']"
      "//div//div[@class='home-hero-card__title-wrapper']")
    article_link.click()
    WebDriverWait(driver, 40).until(ec.presence_of_element_located((By.XPATH, "/html/head/title")))
    time.sleep(2)
    read_full_article_btn = driver.find_element(
      By.XPATH,
      "//div[@id='article-repeating-block-0']"
      "//button[@type='button'][normalize-space()='Read Full Article']")
    actions = ActionChains(driver)
    actions.move_to_element(read_full_article_btn).perform()
    read_full_article_btn.click()
    time.sleep(2)
    # time.sleep(5)
    read_comments = driver.find_element(By.XPATH, "(//button[@type='button']/span[contains(text(),'Read Comments')])[1]")
    actions = ActionChains(driver)
    actions.move_to_element(read_comments).perform()
    read_comments.click()
    time.sleep(4)
    # WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "data-spot-im-shadow-host")))
    str_tmp = "div[data-spot-im-shadow-host='@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover']"
    time.sleep(2)
    root1 = driver.find_element(By.CSS_SELECTOR, str_tmp)
    time.sleep(1)
    last = driver.execute_script("return arguments[0].shadowRoot", root1)
    time.sleep(2)
    # shadow_ele = expand_shadow_element(root1)
    # WebDriverWait(driver, 40).until(ec.presence_of_element_located((By.CSS_SELECTOR, ".Typography__text.Typography__product-heading.Typography__product-heading.spcv_header-text")))
    # tmp = driver.find_element(By.CSS_SELECTOR, ".Typography__text.Typography__product-heading.Typography__product-heading.spcv_header-text")
    # actions = ActionChains(driver)
    # actions.move_to_element(tmp).perform()

    text_ele = last.find_element(By.CSS_SELECTOR, ".ql-container.ql-snow")
    actions = ActionChains(driver)
    actions.move_to_element(text_ele).perform()
    # # root1.find_element(By.CSS_SELECTOR, ".ql-editor.ql-blank")
    # text_ele = shadow_ele1.find_element(By.CSS_SELECTOR, ".ql-container.ql-snow")
    # actions = ActionChains(driver)
    # actions.move_to_element(text_ele).perform()
    text_ele.click()
    text_ele.send_keys("Nice Read")
    time.sleep(2)
    # WebDriverWait(driver, 40).until(ec.presence_of_element_located((By.XPATH, "")))
    # driver.execute_script(
    #   'browserstack_executor: {"action": "setSessionStatus", "arguments": '
    #   '{"status":"passed", "reason": "for Blavity, for the '
    #   'initial article Read Comments button is working as expected"}}')


environment()
page_load()
# time.sleep(4)
post_page_load_pop_up()
smoke_test_landing_page()
driver.quit()
