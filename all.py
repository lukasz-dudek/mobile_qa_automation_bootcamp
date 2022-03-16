from appium import webdriver
import logging
import pytest

log = logging.getLogger('simple_example')
log.setLevel(logging.DEBUG)

the_app = "/Users/lukas/Desktop/boot-camp/theapp.apk"
list_demo_header = "Check out these clouds"


class WebCommon:
    def __init__(self, apk_name):
        self.driver = None
        self.init_driver(apk_name)
        # self.get_driver()

    def init_driver(self, apk_name):
        desired_caps = {
            "platformName": "Android",
            "platformVersion": "12",
            "deviceName": "R5CN81ML3VE",
            "automationName": "UiAutomator2",
            "app": apk_name,
            # "autoGrantPermissions": True
            "noReset": True
        }
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

    def get_driver(self):
        return self.driver

    def close_driver(self):
        self.driver.quit()


driver = WebCommon(the_app).get_driver()


class Test01Android:
    @classmethod
    def setup_class(cls):
        log.info("setup_class")

    def setup_method(self, method):
        log.info("setup_method")

    @pytest.mark.parametrize("os", ["Android"])
    def test_01(self, os):
        log.info(f"test_01 on {os}")

    def teardown_method(self, method):
        log.info("teardown_method")

    @classmethod
    def teardown_class(cls):
        log.info("teardown_class")

    @pytest.mark.xfail(reason="Unable to execute test")
    def test_02_xfail(self):
        assert False

    @pytest.mark.skip(reason="Unable to execute test")
    def test_03_skip(self):
        assert True

    def test_04_list_size(self):
        list_of_elements = driver.find_elements_by_xpath('//android.view.ViewGroup[@content-desc]')
        driver.implicitly_wait(1)
        log.info(f" List size: {len(list_of_elements)}, Expected: 7")
        assert len(list_of_elements) == 7

    def get_element_by_text(self, text):
        find_text = driver.find_element_by_android_uiautomator('new UiSelector().text("' + text + '")')
        return find_text

    def test_05_text(self):
        # to open LIST DEMO I needed to look for "Photo Demo" string because this value matches "List Demo" button in app
        self.get_element_by_text("Photo Demo").click()
        list_demo_screen_header = self.get_element_by_text(list_demo_header).text
        log.info(f" 'List Demo' screen's header \"{list_demo_screen_header}\", \
        expected: \"{list_demo_header}\"")
        assert list_demo_screen_header == list_demo_header
