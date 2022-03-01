import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


url_shadowandact = "https://staging.shadowandact.com/"
username = os.getenv("BROWSERSTACK_USERNAME")
access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
build_name = os.getenv("BROWSERSTACK_BUILD_NAME")
desired_cap = {
   'os_version': '14',
  'device': 'iPhone 12',
  'real_mobile': 'true',
  'browserstack.local': 'false',
  'browserName': 'safari',
  'browser_version': 'latest',
  'os': 'iOS',
  'name': 'BStack-[Python] Smoke Test for staging.shadowandact.com most popular section is as expected on ios safari',
  #'build': 'BStack Build Number'
  'build': build_name,
  'browserstack.user': username,
  'browserstack.key': access_key
}

# desired_cap["chromeOptions"] = {}
# desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
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
        WebDriverWait(driver, 20).until(ec.title_is("SHADOW & ACT"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for staging.shadowandact.com, for ios safari, took too long but no response, checking title"}}')
        driver.quit()


def verify_most_popular():
    print("in the function verify_most_popular section")
    most_popular = driver.find_element(By.XPATH, "//h4[normalize-space()='Most Popular']")
    actions = ActionChains(driver)
    actions.move_to_element(most_popular).perform()
    assert most_popular.is_displayed(), "'Most Popular' heading is not displayed"
    tmp = driver.find_elements(By.CSS_SELECTOR, "div.side-tabs li")
    temp_articles = len(tmp)
    assert temp_articles > 0 , "No articles are present under Most Popular section"
    print(temp_articles)
    count = 0
    while count < temp_articles:
        temp_string = str(count + 1)
        print("count : ", count)
        print("tempString : ", temp_string)
        element = driver.find_element(By.XPATH, "//div[@class='flex-full']//li[" + temp_string + "]")
        time.sleep(1)
        temp_xpath = "//div[@class='flex-full']//li["+temp_string+"]//a[1]"
        WebDriverWait(driver, 40).until(
          ec.presence_of_element_located((
            By.XPATH, temp_xpath)))
        time.sleep(1)
        article_heading = driver.find_element(By.XPATH, temp_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        article = article_heading.get_attribute("title")
        print("article is :", article)
        temp_heading = article + " - SHADOW & ACT"
        driver.execute_script("arguments[0].click();", article_heading)
        print("clicked on article heading")
        WebDriverWait(driver, 5).until(ec.title_is(temp_heading))
        print("Current window title: " + driver.title)
        temp_str = driver.title
        temp = temp_str.split(' -')
        compare_1 = str(temp[0])
        compare_2 = article
        print("deduced string is :", compare_1)
        print("text string is :", compare_2)
        assert compare_1 == compare_2, "for 'Most Popular' section, for " \
                                       + article + ": article , title text does not match"
        driver.back()
        time.sleep(1)
        #     # driver.back()
        #     driver.execute_script("window.history.go(-1)")
        WebDriverWait(driver, 5).until(ec.title_is("SHADOW & ACT"))
        # time.sleep(2)
        count += 1


def post_page_load_pop_up():
    print("close popups in mobile view")
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
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("shadowandact footer adv does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for ios safari, on staging.shadowandact.com Most Popular section do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_most_popular()
set_status()
driver.quit()
