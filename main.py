from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.webdriver.extensions.keyboard import Keyboard
from selenium.common.exceptions import WebDriverException
from appium_extended.appium_get import AppiumGet
from appium.webdriver.common.touch_action import TouchAction
import time
import random

from selenium.webdriver import Keys

tags_list = ["lisboa","shibainu", "madeira", "otters"]

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

    def tags_coder(tag_name):
        tag_name = tag_name.upper()
        android_alphabet ={"A": 29, "B": 30, "C": 31, "D": 32, "E": 33, "F": 34, "G": 35, "H": 36, "I": 37, "J": 38, "K": 39, "L": 40,
         "M": 41, "N": 42, "O": 43, "P": 44, "Q": 45, "R": 46, "S": 47, "T": 48, "U": 49, "V": 50, "W": 51, "X": 52,
         "Y": 53, "Z":54}
        driver.press_keycode(AndroidKey.POUND)
        for letter in tag_name:
            i = android_alphabet[letter]
            driver.press_keycode(i)

    def post_liker():
        #open a post
        #whole_screen
        print('c1')
        whole_screen = driver.find_element(by=AppiumBy.XPATH, value='//androidx.recyclerview.widget.RecyclerView[@resource-id="com.instagram.android:id/recycler_view"]')
        one_of_photos = whole_screen.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.Button')[1]
        wait_a_bit(2, 4)
        print('c2')
        one_of_photos.click()
        print('c2a')
        wait_a_bit(1, 3)
        print('c3')
        touch.press(x=100, y=955).wait(500).move_to(x=130, y=100).release().perform()
        #find like btn
        like_btn = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@content-desc="Like"]')
        print('c4')
        if like_btn is None:
            touch.press(x=100, y=955).wait(500).move_to(x=130, y=100).release().perform()
            print('c5')
        else:
            like_btn.click()
            print('c6')



    try:
        #open Instagram App
        # digit1_btn = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Instagram"]')
        # digit1_btn.click()
        # wait_a_bit(3, 12)

        post_liker()

        # #swipe func
        # # touch = TouchAction(driver)
        # # touch.press(x=100, y=955).wait(500).move_to(x=130, y=100).release().perform()
        # #end swipe
        #
        # #click to search btn !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # search_btn = driver.find_element(by=AppiumBy.ID, value='com.instagram.android:id/search_tab')
        # search_btn.click()
        # wait_a_bit(1, 3)
        #
        # #search bar
        # search_bar = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="com.instagram.android:id/action_bar_search_edit_text"]')
        # search_bar.click()
        # print('checkpoint1')
        # #search_bar.send_keys('#shibainu')
        # print('checkpoint2')
        #
        # wait_a_bit(2, 4)
        # # tags_search (make multiple)
        # tags_coder('lisboa')
        # print('checkpoint3')
        # wait_a_bit(2, 4)
        #
        # #find first match
        # first_match = driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.FrameLayout[@resource-id="com.instagram.android:id/row_hashtag_container"])[1]/android.widget.LinearLayout')
        # first_match.click()
        # print('checkpoint4')
        # wait_a_bit(2, 4)
        #
        # #click to filter
        # filter_el = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@resource-id="com.instagram.android:id/filter_text_to_open_bottom_sheet"]')
        # filter_el.click()
        # print('checkpoint5')
        # wait_a_bit(5, 10)
        #
        # #recent top post
        # recent_top_post = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.RadioButton[@text="Recent top posts"]')
        # recent_top_post.click()
        # print('checkpoint6')
        # wait_a_bit(5, 10)
        #
        #
        # #swipe
        # touch = TouchAction(driver)
        # for i in range(6):
        #     touch.press(x=100, y=955).wait(500).move_to(x=130, y=100).release().perform()
        #     wait_a_bit(1, 3)

        #driver.tap()
        wait_a_bit(3, 12)

        #!!!!!!!!!!!!!!!!!!!!

    finally:

        driver.quit()


if __name__ == '__main__':
    test_start()



# {
#   "appium:deviceName": "Google_Nexus_9",
#   "platformName": "Android",
#   "appium:automationName": "UiAutomator2",
#   "appium:noReset": "True"
# }