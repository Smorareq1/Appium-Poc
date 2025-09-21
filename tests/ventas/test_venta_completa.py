import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class test_venta_completa:
    @pytest.mark.xray("APPTEST-****")
    def test_venta_completa(self, driver, video_recorder):
        pass