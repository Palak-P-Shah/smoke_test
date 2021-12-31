import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver


url_afrotech = "https://afrotech.com/"
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
     'name': 'BStack-[Python] Smoke Test for afrotech.com on ios safari for Most Popular Section',
     'build': 'BStack Build Number'
}

desired_cap["chromeOptions"] = {}
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)


def environment():
    driver.get(url_afrotech)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 40).until(ec.title_is("AfroTech"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for afrotech.com, for ios safari, took too long but no response, checking title"}}')
        driver.quit()


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
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("afrotech footer adv does not exist")


def verify_most_popular():
    print("Within the function call most popular")
    b = driver.find_element(By.CSS_SELECTOR, ".sidebar__sub-title.text-uppercase")
    actions = ActionChains(driver)
    actions.move_to_element(b).perform()
    inner_class = driver.find_elements(By.XPATH, "//a[@class='article-link sidebar__article font-secondary']")
    assert len(inner_class) > 0, "stories are not present for side bar top stories"
    print("number of instances under the top stories section are :", len(inner_class))
    number = len(inner_class)
    count = 0
    while count < number:
        post_page_load_pop_up()
        temp_string = str(count + 1)
        temp_xpath = "(//ol[@class='m-0 p-0'])[1]/li["+str(temp_string)+"]/a[1]"
        b = driver.find_element(By.XPATH, temp_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(b).perform()
        compare_1 = str(b.text)
        assert b.is_displayed(), "particular side bar top story is not present"
        print("top story required link : ", b.get_attribute('href'))
        top_story_link_url = b.get_attribute('href')
        print(top_story_link_url)
        assert (top_story_link_url is not None) and (top_story_link_url != ""), "particular top story link is not there"
        b.click()
        WebDriverWait(driver, 40).until(ec.title_contains("AfroTech"))
        print("Current top story window title: " + driver.title)
        temp_str = driver.title
        temp = temp_str.split(' -')
        compare_2 = str(temp[0])
        assert compare_1 == compare_2, "for side bar top stories, for this particular article :" + driver.title + " :story, the text does not match"
        print("deduced string is :", compare_1)
        print("text string is :", compare_2)
        driver.back()
        WebDriverWait(driver, 20).until(ec.title_is("AfroTech"))
        count += 1
        time.sleep(1)
    print("All the Most Popular Stories links do work as expected")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", Most Popular Section on the '
      ' afrotech.com do work as expected on ios safari."}}')


environment()
page_load()
post_page_load_pop_up()
verify_most_popular()
set_status()
driver.quit()
