import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


url_afrotech = "https://afrotech.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
   'os_version': '10',
   'resolution': '1920x1080',
   'browser': 'Chrome',
   'browser_version': '94.0',
   'os': 'Windows',
   'name': 'BStack-[Python] Smoke Test for afrotech.com sign up for news letter working as expected on desktop',
   'build': 'BStack Build Number'
}

desired_cap["chromeOptions"] = {}
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)


def environment():
    driver.maximize_window()
    driver.get(url_afrotech)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 40).until(ec.title_is("AfroTech"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for afrotech.com, for web, took too long but no response, checking title"}}')
        driver.quit()


def verify_sign_up():
    print("in the function verify_signup")
    sign_up_section = driver.find_element(
      By.XPATH, "//div[@class='subscribe-dropdown subscribe-dropdown--expanded']")
    actions = ActionChains(driver)
    actions.move_to_element(sign_up_section).perform()
    assert sign_up_section.is_displayed(), "Sign Up section is not being displayed"
    sign_up_text = driver.find_element(By.XPATH, "//h4[normalize-space()='Sign up for our daily Newsletter.']")
    assert sign_up_text.is_displayed(), "text is not displayed for signup section"
    post_page_load_pop_up()
    email = driver.find_element(By.XPATH, "//input[@placeholder='Email Address']")
    email.send_keys("fortestpurposesonly5@gmail.com")
    chk_box = driver.find_element(By.XPATH, "//input[@type='checkbox']")
    chk_box.click()
    submit_button = driver.find_element(By.XPATH, "//button[normalize-space()='Subscribe']")
    submit_button.click()
    WebDriverWait(driver, 40).until(
      ec.presence_of_element_located((
        By.XPATH, "//p[@class='subscribe-form__description text-center']")))


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
        print("afrotech footer pop-up does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for desktop, sign up for news letter section on the '
      ' afrotech.com do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_sign_up()
set_status()
driver.quit()
