import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

class MenuTest:
    def setup_method(self):
        # Assuming self.driver is already initialized and points to the app
        self.driver = self.initialize_driver()