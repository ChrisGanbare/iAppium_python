from appium import webdriver
import unittest
import time
import os
import allure
from appium.options.android import UiAutomator2Options
from pytest_testconfig import config

timeout = 30
poll = 2

@allure.feature('IAppium')
class IAppium(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        appium_server_url = config['appium_server_url']
        desired_caps['platformName'] = config['desired_caps']['platformName']
        desired_caps['udid'] = config['desired_caps']['udid']
        desired_caps['deviceName'] = config['desired_caps']['deviceName']
        desired_caps['appPackage'] = config['desired_caps']['appPackage']
        desired_caps['appActivity'] = config['desired_caps']['appActivity']
        desired_caps['automationName'] = config['desired_caps']['automationName']
        desired_caps['noReset'] = config['desired_caps']['noReset']
        desired_caps['app'] = f'{os.path.abspath(os.curdir)}/app/ContactManager.apk'

        # 创建UiAutomator2Options对象（但此处不需调用to_capabilities）
        options = UiAutomator2Options()

        self.driver = webdriver.Remote(appium_server_url, desired_caps,options=options)

    def tearDown(self):
        self.driver.quit()

    @allure.story('Test Contact')
    def test_contact(self):
        """  """

        # Workaround for version issue
        self._click_confirm_ok_btn()

        self._click_add_contact_btn()
        self._input_contact_name('A san')
        self._input_email('asan@example.com')
        self._click_save_btn()

        # Workaround for version issue
        self._click_confirm_ok_btn()
        time.sleep(2)

    def _click_add_contact_btn(self):
        elem = self._find_elem_by_xpath('//android.widget.Button[@content-desc="Add Contact"]')
        print(f'Click add contact button')
        elem.click()

    def _input_contact_name(self, txt_name):
        elem = self._find_elem_by_xpath('//android.widget.EditText[@resource-id="com.example.android.contactmanager:id/contactNameEditText"]')
        print(f'Input contact name {txt_name}')
        elem.send_keys(txt_name)

    def _input_email(self, txt_email):
        elem = self._find_elem_by_xpath('//android.widget.EditText[@resource-id="com.example.android.contactmanager:id/contactEmailEditText"]')
        print(f'Input email {txt_email}')
        elem.send_keys(txt_email)

    def _click_save_btn(self):
        elem = self._find_elem_by_xpath('//android.widget.Button[@content-desc="Save"]')
        print('Click the save button')
        elem.click()

    def _click_confirm_ok_btn(self):
        elem = self._find_elem_by_xpath('//android.widget.Button[contains(@resource-id, "android:id/button1")]',
                                        time_out=3, raise_exception=False)
        if elem is not None:
            print('Click the ok button on confirm dialog')
            elem.click()
        else:
            print('No confirm dialog found')

    def _find_elem_by_xpath(self, elem_xpath, time_out=timeout, raise_exception=True):
        start = time.time()
        elem = None
        while time.time() - start < time_out and elem is None:
            time.sleep(poll)
            try:
                elem = self.driver.find_element_by_xpath(elem_xpath)
            except Exception:
                print('by pass the element not found')

        if elem is None and raise_exception:
            raise LookupError(f'The element which xpath is {elem_xpath} could not be found')

        return elem
