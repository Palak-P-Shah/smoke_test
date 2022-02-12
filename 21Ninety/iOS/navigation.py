import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

url_21ninety = "https://staging.21ninety.com/"
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
     'name': 'BStack-[Python] Smoke Test for 21ninety.com nav bar section is as expected or not on ios safari',
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
        WebDriverWait(driver, 20).until(ec.title_is("21Ninety"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for 21ninety.com, for ios safari, took too long but no response, checking title"}}')
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
        print("21ninety footer cookies pop-up does not exist")


def verify_nav_bar_presense():
    print("function called verify_nav_bar_presense")
    nav_bar = driver.find_element(By.XPATH, "//nav[@class='navbar position-sticky text-black']")
    assert nav_bar.is_displayed(), "nav bar is not present"


def verify_link(page):
    print("function called verify_link "+page)
    page_value = driver.find_element(By.XPATH, "//a[normalize-space()='"+page+"']")
    assert page_value.is_displayed(), page + "link is not present"
    page_value.click()
    if page == "Work & Money":
        page = "Work, Money"
    if page == "Style & Beauty":
        page = "Style, Beauty"
    WebDriverWait(driver, 10).until(ec.title_is(page + " - 21Ninety"))
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((
      By.XPATH,
      "//h1[normalize-space()='"+page+"']")))
    driver.back()
    WebDriverWait(driver, 10).until(ec.title_is("21Ninety"))


def verify_submit_story():
    print("function called verify_submit_story")
    submit = driver.find_element(By.XPATH, "//a[normalize-space()='SUBMIT A STORY']")
    assert submit.is_displayed(), "Submit a Story link is not displayed"
    submit.click()
    WebDriverWait(driver, 10).until(ec.url_matches("https://legacy.21ninety.com/login"))
    # driver.back()
    # WebDriverWait(driver, 10).until(ec.title_is("21Ninety"))
    driver.get(url_21ninety)
    post_page_load_pop_up()


def nav_bar():
    print("function called navbar")
    nav = driver.find_element(
      By.XPATH,
      "(//button[@class='navbar__toggler bg-transparent border-0 d-desktop-none text-center'])[1]")
    nav.click()


def verify_search_btn():
    print("function called verify_search_btn")
    search_btn = driver.find_element(By.XPATH, "//nav[@class='navbar position-sticky text-black']//button[2]")
    assert search_btn.is_displayed(), "search button is not displayed"
    search_btn.click()
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((
      By.XPATH,
      "//label[normalize-space()='SEARCH']")))
    input_txt = driver.find_element(By.XPATH, "//input[@placeholder='Type search term...']")
    input_txt.send_keys("culture")
    input_txt.send_keys(Keys.ENTER)
    WebDriverWait(driver, 10).until(ec.title_is("Search - 21Ninety"))
    driver.back()


def verify_side_social_media_links(value):
    print("function called verify_side_social_media_links")
    link = driver.find_element(By.XPATH, "//div[@class='socialbar position-fixed text-grey']/ul/li["+value+"]/a")
    actions = ActionChains(driver)
    actions.move_to_element(link).perform()
    assert link.is_displayed(), "facebook link not displayed"
    link.click()
    # switch to the new tab being opened.
    driver.switch_to.window(driver.window_handles[1])
    if value == "1":
        WebDriverWait(driver, 40).until(ec.title_contains("21 Ninety"))
        assert "21 Ninety" in driver.title
    elif value == "3":
        WebDriverWait(driver, 40).until(ec.title_contains("Login"))
        assert "Login" in driver.title
    else:
        WebDriverWait(driver, 40).until(ec.title_contains("21Ninety"))
        assert "21Ninety" in driver.title
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("Social Media Link in side bar is working as expected")


def verify_footer_link(value):
    print("function called verify_footer_link")
    link = driver.find_element(By.XPATH, "(//a[@class='d-inline-block'])["+value+"]")
    actions = ActionChains(driver)
    actions.move_to_element(link).perform()
    assert link.is_displayed(), "facebook link not displayed"
    link.click()
    # switch to the new tab being opened.
    driver.switch_to.window(driver.window_handles[1])
    if value == "1":
        WebDriverWait(driver, 40).until(ec.title_contains("21 Ninety"))
        assert "21 Ninety" in driver.title
    elif value == "3":
        WebDriverWait(driver, 40).until(ec.title_contains("Login"))
        assert "Login" in driver.title
    else:
        WebDriverWait(driver, 40).until(ec.title_contains("21Ninety"))
        assert "21Ninety" in driver.title
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("Social Media Link in Footer is working as expected")


def verify_footer_page(page_value):
    print("function called verify_footer ",page_value)
    if page_value == "Shadow & Act" or page_value == "Travel Noire" or page_value == "AfroTech":
        page = driver.find_element(By.XPATH, "(//a[normalize-space()='"+page_value+"'])[3]")
    else:
        page = driver.find_element(By.XPATH, "//a[normalize-space()='"+page_value+"']")
    actions = ActionChains(driver)
    actions.move_to_element(page).perform()
    assert page.is_displayed(), page_value+" link is not displayed in footer"
    page.click()
    if page_value == "Home":
        WebDriverWait(driver, 40).until(ec.title_contains("21Ninety"))
    elif page_value == "About":
        WebDriverWait(driver, 40).until(ec.title_is("About - 21Ninety"))
        driver.back()
        WebDriverWait(driver, 40).until(ec.title_contains("21Ninety"))
    elif page_value == "Shadow & Act" or page_value == "Travel Noire" or page_value == "AfroTech":
        if page_value == "Shadow & Act":
            page_value = "SHADOW & ACT"
        # switch to the new tab being opened.
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 40).until(ec.title_contains(page_value))
        assert page_value in driver.title
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    else:
        # switch to the new tab being opened.
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))
        assert "Blavity" in driver.title
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    print(page_value + " link is working as expected")


def verify_footer_presense():
    footer = driver.find_element(By.XPATH, "//footer[@class='app-footer bg-black text-white']")
    actions = ActionChains(driver)
    actions.move_to_element(footer).perform()
    assert footer.is_displayed(), "footer is not present"


def verify_footer():
    print("function called verify_footer")
    verify_footer_presense()
    img = driver.find_element(By.XPATH, "//img[@src='/images/logo-white.png']")
    image_present = driver.execute_script(
      "return arguments[0].complete && typeof arguments[0].naturalWidth "
      "!= \"undefined\" && arguments[0].naturalWidth > 0",
      img)
    if image_present:
        print("footer Image displayed.")
    else:
        print("footer Image not displayed.")
        assert image_present, "footer image is not displayed"
    desc = driver.find_element(By.XPATH, "//h2[contains(text(),'It takes 21 days to form a habit and 90 days to cr')]")
    assert desc.is_displayed() and desc.text is not None and desc.text != "", "description is not present"
    verify_side_social_media_links("1") # facebook link
    verify_side_social_media_links("2") # twitter link
    verify_side_social_media_links("3") # instagram link
    verify_side_social_media_links("4") # pinterest link
    verify_footer_link("1") # facebook link
    verify_footer_link("2") # twitter link
    verify_footer_link("3") # instagram link
    verify_footer_link("4") # pinterest link
    verify_footer_page("Home")
    verify_footer_page("About")
    verify_footer_page("Privacy")
    verify_footer_page("Careers")
    verify_footer_page("Partner With Us")
    verify_footer_page("Blavity")
    verify_footer_page("Shadow & Act")
    verify_footer_page("Travel Noire")
    verify_footer_page("AfroTech")


def verify_navigation_links():
    print("function called verify_navigation_links")
    verify_nav_bar_presense()
    nav_bar()
    verify_link("News")
    nav_bar()
    verify_link("Wellness")
    nav_bar()
    verify_link("Work & Money")
    nav_bar()
    verify_link("Style & Beauty")
    nav_bar()
    verify_link("Relationships")
    nav_bar()
    verify_submit_story()
    verify_search_btn()


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for ios safari, on 21ninety.com navigation section do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_navigation_links()
set_status()
driver.quit()
