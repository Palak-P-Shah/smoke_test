import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


url_blavity = "https://staging.afrotech.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
   'os_version': '10',
   'resolution': '1920x1080',
   'browser': 'Chrome',
   'browser_version': '94.0',
   'os': 'Windows',
   'name': 'BStack-[Python] Smoke Test for afrotech.com Nav links do work as expected or not on desktop',
   'build': 'BStack Build Number'  # CI/CD job or build name
}
# desired_cap['browserstack.debug'] = True
desired_cap["chromeOptions"] = {}
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
    try:
        WebDriverWait(driver, 40).until(ec.title_is("AfroTech"))
    except TimeoutException:
        driver.execute_script(
          'browserstack_executor: {"action": "setSessionStatus", "arguments": '
          '{"status":"failed", "reason": for afrotech.com, for web, took too long but no response, checking title"}}')
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


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": ", for desktop, navigation links on'
      ' afrotech.com do work as expected"}}')


def verify_nav_bar_presence():
    print("check whether nav bar is present or not")
    # time.sleep(3)
    nav_bar = driver.find_element(By.XPATH, "//div[@class='container-fluid d-flex align-items-center']")
    print(nav_bar.text)
    assert nav_bar.text != "" and nav_bar.text is not None, "Nav Bar is not present for Afrotech website"
    if (nav_bar.text is not None) and (nav_bar.text != ""):
        print("Nav Bar is present")


def verify_sub_links(topics_link, sub_title):
    print("inside function verify_sub_links", sub_title)
    temp_link = driver.find_element(By.XPATH, "//a[@title='" + sub_title + "']")
    post_page_load_pop_up()
    actions = ActionChains(driver)
    actions.move_to_element(topics_link).perform()
    actions.move_to_element(temp_link).perform()
    assert temp_link.is_displayed(), sub_title + " link is not displayed"
    temp_link.click()
    if sub_title == 'Shop':
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 40).until(ec.title_contains("Blavity Shop"))
        assert "Blavity Shop" in driver.title, "title does not match for Shop"
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # print("Link for Shop is working as expected")
    if sub_title == 'AfroTech x Amazon':
        WebDriverWait(driver, 40).until(ec.title_is("Amazon - AfroTech"))
        assert driver.title == "Amazon - AfroTech", "title text for " + sub_title + " does not match"
    elif sub_title == 'AfroTech x Memphis':
        WebDriverWait(driver, 40).until(ec.title_is("Epicenter - AfroTech"))
        assert driver.title == "Epicenter - AfroTech", "title text for " + sub_title + " does not match"
    elif sub_title != 'Shop':
        # print("if not shop")
        WebDriverWait(driver, 40).until(ec.title_is(sub_title + " - AfroTech"))
        assert driver.title == sub_title + " - AfroTech", "title text for '" + sub_title + " - Afrotech' does not match"
    if sub_title != 'Shop':
        # print("Current Window Title for Topics-->"+sub_title+" Link is : ", driver.title)
        driver.back()
        WebDriverWait(driver, 40).until(ec.title_is("AfroTech"))


def verify_nav_topics_link():
    print("checking the Topics")
    topics_link = driver.find_element(By.XPATH, "//button[normalize-space()='Topics']")
    assert topics_link.is_displayed(), "Topics link is not displayed"
    post_page_load_pop_up()
    verify_sub_links(topics_link, 'News')
    post_page_load_pop_up()
    verify_sub_links(topics_link, 'Education')
    verify_sub_links(topics_link, 'Enterprise')
    verify_sub_links(topics_link, 'Startups')
    verify_sub_links(topics_link, 'Venture Capital')
    verify_sub_links(topics_link, 'Business')
    verify_sub_links(topics_link, 'Founders')
    verify_sub_links(topics_link, 'Interviews')
    verify_sub_links(topics_link, 'BTGM')
    verify_sub_links(topics_link, 'AfroTech x Amazon')
    verify_sub_links(topics_link, 'AfroTech x Memphis')
    verify_sub_links(topics_link, 'Shop')


def verify_nav_watch_link():
  print("inside function verify_nav_watch_link")
  watch_link = driver.find_element(By.XPATH, "//a[normalize-space()='Watch']")
  assert watch_link.is_displayed(), "Watch link is not displayed"
  watch_link.click()
  WebDriverWait(driver, 40).until(ec.title_is("AfroTech Videos - AfroTech"))
  driver.back()
  WebDriverWait(driver, 40).until(ec.title_is("AfroTech"))


def verify_nav_events_link():
    print("inside function verify_nav_events_link")
    events_link = driver.find_element(By.XPATH, "//a[normalize-space()='Events']")
    assert events_link.is_displayed(), "Events link is not displayed"
    events_link.click()
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 40).until(ec.title_contains("The AFROTECH"))
    assert "The AFROTECH" in driver.title, "title does not match for experience.afrotech.com events link"
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("Link Events for experience.afrotech.com is working as expected")


def verify_nav_podcast_link():
    print("inside function verify_nav_podcast_link")
    podcast_link = driver.find_element(By.XPATH, "//a[normalize-space()='Podcast']")
    assert podcast_link.is_displayed(), "Podcast link is not displayed"
    podcast_link.click()
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 40).until(ec.title_contains("Black Tech"))
    assert "Black Tech" in driver.title, "title does not match for https://www.afrotechpodcast.com/ podcast link"
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("Link for Podcast is working as expected")


def verify_nav_submit_story_link():
    print("inside function verify_nav_podcast_link")
    submit_story_link = driver.find_element(By.XPATH, "//a[normalize-space()='Submit Story']")
    assert submit_story_link.is_displayed(), "Submit a Story link is not displayed"
    submit_story_link.click()
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 40).until(ec.title_contains("AfroTech wants"))
    assert "AfroTech wants" in driver.title, "title does not match for Submit a Story link"
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("Link for Submit a Story is working as expected")


def verify_search_button():
    print("inside function verify_search_button")
    search_link = driver.find_element(
      By.XPATH,
      "//button[@class='btn bg-transparent border-0 color-black font-size-0 p-0 position-absolute']//*[name()='svg']")
    assert search_link.is_displayed(), "Search link is not displayed"
    search_link.click()
    search_input = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    search_input.send_keys("afrotech")
    search_input.send_keys(Keys.ENTER)
    WebDriverWait(driver, 40).until(ec.title_is("Search - AfroTech"))
    driver.back()
    WebDriverWait(driver, 40).until(ec.title_is("AfroTech"))


def verify_news_letter_section():
    print("inside function verify_news_letter")
    news_letter_section = driver.find_element(
      By.XPATH,
      "//div[@class='subscribe-dropdown subscribe-dropdown--expanded']")
    assert news_letter_section.is_displayed(), "News Letter Section is not displayed for Afrotech"
    sign_up_txt = driver.find_element(By.XPATH, "//h4[normalize-space()='Sign up for our daily Newsletter.']")
    assert sign_up_txt.is_displayed(), "Signup Text is not displayed for News Letter Section of Afrotech"
    collapse_expand_btn = driver.find_element(
      By.XPATH,
      "//span[@class='d-none d-desktop-inline font-secondary']")
    collapse_expand_btn.click()
    WebDriverWait(driver, 40).until(
      ec.presence_of_element_located((By.XPATH, "//span[contains(text(),'Expand')]")))
    collapse_expand_btn.click()
    WebDriverWait(driver, 40).until(
      ec.presence_of_element_located((By.XPATH, "//span[contains(text(),'Collapse')]")))
    assert \
        collapse_expand_btn.is_displayed(), \
        "Collapse and Expand button is not displayed " \
        "for New Letter Section of Afrotech"
    email = driver.find_element(By.XPATH, "//input[@placeholder='Email Address']")
    assert email.is_displayed(), "Email input text button is not displayed for Sign Up News Letter Section"
    email.send_keys("fortestpurposesonly5@gmail.com")
    agree = driver.find_element(By.XPATH, "//label[contains(text(),'I agree to the')]")
    assert agree.is_displayed(), "agree text and checkbox is not displayed for Sign Up News Letter Section"
    chk_box = driver.find_element(By.XPATH, "//input[@type='checkbox']")
    assert chk_box.is_displayed(), "checkbox is not displayed for Sign Up News Letter Section"
    chk_box.click()
    subscribe_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Subscribe']")
    assert subscribe_btn.is_displayed(), "subscribe button is not displayed for Sign Up News Letter Section"
    subscribe_btn.click()
    WebDriverWait(driver, 40).until(
      ec.presence_of_element_located((By.XPATH, "//p[@class='subscribe-form__description text-center']")))


def verify_nav_bar_links():
    print("check whether each nav bar link is present and working")
    # post_page_load_pop_up()
    verify_nav_bar_presence()
    # post_page_load_pop_up()
    verify_nav_topics_link()
    # post_page_load_pop_up()
    verify_nav_watch_link()
    verify_nav_events_link()
    verify_nav_podcast_link()
    verify_nav_submit_story_link()
    verify_search_button()
    verify_news_letter_section()


environment()
page_load()
post_page_load_pop_up()
verify_nav_bar_links()
set_status()
driver.quit()
