import time
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


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
 'build_name': 'BStack-[Python] Test for afrotech.com on mobile ios safari browser', # test name
 'name': 'BStack-[Python] Test for afrotech.com on mobile ios safari browser', # test name
 'build': 'BStack Build Number' # CI/CD job or build name
}
desired_cap['browserstack.debug'] = True
driver = webdriver.Remote(
    command_executor='https://'+BROWSERSTACK_USERNAME+':'+BROWSERSTACK_ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)

url_name = "https://www.afrotech.com/"


def environment():
    # driver.maximize_window()
    driver.get(url_name)
    time.sleep(5)
    print(driver.title)


def page_load():
    WebDriverWait(driver, 40).until(ec.title_is("AfroTech"))
    assert driver.current_url == url_name, "url does not match"


def post_page_load_pop_up():
    print("accept popups in mobile view")
    try:
        btn_close = driver.find_element(By.XPATH, "(//button[@type='button'][normalize-space()='×'])[1]")
        btn_close.click()
        # frame = driver.find_element(By.XPATH, "(//iframe[@class='ub-emb-iframe'])[1]")
        # driver.switch_to.frame(frame)
        # # WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.XPATH, "//div[@class='ub-emb-iframe-wrapper ub-emb-visible']//button[@type='button'][normalize-space()='×']")))
        # event_promo_pop_up = driver.find_element_by_xpath(
        #   "//div[@class='ub-emb-iframe-wrapper ub-emb-visible']//button[@type='button'][normalize-space()='×']")
        # driver.execute_script("arguments[0].click();", event_promo_pop_up)
    except NoSuchElementException:
        print("event promo pop-up does not exist")
    # try:
    #     frame = driver.find_element(By.XPATH, "(//iframe[@class='ub-emb-iframe'])[1]")
    #     driver.switch_to.frame(frame)
    #     pop_up_text = driver.find_element(By.XPATH, "//p[normalize-space()='We value your privacy']")
    #     if pop_up_text.is_displayed():
    #         accept_button = driver.find_element(By.XPATH, "//button[@title='Accept']")
    #         accept_button.click()
    #     driver.switch_to.parent_frame()
    # except NoSuchElementException:
    #     print("afrotech privacy pop-up does not exist")
    # try:
    #     WebDriverWait(driver, 40).until(ec.presence_of_element_located((By.XPATH, "//button[text()='Accept']")))
    #     boolean_flag = True
    # except NoSuchElementException:
    #     print("afrotech footer pop-up does not exist")
    try:
        # WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.XPATH, "//button[text()='Accept']")))
        footer_xpath = driver.find_element(By.XPATH, "//button[text()='Accept']")
        driver.execute_script("arguments[0].click();", footer_xpath)
    except NoSuchElementException:
        print("afrotech footer pop-up does not exist")


def expand_shadow_element(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root


def smoke_test_landing_page():
    print("function called smoke_test_landing_page")
    article_link = driver.find_element(
      By.XPATH,
      "(//a[@class='article-link hero-card__title d-inline-block']/span[1])[2]")
    article_link.click()
    WebDriverWait(driver, 40).until(ec.presence_of_element_located((By.XPATH, "/html/head/title")))
    time.sleep(2)
    read_comments = driver.find_element(
      By.XPATH,
      "//article[@class='at-article d-desktop-flex align-items-start at-article--featured']"
      "//button[@class='at-article__comments__toggler font-secondary text-center text-uppercase']"
      "[normalize-space()='Read Comments']")
    actions = ActionChains(driver)
    actions.move_to_element(read_comments).perform()
    time.sleep(2)
    post_page_load_pop_up()
    read_comments.click()
    time.sleep(2)
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.TAG_NAME, "data-spot-im-shadow-host")))
    root1 = driver.find_element_by_tag_name('data-spot-im-shadow-host')

    shadow_root1 = expand_shadow_element(root1)
    text_ele = shadow_root1.find_element_by_tag_name('data-editor-mode')
    actions = ActionChains(driver)
    actions.move_to_element(text_ele).perform()
    text_ele.send_keys("test")
    time.sleep(2)
    # WebDriverWait(driver, 40).until(ec.presence_of_element_located((By.XPATH, "")))
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": "for Afrotech, for the '
      'initial article Read Comments button is working as expected"}}')


environment()
page_load()
time.sleep(4)
post_page_load_pop_up()
smoke_test_landing_page()
driver.quit()
