import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver


url_21ninety = "https://21ninety.com/"
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
     'name': 'BStack-[Python] Smoke Test for 21ninety.com on Android Chrome for Featured Section',
     'build': 'BStack Build Number'
}

desired_cap["chromeOptions"] = {}
desired_cap["chromeOptions"]["args"] = ["--disable-notifications"]
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)


def environment():
    driver.get(url_21ninety)
    time.sleep(5)
    print(driver.title)


def page_load():
    try:
        WebDriverWait(driver, 40).until(ec.title_is("21Ninety"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for 21ninety.com, for android chrome, took too long but no response, checking title"}}')
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
        print("footer pop-up does not exist")
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("footer adv does not exist")


def verify_featured():
    print("in the function verify_featured section")
    featured = driver.find_element(By.XPATH, "//h2[normalize-space()='Featured']")
    actions = ActionChains(driver)
    actions.move_to_element(featured).perform()
    assert featured.is_displayed(), "'Featured' heading is not displayed"
    tmp = driver.find_elements(By.XPATH, "(//div[@class='featured-article-card d-flex flex-column position-relative'])")
    temp_articles = int(len(tmp) / 3)
    assert temp_articles > 0, "No articles are present under Featured section"
    print(temp_articles)
    count = 7
    while count < 13:
        temp_string = str(count)
        print("count : ", count)
        print("tempString : ", temp_string)
        temp_xpath = "(//div[@class='featured-article-card__content bg-white d-flex " \
                     "flex-column flex-full position-absolute']//div[1]//a[1])[" + temp_string + "]"
        WebDriverWait(driver, 5).until(
          ec.presence_of_element_located((
            By.XPATH, temp_xpath)))
        time.sleep(1)
        article_heading = driver.find_element(By.XPATH, temp_xpath)
        # driver.execute_script("arguments[0].scrollIntoView();", article_heading)
        actions = ActionChains(driver)
        actions.move_to_element(article_heading).perform()
        article = article_heading.get_attribute("title")
        print("article is :", article)
        temp_heading = article + " - 21Ninety"
        driver.execute_script("arguments[0].click();", article_heading)
        print("clicked on article heading")
        WebDriverWait(driver, 5).until(ec.title_is(temp_heading))
        try:
            adv = driver.find_element(By.XPATH, "//button[@class='ub-emb-close']")
            driver.execute_script("arguments[0].click();", adv)
        except NoSuchElementException:
            print("21ninety adv pop-up does not exist")
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
        WebDriverWait(driver, 5).until(ec.title_is("21Ninety"))
        count += 1


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", Featured Section on the '
      ' 21ninety.com do work as expected on android chrome."}}')


environment()
page_load()
post_page_load_pop_up()
verify_featured()
set_status()
driver.quit()
