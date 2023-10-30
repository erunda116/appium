from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.webdriver.common.touch_action import TouchAction
import time
import random


log_file = open(f'log_file_{time.strftime("%d-%m-%Y")}.log', 'a')



tags_list = ["london","#shibainu"]

def wait_a_bit(start, end):
    time.sleep(random.randrange(start, end))

def test_start():
    capabilities = {
        'platformName': 'Android',
        'deviceName': 'Google_Nexus_9',
        'automationName': 'UiAutomator2',
        'noReset': True,
    }
    url = 'http://localhost:4723/wd/hub'
    driver = webdriver.Remote(url, capabilities)
    touch = TouchAction(driver)

    log_file.write(f'Start scrapping ' + time.ctime() + '\n')

    def tags_coder(tag_name):
        tag_name = tag_name.upper()
        android_alphabet ={"A": 29, "B": 30, "C": 31, "D": 32, "E": 33, "F": 34, "G": 35, "H": 36, "I": 37, "J": 38, "K": 39, "L": 40,
         "M": 41, "N": 42, "O": 43, "P": 44, "Q": 45, "R": 46, "S": 47, "T": 48, "U": 49, "V": 50, "W": 51, "X": 52,
         "Y": 53, "Z":54, "#":AndroidKey.POUND}
        for letter in tag_name:
            i = android_alphabet[letter]
            driver.press_keycode(i)
        driver.press_keycode(66)
        wait_a_bit(1,3)

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element(by=AppiumBy.XPATH, value=xpath)
        except NoSuchElementException:
            return False
        return True

    def random_vertical_swipe(amount):
        for i in range(amount):
            wait_a_bit(1, 3)
            start_x = random.randrange(100, 450)
            start_y = random.randrange(799, 1132)
            end_x = random.randrange(77, 470)
            end_y = random.randrange(100, 234)
            wait_time = random.randrange(270, 510)
            touch.press(x=start_x, y=start_y).wait(wait_time).move_to(x=end_x, y=end_y).release().perform()
            # log_file.write(f'vertical swipe ' + time.ctime() + '\n')

    def post_liker(like_amount):
        rand_swipe = random.randrange(1, 6)
        rand_deadtime = random.randrange(80, 120)
        deadline = time.monotonic() + rand_deadtime
        while like_amount != 0:
            random_vertical_swipe(1)
            #find like btn
            if check_exists_by_xpath('//android.widget.ImageView[@content-desc="Like"]'):
                like_btn = driver.find_element(by=AppiumBy.XPATH,
                                               value='//android.widget.ImageView[@content-desc="Like"]')
                like_btn.click()
                like_amount -= 1
                log_file.write(f'Post liked sucessfully ' + time.ctime() + '\n')

            random_vertical_swipe(rand_swipe)
            wait_a_bit(2, 4)
            if time.monotonic() > deadline:
                break
        if like_amount > 0:
            log_file.write(f'Not all desired post has been liked ' + time.ctime() + '\n')

    def find_and_click(method='XPATH', val='',start_wait=1, end_wait=15):
        try:
            if method == 'XPATH':
                element = driver.find_element(by=AppiumBy.XPATH, value=val)
                log_file.write(f'Element by {method} with {val} was found. ' + time.ctime() + '\n')
            elif method == 'ID':
                element = driver.find_element(by=AppiumBy.ID, value=val)
                log_file.write(f'Element by {method} with {val} was found. ' + time.ctime() + '\n')
            elif method == 'CLASS_NAME':
                element = driver.find_element(by=AppiumBy.CLASS_NAME, value=val)
                log_file.write(f'Element by {method} with {val} was found. ' + time.ctime() + '\n')
            element.click()
        except NoSuchElementException:
            log_file.write(f'Element by {method} with {val} was not found. ' + time.ctime() + '\n')
        wait_a_bit(start_wait, end_wait)

    def go_scrapp(lst, approx_like_per_tag):
        for tag in lst:
            approx_like_per_tag += random.randrange(1, 5)
            log_file.write(f'Start searching by tag {tag} ' + time.ctime() + '\n')
            #click to search bar button
            find_and_click('ID', 'com.instagram.android:id/search_tab', 1, 3)
            #click on search bar panel
            find_and_click('XPATH', '//android.widget.EditText[@resource-id="com.instagram.android:id/action_bar_search_edit_text"]', 2, 4)
            tags_coder(tag)

            if tag[0] == '#':
                #find first match
                find_and_click('XPATH', '(//android.widget.FrameLayout[@resource-id="com.instagram.android:id/row_hashtag_container"])[1]/android.widget.LinearLayout')
                #click to filter
                find_and_click('XPATH','//android.widget.Button[@resource-id="com.instagram.android:id/filter_text_to_open_bottom_sheet"]',2,4)
                #recent top post
                find_and_click('XPATH','//android.widget.RadioButton[@text="Recent top posts"]', 5, 10)
                #random swipe
                random_vertical_swipe(1)
            else:
                # swipe to like by location
                touch = TouchAction(driver)
                touch.press(x=600, y=195).wait(500).move_to(x=54, y=202).release().perform()
                wait_a_bit(2, 4)

                # click to places
                find_and_click('XPATH', '//android.widget.HorizontalScrollView[@resource-id="com.instagram.android:id/scrollable_tab_layout"]/android.widget.LinearLayout/android.widget.LinearLayout[5]', 1, 3)

                # click to first location
                find_and_click('XPATH', '(//android.widget.LinearLayout[@resource-id="com.instagram.android:id/row_places_container"])[1]', 4, 7)

                #click to recent posts
                find_and_click('XPATH', '//android.widget.TextView[@content-desc="Most Recent Posts"]', 6, 10)


            #click to first photo
            find_and_click('ID', 'com.instagram.android:id/image_button', 2, 5)


            post_liker(approx_like_per_tag)
            wait_a_bit(1, 3)
            # back button
            driver.press_keycode(4)
            driver.press_keycode(4)
            driver.press_keycode(4)
            log_file.write(f'End searching by tag {tag} ' + time.ctime() + '\n')
        driver.press_keycode(3)
    try:
        #open Instagram App
        find_and_click('XPATH', '//android.widget.TextView[@content-desc="Instagram"]', 3, 12)
        #go_scrapp(tags_list, 8)


        #need to create login functional



    finally:

        driver.quit()
        log_file.write(f'End scrapping ///////////////////////////////////////////////////// ' + time.ctime() + '\n\n')
        log_file.close()

if __name__ == '__main__':
    test_start()



# {
#   "appium:deviceName": "Google_Nexus_9",
#   "platformName": "Android",
#   "appium:automationName": "UiAutomator2",
#   "appium:noReset": "True"
# }

