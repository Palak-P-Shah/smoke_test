from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

url_afrotech = "https://afrotech.com/"
BROWSERSTACK_USERNAME = 'palakshah_rcAxD5'
BROWSERSTACK_ACCESS_KEY = 's2rqmyxFs8r999bzvGXJ'
desired_cap = {
 'os_version': '10.0',
 'device': 'Google Pixel 3',
 'real_mobile': 'true',
 'browserstack.local': 'false',
 'browserName': 'Chrome',
 # 'resolution': '1920x1080',
 # 'browser': 'Chrome',
 'browser_version': 'latest',
 'os': 'Android',
 'build_name': 'BStack-[Python] Monitoring Test for afrotech.com on mobile Android Chrome browser', # test name
 'name': 'BStack-[Python] Monitoring Test for afrotech.com on mobile Android Chrome browser', # test name
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
