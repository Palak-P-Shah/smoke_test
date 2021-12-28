from common_mobile_ios_safari import *


def smoke_test_podcast():
    print("function called podcast")
    more = driver.find_element(By.XPATH, "//button[@class='navbar__toggler bg-transparent border-0 d-desktop-none text-center']")
    actions = ActionChains(driver)
    actions.move_to_element(more).perform()
    time.sleep(2)
    more.click()
    time.sleep(2)
    post_page_load_pop_up()
    podcast = driver.find_element(By.XPATH, "//a[normalize-space()='Podcast']")
    actions = ActionChains(driver)
    actions.move_to_element(podcast).perform()
    podcast.click()
    # post_page_load_pop_up()
    # switch to the new tab being opened.
    driver.switch_to.window(driver.window_handles[1])
    print(driver.current_url)
    WebDriverWait(driver, 40).until(ec.title_contains("Black Tech Green"))
    listen = driver.find_element(
      By.XPATH,
      "/html[1]/body[1]/div[1]/main[1]/article[1]/section[1]"
      "/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/a[1]")
    actions = ActionChains(driver)
    actions.move_to_element(listen).perform()
    post_page_load_pop_up()
    listen.click()
    audio_page = driver.find_element(
      By.XPATH,
      "/html[1]/body[1]/div[1]/main[1]/article[1]/section[3]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/a[1]")
    actions = ActionChains(driver)
    actions.move_to_element(audio_page).perform()
    audio_page.click()
    time.sleep(2)
    audio = driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/img[1]")
    actions = ActionChains(driver)
    actions.move_to_element(audio).perform()
    audio.click()
    time.sleep(2)
    driver.execute_script(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": '
      '{"status":"passed", "reason": "for Afrotech, for the '
      'podcast page, initial podcast is working as expected"}}')
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


environment()
page_load()
time.sleep(4)
post_page_load_pop_up()
smoke_test_podcast()
driver.quit()
