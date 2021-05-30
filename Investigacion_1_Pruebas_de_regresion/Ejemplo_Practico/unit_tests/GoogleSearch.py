from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from unittest import TestCase
from time import sleep


class GoogleSearch(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def test_search_netflix(self):
        self.driver.get('https://google.com/')
        self.driver.find_element_by_name('q').send_keys('Netflix' + Keys.RETURN)
        self.driver.find_element_by_xpath("//h3[contains(.,'Netflix Costa Rica')]").click()
        sleep(1)
        self.assertEqual(self.driver.title, 'Netflix Costa Rica: Ve series online, ve películas online')

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        print('Test Completed')
