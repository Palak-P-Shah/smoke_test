import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
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
   'name': 'BStack-[Python] Smoke Test for blavity.com in carousel for left and right slides on ios safari',  # test name
   'build': 'BStack Build Number'  # CI/CD job or build name
}
desired_cap['browserstack.debug'] = True
desired_cap["chromeOptions"] = {}
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
          '{"status":"failed", "reason": for blavity.com, for web, took too long but no response, checking title"}}')
        driver.quit()


def verify_scroll_right(count):
    temp = 1
    while temp < (count + 1):
        print("inside the while temp variable value is ", temp)
        right_article = driver.find_element(By.XPATH, "(//div[@class='home-hero-card__image-container'])["+str(temp)+"]")
        actions = ActionChains(driver)
        actions.move_to_element(right_article).perform()
        time.sleep(3)
        temp += 1
        print("clicked the right icon number of times :- ", temp)


def verify_scroll_carousel():
    print("function called scroll_carousel")
    number_of_entries = driver.find_elements(By.CLASS_NAME, "home-hero-card__title-wrapper")
    print(len(number_of_entries))
    count = 1
    tmp = 0
    while count < len(number_of_entries):
        tmp = count + 1
        print(tmp)
        temp = str(tmp)
        time.sleep(2)
        right_article = driver.find_element(
          By.XPATH,
          # "(//div[@class='home-hero-card__title-wrapper']/a[1])["+temp+"]")
          "(//div[@class='home-hero-card__image-container'])["+temp+"]")
        time.sleep(2)
        driver.execute_script("arguments[0].scrollIntoView();", right_article)
        actions = ActionChains(driver)
        actions.move_to_element(right_article).perform()
        print("slided number of times ", count)
        time.sleep(1)
        # verify_scroll_right(count)
        count += 1
    print("after while loop 1, count", count)
    count = count - 1
    while count > 0:
        left_article = driver.find_element(By.XPATH, "(//div[@class='home-hero-card__image-container'])["+str(count)+"]")
        time.sleep(2)
        driver.execute_script("arguments[0].scrollIntoView();", left_article)
        actions = ActionChains(driver)
        actions.move_to_element(left_article).perform()
        time.sleep(1)
        count -= 1
        print("second while loop count :", count)
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
        print("blavity footer pop-up does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for on ios safari, in carousel left and right arrow '
      'Links for blavity do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_scroll_carousel()
set_status()
driver.quit()
