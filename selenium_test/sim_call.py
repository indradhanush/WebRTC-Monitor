import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from pyvirtualdisplay import Display

chromedriver = "./chromedriver"
os.environ["webdriver.chr  ome.driver"] = chromedriver
driver_arguments = {}

ENDPOINT = "end1130723173627" 
PASSWORD = "testplivowebrtc" 
DESTINATION = "end2130723173650@phone.plivo.com"

class CallerEndpoint(unittest.TestCase):
    
    def setUp(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        self.driver = webdriver.Chrome(chromedriver)
        driver_arguments["chrome_options"] = webdriver.ChromeOptions()
        if "TRAVIS" in os.environ:
            driver_arguments['chrome_options'].add_argument("--no-sandbox")

    def test_login(self):
        driver = self.driver
        driver.get("file:///home/dhanush/WebRTC-Monitor/caller.html")
        #driver.wait_for_page_to_load("3000")
        self.assertIn("Plivo Webphone Demo", driver.title)
        wait = ui.WebDriverWait(driver, 30)
        wait.until(lambda driver: driver.find_element_by_id("login_box"))
        username = driver.find_element_by_id("username")
        #wait.until(lambda driver: driver.find_element_by_id("password"))
        passwd = driver.find_element_by_id("password")
        username.send_keys(ENDPOINT)
        passwd.send_keys(PASSWORD)
        #passwd.submit()
        #wait.until(lambda driver: driver.find_element_by_id("btn_login"))
        driver.find_element_by_id("btn_login").click()
        #driver.click("btn_login")
        wait.until(lambda driver: driver.find_element_by_id(
                                        "callcontainer").is_displayed())

    # def test_something(self):
    #    pass
    # def test_call(self):
    #     driver = self.driver
    #     wait = ui.WebDriverWait(driver, 30)
    #     wait.until(lambda driver: driver.find_element_by_id(
    #                                      "callcontainer").is_displayed())
    #     print "Yeah!!!"
    #     #destination = driver.find_element_by_id("to")
    #     #destination.send_keys(DESTINATION)

if __name__ == "__main__":
        unittest.main()
