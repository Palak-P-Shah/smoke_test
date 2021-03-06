import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


url_blavity = "https://blavity.com/"
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
   'name': 'BStack-[Python] Smoke Test for blavity.com top stories section is as expected on android chrome',
   'build': 'BStack Build Number'
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
        WebDriverWait(driver, 20).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for blavity.com, for android, took too long but no response, checking title"}}')
        driver.quit()


def verify_top_stories():
    print("Within the function call top stories")
    b = driver.find_element(By.CSS_SELECTOR, ".home-top-stories.page-home__top-stories.flex-full")
    actions = ActionChains(driver)
    actions.move_to_element(b).perform()
    inner_class = driver.find_elements(By.CLASS_NAME, "home-top-story-card__title-container")
    assert len(inner_class) > 0, "stories are not present for side bar top stories"
    print("number of instances under the top stories section are :", len(inner_class))
    number = len(inner_class)
    count = 0
    while count < number:
        temp_string = str(count + 1)
        temp_xpath = "//div[@class='page-home__content']//li["+str(temp_string)+"]/div[1]/div[2]/div[1]/a[1]"
        b = driver.find_element(By.XPATH, temp_xpath)
        compare_1 = str(b.text)
        assert b.is_displayed(), "particular side bar top story is not present"
        print("top story required link : ", b.get_attribute('href'))
        top_story_link_url = b.get_attribute('href')
        if (top_story_link_url is None) or (top_story_link_url == ""):
            print("particular top story link is not there")
        b.click()
        WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))
        print("Current top story window title: " + driver.title)
        temp_str = driver.title
        temp = temp_str.split(' -')
        compare_2 = str(temp[0])
        assert compare_1 == compare_2, "for side bar top stories, for this particular article :"+driver.title+" :story, the text does not match"
        print("deduced string is :", compare_1)
        print("text string is :", compare_2)
        driver.back()
        WebDriverWait(driver, 20).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
        count += 1
        time.sleep(1)
    print("All the Side bar Top Stories links do work as expected")


def post_page_load_pop_up():
    print("accept popups in web view")
    try:
        btn_close = driver.find_element(By.XPATH, "(//button[@type='button'][normalize-space()='??'])[1]")
        btn_close.click()
    except NoSuchElementException:
        print("event promo pop-up does not exist")
    try:
        footer_xpath = driver.find_element(By.XPATH, "//button[text()='Accept']")
        driver.execute_script("arguments[0].click();", footer_xpath)
    except NoSuchElementException:
        print("blavity footer pop-up does not exist")
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("blavity footer adv does not exist")


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for android chrome, on blavity.com top stories section do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_top_stories()
set_status()
driver.quit()
