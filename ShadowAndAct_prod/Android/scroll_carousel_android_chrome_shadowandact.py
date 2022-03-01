import time, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver import ActionChains

url_shadowandact = "https://shadowandact.com/"
username = os.getenv("BROWSERSTACK_USERNAME")
access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
build_name = os.getenv("BROWSERSTACK_BUILD_NAME")
browserstack_local = os.getenv("BROWSERSTACK_LOCAL")
browserstack_local_identifier = os.getenv("BROWSERSTACK_LOCAL_IDENTIFIER")
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
    'name': 'BStack-[Python] Smoke Test in android chrome for shadowandact.com in '
           'carousel for left and right slides',  # test name
    #'build': 'BStack Build Number'
    'build': build_name,
    'browserstack.user': username,
    'browserstack.key': access_key
}
# desired_cap['browserstack.debug'] = True
desired_cap["chromeOptions"] = {}
# desired_cap["chromeOptions"]["excludeSwitches"] = ["disable-popup-blocking"]
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
# driver = webdriver.Remote(
#     command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
#     desired_capabilities=desired_cap)

driver = webdriver.Remote(
    command_executor='https://hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)


def environment():
    driver.get(url_shadowandact)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 10).until(ec.title_is("SHADOW & ACT"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for shadowandact.com, for android chrome, '
          'took too long but no response, checking title"}}')
        driver.quit()


def verify_scroll_carousel():
    print("function called scroll_carousel")
    temp_number = driver.find_elements(By.XPATH, "(//a[@class='article-link home-hero-card__image__link'])")
    number_of_entries = int((int(len(temp_number)-1)/2))
    assert number_of_entries > 0, "articles are not present in carousel"
    print("number of entries in Carousel are :- ", number_of_entries)
    left_click_button = driver.find_element(By.XPATH, "//div[@class='home-hero-slider position-relative']//button[1]")
    assert left_click_button.is_displayed(), "left click arrow button is not displayed in carousel"
    right_click_button = driver.find_element(By.XPATH, "//div[@class='home-hero-slider position-relative']//button[2]")
    assert right_click_button.is_displayed(), "right click arrow button is not displayed in carousel"
    if left_click_button.is_displayed() and right_click_button.is_displayed():
        print("both right and left click buttons are displayed on this page")
    temp = 13
    count = 8
    while count < temp:
        time.sleep(1)
        right_slide = driver.find_element(By.XPATH, "(//div[@class='home-hero-card position-relative'])["+str(count)+"]")
        actions = ActionChains(driver)
        actions.move_to_element(right_slide).perform()
        print("slided :", count-6)
        count += 1
    print("after while loop 1, count", count)
    count = count - 1
    while count > 7:
        left_arrow = driver.find_element(By.XPATH, "(//div[@class='home-hero-card position-relative'])["+str(count)+"]")
        actions = ActionChains(driver)
        actions.move_to_element(left_arrow).perform()
        time.sleep(1)
        count -= 1
        print("second while loop temp_num :", count)
    print("after while loop 2, temp_num", count)


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
        print("shadowandact cookies footer pop-up does not exist")
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("shadowandact footer adv does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for android chrome, in carousel left and right slides '
      'for shadowandact do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_scroll_carousel()
set_status()
driver.quit()
