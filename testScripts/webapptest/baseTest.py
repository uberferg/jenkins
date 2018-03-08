from selenium import webdriver
import unittest


class BaseTest(unittest.TestCase):
    driver = None
    browser = "chrome"

    def setUp(self):
        if self.browser == "chrome":
            self.driver = webdriver.Chrome()
        elif self.browser == "ff":
            self.driver = webdriver.Firefox()
        else:
            pass
        # self.driver.maximize_window()

    def tearDown(self):
        pass
        # self.driver.close()
