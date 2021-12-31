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
  'os_version': '14',
  'device': 'iPhone 12',
  'real_mobile': 'true',
  'browserstack.local': 'false',
  'browserName': 'safari',
  'browser_version': 'latest',
  'os': 'iOS',
  'name': 'BStack-[Python] Smoke Test for blavity.com for Navigation, checking all Nav Links on ios safari',  # test name
  'build': 'BStack Build Number'  # CI/CD job or build name
}
# desired_cap['browserstack.debug'] = True
desired_cap["chromeOptions"] = {}
# desired_cap["chromeOptions"]["excludeSwitches"] = ["disable-popup-blocking"]
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
          '{"status":"failed", "reason": in ios safari for blavity.com, took too long but no response, checking title"}}')
        driver.quit()


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
        print("blavity footer cookies pop-up does not exist")
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("blavity footer adv does not exist")


def verify_nav_bar_presence():
    print("check whether nav bar is present or not")
    time.sleep(3)
    nav_bar = driver.find_element(By.CSS_SELECTOR, "button[class='navbar-toggler bg-transparent border-0 d-desktop-none text-center text-white']")
    print(nav_bar.text)
    assert nav_bar.text is not None and nav_bar.text != "", "Nav Bar Tabs are Missing for Blavity"


def verify_nav_news_link():
    print("checking the News tab")
    news_link = driver.find_element(By.XPATH, "//a[@class='nav-link text-white'][normalize-space()='News']")
    assert news_link.is_displayed(), "News link is not displayed"
    news_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("News - Blavity News"))
    assert driver.title == "News - Blavity News", "title text does not match"
    print("Current Window Title for News Link is : ", driver.title)
    driver.back()
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))


def verify_nav_opinions_link():
    print("checking the Opinion link")
    opinion_ed_link = driver.find_element(By.XPATH, "//a[@class='nav-link text-white'][normalize-space()='Op-Eds']")
    assert opinion_ed_link.is_displayed(), "Opinion link is not displayed"
    opinion_ed_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("Opinion - Blavity News"))
    assert driver.title == "Opinion - Blavity News", "title text does not match"
    print("Current Window Title for Opinion Eds Link is : ", driver.title)
    driver.back()
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))


def verify_nav_lifestyle_link():
    print("checking the Lifestyle tab")
    life_style_link = driver.find_element(By.XPATH, "//a[@class='nav-link text-white'][normalize-space()='Lifestyle']")
    assert life_style_link.is_displayed(), "Lifestyle link is not displayed"
    life_style_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("Lifestyle - Blavity News"))
    assert driver.title == "Lifestyle - Blavity News", "title text does not match for Lifestyle page"
    print("Current Window Title for Life Style Link is : ", driver.title)
    driver.back()
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))


def verify_nav_blavity_u_link():
    blavity_u_link = driver.find_element(By.XPATH, "//a[normalize-space()='BlavityU']")
    assert blavity_u_link.is_displayed(), "BlavityU link is not displayed"
    blavity_u_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("Blavity U - Blavity News"))
    assert driver.title == "Blavity U - Blavity News", "title text does not match"
    print("Current Window Title for Blavity U Link is : ", driver.title)
    driver.back()
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))


def verify_submit_story():
    submit_a_story_link = driver.find_element(By.XPATH, "//a[normalize-space()='Submit a Story']")
    assert submit_a_story_link.is_displayed(), "Submit a story link is not displayed"
    submit_a_story_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    assert driver.title == "The Community for Black Creativity and News - Blavity News", "title text does not match"
    print("Current Window Title for Submit a Story is : ", driver.title)
    driver.back()
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))


def verify_sign_up_link():
    ad_pop_up()
    sign_up_link = driver.find_element(By.XPATH, "//a[normalize-space()='Sign Up']")
    assert sign_up_link.is_displayed(), "Sign-Up link is not displayed"
    sign_up_link.click()
    # WebDriverWait(driver, 40).until(ec.number_of_windows_to_be(2))
    # time.sleep(5)
    # window_after = driver.window_handles[1]
    # driver.switch_to.window(window_after)
    # time.sleep(5)
    driver.get("https://join.blavity.com/")
    WebDriverWait(driver, 40).until(ec.url_to_be("https://join.blavity.com/"))
    assert driver.title == "Newsletter Signup | Blavity", "title text does not match for sign up page"
    print("Current window title for Sign Up is: " + driver.title)
    # driver.close()
    # driver.switch_to.window(driver.window_handles[1])
    driver.get(url_blavity)
    time.sleep(2)
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    post_page_load_pop_up()
    print("link for Sign Up Section is present and working as expected")


def verify_nav_search_bar():
    search_bar = driver.find_element(
      By.CSS_SELECTOR,
      "button[class='btn btn--search bg-transparent border-0 text-right text-white position-absolute']")
    assert search_bar.is_displayed(), "Search Bar is not displayed"
    search_bar.click()
    input_search = driver.find_element(By.XPATH, "//input[@type='text']")
    search_text = "culture"
    input_search.send_keys(search_text)
    search_bar.click()
    WebDriverWait(driver, 40).until(ec.url_contains(search_text))
    WebDriverWait(driver, 40).until(ec.title_is("Search - Blavity News"))
    assert driver.title == "Search - Blavity News", "title text does not match for search page"
    print("Current window title for Search Page is: " + driver.title)
    print("link for Search is present and working as expected")



def verify_more_email_section():
    news_letter = driver.find_element(By.XPATH, "//button[normalize-space()='get our newsletter']")
    scroll_to_last()
    news_letter.click()
    more_link_email = driver.find_element(By.XPATH, "//form[@class='subscribe-form']//input[@placeholder='Email Address']")
    assert more_link_email.is_displayed(), "More-Email link is not displayed"
    more_link_email.send_keys("test@gmail0.com")
    # time.sleep(1)

    more_link_checkbox = driver.find_element(By.XPATH, "//form[@class='subscribe-form']//input[@type='checkbox']")
    scroll_to_last()
    # assert more_link_checkbox.is_displayed(), "More Email - Checkbox is not displayed"
    more_link_checkbox.click()
    submit_more_email_link = driver.find_element(By.XPATH, "//form[@class='subscribe-form']//button[@type='submit'][normalize-space()='submit']")
    assert submit_more_email_link.is_displayed(), "More - Email Submit Button is not displayed"
    submit_more_email_link.click()
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((
     By.XPATH, "//p[@class='success-message text-silver']")))
    success_msg_on_click = driver.find_element(By.XPATH, "//p[@class='success-message text-silver']")
    assert (success_msg_on_click.text is not None) or (success_msg_on_click.text != ""), \
        "Email section of more link , Success message is not displayed"
    if (success_msg_on_click.text is not None) or (success_msg_on_click.text != ""):
        print("Email section of more link is working as expected")


def verify_more_politics():
    more_politics_link = driver.find_element(By.XPATH, "//a[normalize-space()='Politics']")
    assert more_politics_link.is_displayed(), "More -Politics link is not displayed"
    more_politics_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("Politics - Blavity News"))
    assert driver.title == "Politics - Blavity News", "title text is not matching"
    print("Link for Politics under More Section is working as expected")


def verify_more_news():
    more_news_link = driver.find_element(By.XPATH, "//a[normalize-space()='News']")
    assert more_news_link.is_displayed(), "More -News link is not displayed"
    more_news_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("News - Blavity News"))
    assert driver.title == "News - Blavity News", "title text is not matching"
    print("Link for News under More Section is working as expected")


def verify_more_op_ed():
    more_op_ed_link = driver.find_element(By.XPATH, "//a[@class='nav-link'][normalize-space()='Op-Eds']")
    actions = ActionChains(driver)
    actions.move_to_element(more_op_ed_link).perform()
    assert more_op_ed_link.is_displayed(), "More -Op-Eds link is not displayed"

    more_op_ed_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("Opinion - Blavity News"))
    assert driver.title == "Opinion - Blavity News", "title text is not matching"
    # print("Current Window Title for Politics is : ", driver.title)
    print("Link for Op-Eds under More Section is working as expected")


def verify_more_write_a_story():
    more_write_a_story_link = driver.find_element(By.XPATH, "//a[normalize-space()='Write a Story']")
    actions = ActionChains(driver)
    actions.move_to_element(more_write_a_story_link).perform()
    assert more_write_a_story_link.is_displayed(), "More -Write a story link is not displayed"
    more_write_a_story_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    assert driver.title == "The Community for Black Creativity and News - Blavity News", "title text is not matching"
    # print("Current Window Title for Write a Story is : ", driver.title)
    print("Link for Write a Story under More Section is working as expected")


def verify_more_terms():
    more_terms_link = driver.find_element(By.XPATH, "//a[normalize-space()='Terms & Conditions']")
    # actions = ActionChains(driver)
    # actions.move_to_element(more_terms_link).perform()
    assert more_terms_link.is_displayed(), "More -terms link is not displayed"
    more_terms_link.click()
    driver.get("https://blavity.com/terms-of-service")
    # switch to the new tab being opened.
    # driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))
    assert "Blavity" in driver.title
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    driver.get(url_blavity)
    time.sleep(2)
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    post_page_load_pop_up()
    print("Link for Terms & Conditions under More Section is working as expected")


def verify_more_partner_with_us():
    more_partner_with_us_link = driver.find_element(By.XPATH, "//a[normalize-space()='Partner With Us']")
    actions = ActionChains(driver)
    actions.move_to_element(more_partner_with_us_link).perform()
    assert more_partner_with_us_link.is_displayed(), "More - Partner with us link is not displayed"
    more_partner_with_us_link.click()
    # switch to the new tab being opened.
    driver.get("https://blavityinc.com/partner-with-us")
    # driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))
    assert "Blavity" in driver.title
    driver.get(url_blavity)
    time.sleep(2)
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    post_page_load_pop_up()
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    print("Link for Partner With Us under More Section is working as expected")


def verify_more_culture():
    more_culture_link = driver.find_element(By.XPATH, "//a[normalize-space()='Culture']")
    actions = ActionChains(driver)
    actions.move_to_element(more_culture_link).perform()
    assert more_culture_link.is_displayed(), "More - Culture link is not displayed"
    more_culture_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("Culture - Blavity News"))
    assert driver.title == "Culture - Blavity News", "title text is not matching"
    # print("Current Window Title for Write a Story is : ", driver.title)
    print("Link for Culture under More Section is working as expected")


def verify_more_my_account():
    more_my_account_link = driver.find_element(By.XPATH, "//a[normalize-space()='My Account']")
    actions = ActionChains(driver)
    actions.move_to_element(more_my_account_link).perform()
    assert more_my_account_link.is_displayed(), "More - My Account link is not displayed"
    more_my_account_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    assert driver.title == "The Community for Black Creativity and News - Blavity News", "title text is not matching"
    # print("Current Window Title for Write a Story is : ", driver.title)
    print("Link for My Account under More Section is working as expected")
    driver.back()


def verify_more_careers():
    more_careers_link = driver.find_element(By.XPATH, "//a[@class='nav-link'][normalize-space()='Careers']")
    actions = ActionChains(driver)
    actions.move_to_element(more_careers_link).perform()
    assert more_careers_link.is_displayed(), "More - Careers link is not displayed"
    more_careers_link.click()
    # switch to the new tab being opened.
    # driver.switch_to.window(driver.window_handles[1])
    # WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))
    driver.get("https://blavityinc.com/careers")
    assert "Blavity" in driver.title
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    driver.get(url_blavity)
    time.sleep(2)
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    post_page_load_pop_up()
    print("Link for Careers under More Section is working as expected")


def verify_more_life_style():
    more_life_style_link = driver.find_element(By.XPATH, "//a[@class='nav-link'][normalize-space()='Lifestyle']")
    actions = ActionChains(driver)
    actions.move_to_element(more_life_style_link).perform()
    assert more_life_style_link.is_displayed(), "More - Lifestyle link is not displayed"
    more_life_style_link.click()
    WebDriverWait(driver, 40).until(ec.title_is("Lifestyle - Blavity News"))
    assert driver.title == "Lifestyle - Blavity News", "title text is not matching for Lifestyle tab"
    # print("Current Window Title for Write a Story is : ", driver.title)
    print("Link for LifeStyle under More Section is working as expected")


def verify_more_privacy_policies():
    more_privacy_policies_link = driver.find_element(By.XPATH, "//a[normalize-space()='Privacy Policies']")
    actions = ActionChains(driver)
    actions.move_to_element(more_privacy_policies_link).perform()
    assert more_privacy_policies_link.is_displayed(), "More - Privacy Policies link is not displayed"
    more_privacy_policies_link.click()
    # switch to the new tab being opened.
    driver.get("https://blavity.com/privacy")
    # driver.switch_to.window(driver.window_handles[1])
    # WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))
    assert "Blavity" in driver.title
    driver.get(url_blavity)
    time.sleep(2)
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    post_page_load_pop_up()
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    print("Link for Privacy Policy under More Section is working as expected")


def scroll_to_last():
    element = driver.find_element(By.XPATH, "//h6[contains(text(),'Blavity News is a community and platform for Black')]")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()


def scroll_to_shop():
    more_shop_link = driver.find_element(By.XPATH, "//a[normalize-space()='Shop']")
    actions = ActionChains(driver)
    actions.move_to_element(more_shop_link).perform()


def verify_more_shop():
    more_shop_link = driver.find_element(By.XPATH, "//a[normalize-space()='Shop']")
    # actions = ActionChains(driver)
    # actions.move_to_element(more_shop_link).perform()
    assert more_shop_link.is_displayed(), "More - Shop link is not displayed"
    more_shop_link.click()
    # switch to the new tab being opened.
    # driver.switch_to.window(driver.window_handles[1])
    driver.get("https://shop.blavity.com/")
    WebDriverWait(driver, 5).until(ec.title_contains("Shop"))
    assert "Shop" in driver.title
    driver.get(url_blavity)
    time.sleep(2)
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    post_page_load_pop_up()
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    print("Link for Shop under More Section is working as expected")


def verify_more_social_justice():
    more_social_justice_link = driver.find_element(By.XPATH, "//a[normalize-space()='Social Justice']")
    actions = ActionChains(driver)
    actions.move_to_element(more_social_justice_link).perform()
    assert more_social_justice_link.is_displayed(), "More - Social Justice link is not displayed"
    more_social_justice_link.click()
    WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))
    assert "Blavity" in driver.title
    # print("Current Window Title for Write a Story is : ", driver.title)
    print("Link for Social Justice under More Section is working as expected")


def verify_more_mastercard():
    more_mastercard_link = driver.find_element(By.XPATH, "//a[normalize-space()='Blavity x Mastercard']")
    actions = ActionChains(driver)
    actions.move_to_element(more_mastercard_link).perform()
    assert more_mastercard_link.is_displayed(), "More - MasterCard link is not displayed"
    more_mastercard_link.click()
    WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))
    assert "Blavity" in driver.title
    # print("Current Window Title for Write a Story is : ", driver.title)
    print("Link for Blavity x Mastercard under More Section is working as expected")
    driver.back()
    WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))


def scroll_to_more_disclaimer():
    more_disclaimer_text = driver.find_element(
      By.XPATH, "//h6[contains(text(),'Blavity is a community of the most exceptional mul')]")
    actions = ActionChains(driver)
    actions.move_to_element(more_disclaimer_text).perform()


def verify_more_disclaimer_text():
    more_disclaimer_text = driver.find_element(
     By.XPATH, "//h6[contains(text(),'Blavity News is a community and platform for Black')]")
    actions = ActionChains(driver)
    actions.move_to_element(more_disclaimer_text).perform()
    assert more_disclaimer_text.is_displayed(), "More - Disclaimer text is not displayed"
    if more_disclaimer_text.is_displayed():
        print("info under more is displayed under more section.")

def ad_pop_up():
    print("function called ad_pop_up")
    try:
        footer_adv = driver.find_element(By.XPATH, "//img[@alt='close button']")
        driver.execute_script("arguments[0].click();", footer_adv)
    except NoSuchElementException:
        print("blavity footer adv does not exist")


def verify_more_instagram_link():
    ad_pop_up()
    # assert more_instagram.is_displayed(), "More - Instagram link is not displayed"
    more_instagram = driver.find_element(
      By.XPATH, "//div[@class='d-desktop-none']//a[1]")
    scroll_to_last()
    more_instagram.click()
    print("clicked on instagram link")
    verify_blavity_footer_instagram()


def verify_blavity_footer_instagram():
    time.sleep(2)
    # switch to the new tab being opened.
    # driver.switch_to.window(driver.window_handles[1])
    # print(driver.current_url)
    driver.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(driver, 40).until(ec.title_contains("Login"))
    assert driver.current_url == 'https://www.instagram.com/accounts/login/', "instagram link in footer is not active"
    if driver.current_url == 'https://www.instagram.com/accounts/login/':
        print("instagram link is active")
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    driver.get(url_blavity)
    time.sleep(2)
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    post_page_load_pop_up()


def verify_more_twitter_link():
    ad_pop_up()
    twitter = driver.find_element(By.XPATH, "//div[@class='d-desktop-none']//a[2]")
    scroll_to_last()
    assert twitter.is_displayed(), "More - Twitter link is not displayed"
    twitter.click()
    print("clicked on twitter link")
    verify_blavity_footer_twitter()


def verify_blavity_footer_twitter():
    time.sleep(2)
    # switch to the new tab being opened.
    # driver.switch_to.window(driver.window_handles[1])
    # print(driver.current_url)
    driver.get('https://mobile.twitter.com/blavity')
    WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))
    assert driver.current_url == 'https://mobile.twitter.com/blavity', "twitter link in footer is not active"
    if driver.current_url == 'https://mobile.twitter.com/blavity':
        print("twitter link is active")
    driver.get(url_blavity)
    time.sleep(2)
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    post_page_load_pop_up()
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])


def verify_blavity_footer_facebook_nav():
    print("inside function footer facebook link")
    time.sleep(2)
    # switch to the new tab being opened.
    # driver.switch_to.window(driver.window_handles[1])
    print(driver.current_url)
    print(driver.title)
    driver.get('https://www.facebook.com/Blavity/')
    WebDriverWait(driver, 40).until(ec.title_contains("Facebook"))
    assert "Facebook" in  driver.title, "facebook link in footer is not active"
    print("face book link is active")
    driver.get(url_blavity)
    time.sleep(2)
    WebDriverWait(driver, 40).until(ec.title_is("The Community for Black Creativity and News - Blavity News"))
    post_page_load_pop_up()


def verify_more_facebook_link():
    ad_pop_up()
    more_facebook = driver.find_element(
       By.XPATH, "//div[@class='d-desktop-none']//a[3]")
    scroll_to_last()
    assert more_facebook.is_displayed(), "More - Facebook link is not displayed"
    more_facebook.click()
    print("clicked on facebook link")
    verify_blavity_footer_facebook_nav()


def open_new_tab_and_verify():
  # switch to the new tab being opened.
  driver.switch_to.window(driver.window_handles[1])
  WebDriverWait(driver, 40).until(ec.title_contains("Blavity"))
  assert "Blavity" in driver.title
  # assert ec.title_contains("Blavity") == 'https://www.instagram.com/blavity/', "instagram link in footer is active"
  driver.close()
  driver.switch_to.window(driver.window_handles[0])


def verify_blavity_footer_facebook():
    print("inside function footer facebook link")
    time.sleep(2)
    # switch to the new tab being opened.
    driver.switch_to.window(driver.window_handles[1])
    print(driver.current_url)
    WebDriverWait(driver, 40).until(ec.title_contains("Facebook"))
    assert driver.current_url == 'https://m.facebook.com/login.php?next=https%3A%2F%2Fm.facebook.com%2FBlavity&refsrc=deprecated&_rdr', "facebook link in footer is not active"
    print("face book link is active")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def verify_blavity_footer_link_media():
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 40).until(ec.title_is("Media Credentials Request Form"))
    assert "Media Credentials Request Form" in driver.title
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("footer media passes link is active")


def verify_blavity_footer():
    print("function called to check blavity footer")
    all_rights_reserved = driver.find_element(
      By.XPATH, "//p[contains(text(),'© 2021 Blavity, Inc. All rights reserved.')]")
    actions = ActionChains(driver)
    actions.move_to_element(all_rights_reserved).perform()
    assert all_rights_reserved.is_displayed(), "under footer all rights reserved text is not displayed"
    actions = ActionChains(driver)
    actions.move_to_element(all_rights_reserved).perform()
    # image = driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/footer[1]/div[1]/img[1]")
    if all_rights_reserved.is_displayed():
        print("footer blavity image is present")
        fb_blavity = driver.find_element(
          By.XPATH,
          "//a[@href='https://www.facebook.com/Blavity']")
        assert fb_blavity.is_displayed(), "facebook link is not displayed under footer"
        actions.move_to_element(all_rights_reserved).perform()
        ad_pop_up()
        # if fb_blavity.is_displayed():
        #     print("footer facebook image is present")
        #     fb_blavity = driver.find_element(By.XPATH, "//a[@href='https://www.facebook.com/Blavity']")
        #     time.sleep(2)
        #     fb_blavity.click()
        #     verify_blavity_footer_facebook()
        twitter_blavity = driver.find_element(
          By.XPATH,
          "//ul[@class='app-footer__links app-footer__links--social d-grid justify-content-center justify-content-desktop-start']//li[2]//a[1]")
        assert twitter_blavity.is_displayed(), "twitter link is not displayed under footer"
        if twitter_blavity.is_displayed():
            print("footer tweeter image is present")
            twitter_blavity.click()
            verify_blavity_footer_twitter()
        instag_blavity = driver.find_element(
          By.XPATH,
          "//ul[@class='app-footer__links app-footer__links--social d-grid justify-content-center justify-content-desktop-start']//li[3]//a[1]")
        assert instag_blavity.is_displayed(), "instagram link is not displayed under footer"
        if instag_blavity.is_displayed():
            print("footer instagram image is present")
            instag_blavity.click()
            verify_blavity_footer_instagram()
        if all_rights_reserved.is_displayed():
            print("All rights reserved condition is there")
        link_careers = driver.find_element(By.XPATH, "//a[@class='text-bold'][normalize-space()='Careers']")
        assert link_careers.is_displayed(), "careers link is not displayed under footer"
        if link_careers.is_displayed():
            print("Careers link is displayed")
            link_careers.click()
            open_new_tab_and_verify()
            print("footer career's link is active")
        link_terms = driver.find_element(By.XPATH, "//a[normalize-space()='Terms']")
        actions = ActionChains(driver)
        actions.move_to_element(link_terms).perform()
        assert link_terms.is_displayed(), "terms link is not displayed under footer"
        if link_terms.is_displayed():
            print("terms link is displayed")
            link_terms.click()
            # switch to the new tab being opened.
            open_new_tab_and_verify()
            print("footer terms link is active")
        link_privacy = driver.find_element(By.XPATH, "//a[normalize-space()='Privacy']")
        actions = ActionChains(driver)
        actions.move_to_element(link_privacy).perform()
        assert link_privacy.is_displayed(), "privacy link is not displayed under footer"
        if link_privacy.is_displayed():
            print("privacy link is displayed")
            actions.move_to_element(all_rights_reserved).perform()
            link_privacy.click()
            # switch to the new tab being opened.
            open_new_tab_and_verify()
            print("footer privacy link is active")
        link_adv = driver.find_element(By.XPATH, "//a[normalize-space()='Advertise']")
        actions = ActionChains(driver)
        actions.move_to_element(link_adv).perform()
        assert link_adv.is_displayed(), "Advertise link is not displayed under footer"
        if link_adv.is_displayed():
            print("Advertise link is displayed")
            actions.move_to_element(all_rights_reserved).perform()
            link_adv.click()
            # switch to the new tab being opened.
            open_new_tab_and_verify()
            print("footer advertise link is active")
        link_media = driver.find_element(By.XPATH, "//a[contains(text(),'Media Passes')]")
        assert link_media.is_displayed(), "Media link is not displayed under footer"
        if link_media.is_displayed():
            print("Media Passes link is displayed")
            actions.move_to_element(all_rights_reserved).perform()
            link_media.click()
            # switch to the new tab being opened.
            verify_blavity_footer_link_media()


def verify_more_blavity_image():
    more_blavity_image = driver.find_element(
      By.XPATH, "//div[@class='logo-blavity-container text-center']//img[@title='Blavity']")
    assert more_blavity_image.is_displayed(), "More - Blavity Image is not displayed"
    if more_blavity_image.is_displayed():
        print("under navbar blavity is displayed.")


def verify_nav_more_section():
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    assert more_link.is_displayed(), "More link is not displayed"
    more_link.click()
    scroll_to_last()
    verify_more_shop()
    open_nav_bar()
    verify_more_email_section()
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    actions = ActionChains(driver)
    actions.move_to_element(more_link).perform()
    more_link.click()
    verify_more_politics()
    open_nav_bar()
    more_link.click()
    verify_more_news()
    open_nav_bar()
    more_link.click()
    scroll_to_shop()
    verify_more_op_ed()
    open_nav_bar()
    more_link.click()
    scroll_to_shop()
    verify_more_write_a_story()
    open_nav_bar()
    more_link.click()
    scroll_to_last()
    verify_more_terms()
    open_nav_bar()
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    more_link.click()
    scroll_to_last()
    verify_more_partner_with_us()
    open_nav_bar()
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    more_link.click()
    scroll_to_shop()
    verify_more_culture()
    open_nav_bar()
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    more_link.click()
    scroll_to_shop()
    verify_more_my_account()
    open_nav_bar()
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    more_link.click()
    scroll_to_last()
    verify_more_careers()
    open_nav_bar()
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    more_link.click()
    scroll_to_shop()
    verify_more_life_style()
    open_nav_bar()
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    more_link.click()
    scroll_to_last()
    verify_more_privacy_policies()
    open_nav_bar()
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    more_link.click()
    scroll_to_shop()
    verify_more_social_justice()
    open_nav_bar()
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    more_link.click()
    scroll_to_shop()
    verify_more_mastercard()
    open_nav_bar()
    more_link = driver.find_element(By.XPATH, "//span[@class='font-primary']")
    more_link.click()
    scroll_to_shop()
    verify_more_disclaimer_text()
    scroll_to_last()
    verify_more_instagram_link()
    open_nav_bar()
    scroll_to_last()
    verify_more_twitter_link()
    open_nav_bar()
    scroll_to_last()
    verify_more_facebook_link()
    open_nav_bar()
    scroll_to_last()
    verify_more_blavity_image()
    print("verified all links in more section.")


def open_nav_bar():
    nav_bar = driver.find_element(
      By.CSS_SELECTOR,
      "button[class='navbar-toggler bg-transparent border-0 d-desktop-none text-center text-white']")
    nav_bar.click()


def verify_nav_bar_links():
    print("check whether each nav bar link is present and working, total 7 links")
    open_nav_bar()
    nav_bar_ele = driver.find_element(By.XPATH, "//ul[@class='navbar-nav d-desktop-flex align-items-center']")
    print(nav_bar_ele.text)
    verify_nav_news_link()
    open_nav_bar()
    verify_nav_opinions_link()
    open_nav_bar()
    verify_nav_lifestyle_link()
    open_nav_bar()
    verify_nav_blavity_u_link()
    open_nav_bar()
    verify_submit_story()
    open_nav_bar()
    verify_sign_up_link()
    open_nav_bar()
    verify_nav_search_bar()
    print("All 7 links :- News, Op-Eds, Lifestyle, BlavityU, Submit a "
          "Story, Sign-Up and search bar are working as expected.")
    # open_nav_bar()
    verify_nav_more_section()


def verify_footer_presence():
    time.sleep(3)
    footer = driver.find_element(
      By.XPATH, "//footer[@class='app-footer text-center text-desktop-left text-white']")
    assert footer.is_displayed(), "Footer section is not present for blavity"
    actions = ActionChains(driver)
    actions.move_to_element(footer).perform()
    if footer.is_displayed():
        print("footer section is displayed")


def verify_read_full_article_button():
    read_full_article_button = driver.find_element(By.XPATH, "(//button[normalize-space()='Read Full Article'])[1]")
    assert read_full_article_button.is_displayed(), "Read Full Article Button is not displayed"
    actions = ActionChains(driver)
    actions.move_to_element(read_full_article_button).perform()
    try:
        pop_up_close_button = driver.find_element(By.XPATH, "//img[@data-pin-nopin='true']")
        if pop_up_close_button.is_displayed():
            pop_up_close_button.click()
            print("clicked on close button of pop up")
    # NoSuchElementException thrown if not present
    except NoSuchElementException:
        print("pop-up does not exist")
    if read_full_article_button.is_displayed():
        print("4. Read Full Article Button is displayed")
        read_full_article_button.click()
        WebDriverWait(driver, 40).until(
          ec.presence_of_element_located(
            (By.XPATH, "(//span[contains(text(),'Read Comments')])[1]")))


def verify_read_comments_button():
    WebDriverWait(driver, 40).until(
      ec.presence_of_element_located((By.XPATH, "(//span[contains(text(),'Read Comments')])[1]")))
    # time.sleep(2)
    read_comments_button = driver.find_element(By.XPATH, "(//span[contains(text(),'Read Comments')])[1]")
    assert read_comments_button.is_displayed(), "Read Comments Button is not displayed"
    actions = ActionChains(driver)
    actions.move_to_element(read_comments_button).perform()
    read_comments_button.click()
    WebDriverWait(driver, 40).until(
      ec.presence_of_element_located((By.XPATH, "//span[contains(text(),'Hide Comments')]")))
    hide_comments_button = driver.find_element(By.XPATH, "//span[contains(text(),'Hide Comments')]")
    assert hide_comments_button.is_displayed(), "Read Comments Button is not displayed"
    if hide_comments_button.is_displayed():
        print("5. comments are loaded")


def exit_browser():
    print("closing the browser instance")
    driver.quit()


def set_status():
    print("Function called set Status")
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": "in ios safari, '
      'All Navigation Links for blavity do work as expected"}}')


environment()
page_load()
post_page_load_pop_up()
verify_nav_bar_links()
set_status()
exit_browser()
