from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.webdriver.common.touch_action import TouchAction
import time
import random


class InstaSc:
    def __init__(self):
        log_file = open(f'logs/log_file_{time.strftime("%d-%m-%Y")}.log', 'a')

        capabilities = {
            'platformName': 'Android',
            'deviceName': 'Google_Nexus_9',
            'automationName': 'UiAutomator2',
            'noReset': True,
        }
        url = 'http://localhost:4723/wd/hub'
        driver = webdriver.Remote(url, capabilities)
        touch = TouchAction(driver)
        # self.find_and_click = find_and_click(self.method,self.val, self.start_wait, self.end_wait)
        log_file.write(f'Start scrapping ' + time.ctime() + '\n')
        self.driver = driver
        self.log_file = log_file
        self.touch = touch

    def wait_a_bit(self, start, end):
        self.start = start
        self.end = end
        time.sleep(random.randrange(start, end))

    def tags_coder(self, tag_name):
        self.tag_name = tag_name
        tag_name = tag_name.upper()
        android_alphabet = {"A": 29, "B": 30, "C": 31, "D": 32, "E": 33, "F": 34, "G": 35, "H": 36, "I": 37,
                                "J": 38, "K": 39, "L": 40,
                                "M": 41, "N": 42, "O": 43, "P": 44, "Q": 45, "R": 46, "S": 47, "T": 48, "U": 49,
                                "V": 50, "W": 51, "X": 52,
                                "Y": 53, "Z": 54, "#": AndroidKey.POUND, " ": AndroidKey.SPACE}
        for letter in tag_name:
            i = android_alphabet[letter]
            self.driver.press_keycode(i)
        self.driver.press_keycode(66)
        self.wait_a_bit(1, 3)

    def check_exists_by_xpath(self, xpath):
        self.xpath = xpath
        try:
            self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
        except NoSuchElementException:
            return False
        return True

    def random_vertical_swipe(self, amount):
        self.amount = amount
        for i in range(amount):
             self.wait_a_bit(1, 3)
             start_x = random.randrange(100, 450)
             start_y = random.randrange(799, 1132)
             end_x = random.randrange(77, 470)
             end_y = random.randrange(100, 234)
             wait_time = random.randrange(270, 510)
             self.touch.press(x=start_x, y=start_y).wait(wait_time).move_to(x=end_x, y=end_y).release().perform()


    def post_liker(self, like_amount):
        self.like_amount = like_amount
        rand_swipe = random.randrange(1, 6)
        rand_deadtime = random.randrange(80*self.like_amount, 200*self.like_amount)
        deadline = time.monotonic() + rand_deadtime
        while like_amount != 0:
            self.random_vertical_swipe(1)
            # find like btn
            if self.check_exists_by_xpath('//android.widget.ImageView[@content-desc="Like"]'):
                like_btn = self.driver.find_element(by=AppiumBy.XPATH,
                                                             value='//android.widget.ImageView[@content-desc="Like"]')
                like_btn.click()
                like_amount -= 1
                self.log_file.write(f'Post liked sucessfully ' + time.ctime() + '\n')

            self.random_vertical_swipe(rand_swipe)
            self.wait_a_bit(2, 4)
            if time.monotonic() > deadline:
                break
        if like_amount > 0:
            self.log_file.write(f'Not all desired post has been liked ' + time.ctime() + '\n')

    def find_and_click(self,method='XPATH', val='', start_wait=1, end_wait=15):
        self.method = method
        self.val = val
        self.start_wait = start_wait
        self.end_wait = end_wait

        try:
            if method == 'XPATH':
                self.element = self.driver.find_element(by=AppiumBy.XPATH, value=val)
                self.log_file.write(f'Element by {method} with {val} was found. ' + time.ctime() + '\n')
            elif method == 'ID':
                self.element = self.driver.find_element(by=AppiumBy.ID, value=val)
                self.log_file.write(f'Element by {method} with {val} was found. ' + time.ctime() + '\n')
            elif method == 'CLASS_NAME':
                self.element = self.driver.find_element(by=AppiumBy.CLASS_NAME, value=val)
                self.log_file.write(f'Element by {method} with {val} was found. ' + time.ctime() + '\n')
            self.element.click()
        except NoSuchElementException:
            self.log_file.write(f'Element by {method} with {val} was not found. ' + time.ctime() + '\n')
        self.wait_a_bit(start_wait, end_wait)


    def go_scrapp(self, lst, approx_like_per_tag):
        self.lst = lst
        self.approx_like_per_tag = approx_like_per_tag
        try:
            if self.check_exists_by_xpath('//android.widget.TextView[@content-desc="Instagram"]'):
                # open Instagram App
                self.find_and_click('XPATH', '//android.widget.TextView[@content-desc="Instagram"]', 3, 12)
            for tag in lst:
                approx_like_per_tag += random.randrange(1, 5)
                self.log_file.write(f'Start searching by tag {tag} ' + time.ctime() + '\n')
                # click to search bar button
                self.find_and_click('ID', 'com.instagram.android:id/search_tab', 1, 3)
                # click on search bar panel
                self.find_and_click('XPATH',
                               '//android.widget.EditText[@resource-id="com.instagram.android:id/action_bar_search_edit_text"]',
                               2, 4)
                self.tags_coder(tag)

                if tag[0] == '#':

                    #swipe to tags !!!! !!!! DRY!!!
                    # swipe to like by location
                    touch = TouchAction(self.driver)
                    touch.press(x=600, y=195).wait(500).move_to(x=54, y=202).release().perform()
                    self.wait_a_bit(2, 4)

                    #click to tags
                    self.find_and_click('XPATH',
                                        '//android.widget.TabWidget[@text="Tags"]',
                                        1, 3)

                    # find first match
                    self.find_and_click('XPATH',
                                        '(//android.widget.FrameLayout[@resource-id="com.instagram.android:id/row_hashtag_container"])[1]')

                    # click to filter
                    self.find_and_click('XPATH',
                                   '//android.widget.Button[@resource-id="com.instagram.android:id/filter_text_to_open_bottom_sheet"]',
                                   2, 4)
                    # recent top post
                    self.find_and_click('XPATH', '//android.widget.RadioButton[@text="Recent top posts"]', 5, 10)
                    # random swipe
                    self.random_vertical_swipe(1)
                else:
                    # swipe to like by location
                    touch = TouchAction(self.driver)
                    touch.press(x=600, y=195).wait(500).move_to(x=54, y=202).release().perform()
                    self.wait_a_bit(2, 4)

                    # click to places
                    self.find_and_click('XPATH',
                                   '//android.widget.HorizontalScrollView[@resource-id="com.instagram.android:id/scrollable_tab_layout"]/android.widget.LinearLayout/android.widget.LinearLayout[4]',
                                   1, 3)

                    # click to first location
                    self.find_and_click('XPATH',
                                   '(//android.widget.LinearLayout[@resource-id="com.instagram.android:id/row_places_container"])[1]',
                                   7, 13)

                    # click to recent posts
                    self.find_and_click('XPATH', '//android.widget.TextView[@content-desc="Most Recent Posts"]', 6, 10)

                # click to first photo
                self.find_and_click('ID', 'com.instagram.android:id/image_button', 2, 5)

                self.post_liker(approx_like_per_tag)
                self.wait_a_bit(1, 3)
                # back button
                self.driver.press_keycode(4)
                self.driver.press_keycode(4)
                self.driver.press_keycode(4)
                self.log_file.write(f'End searching by tag {tag} ' + time.ctime() + '\n')
            self.driver.press_keycode(3)
        finally:

            self.driver.quit()
            self.log_file.write(
                f'End scrapping ///////////////////////////////////////////////////// ' + time.ctime() + '\n\n')
            self.log_file.close()


s = InstaSc()
s.go_scrapp(["marques de pombal", "avenida roma","#caisdosodre", "#campopequenolisboa", "saldanha", "vanite beauty bar"],20)
