# System Imports
import os
import unittest
import sys
from pyvirtualdisplay import Display

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.common.exceptions import WebDriverException, TimeoutException, ErrorInResponseException

chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

ENDPOINT = "end1130723173627" 
PASSWORD = "testplivowebrtc" 
DESTINATION = "end2130723173650@phone.plivo.com"

STATUS = 0
ERROR_STATUS = {
    0: "FAILED_AT_START",
    1: "FAILED_AFTER_LOGIN",
    2: "FAILED_AFTER_ATTEMPT_TO_CALL_CONNECT",
    3: "FAILED_AFTER_CALL_RINGING",
    4: "FAILED_AFTER_CALL_ANSWERED",
    5: "FAILED_AFTER_CALL_TERMINATED",
    6: "FAILED_AFTER_CALLER_LOGOUT",
    7: "FAILED_AFTER_RECEIVER_LOGOUT"
}

class CallerEndpoint(unittest.TestCase):
    
    def setUp(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        self.LEVEL = 0  
        self.driver = webdriver.Chrome(chromedriver)
        self.receiver = webdriver.Chrome(chromedriver)
        self.receiver.get("file:///home/dhanush/WebRTC-Monitor/receiver.html")
        
    def test_login(self):
        try:
            driver = self.driver
            receiver = self.receiver
            driver.get("file:///home/dhanush/WebRTC-Monitor/caller.html")
            self.assertIn("Plivo Webphone Demo", driver.title)
            wait = ui.WebDriverWait(driver, 30)
            wait.until(lambda driver: driver.find_element_by_id(
                                             "login_box").is_displayed())
            username = driver.find_element_by_id("username")
            passwd = driver.find_element_by_id("password")
            username.send_keys(ENDPOINT)
            passwd.send_keys(PASSWORD)
            driver.find_element_by_id("btn_login").click()
            wait.until(lambda driver: driver.find_element_by_id(
                                            "callcontainer").is_displayed())
            self.LEVEL = 1
           
            # Test Call
            to = driver.find_element_by_id("to")
            to.send_keys(DESTINATION)
            driver.find_element_by_id("make_call").click()
            wait.until(lambda driver: driver.find_element_by_id(
                                            "call_connecting").is_displayed())
            self.LEVEL = 2
            wait.until(lambda driver: driver.find_element_by_id(
                                            "call_ringing").is_displayed())
            self.LEVEL = 3
            wait.until(lambda driver: driver.find_element_by_id(
                                            "call_answered").is_displayed())
            self.LEVEL = 4
            wait.until(lambda driver: driver.find_element_by_id(
                                            "call_terminated").is_displayed())
            self.LEVEL = 5
            wait.until(lambda driver: driver.find_element_by_id(
                                            "logout_box").is_displayed())
            driver.find_element_by_id("btn_logout").click()
            self.LEVEL = 6
            wait.until(lambda receiver: receiver.find_element_by_id(
                                            "logout_box").is_displayed())
            receiver.find_element_by_id("btn_logout").click()
            self.LEVEL = 7

        # Printing out for now. Needs to be a POST along with STATUS
        except TimeoutException:
            print "TimeoutException: LEVEL %d - %s" % (self.LEVEL, str(ERROR_STATUS[self.LEVEL]))
            STATUS = 2
            
        except WebDriverException:
            print "WebDriverException: LEVEL %d - %s" % (self.LEVEL, str(ERROR_STATUS[self.LEVEL]))
            STATUS = 2
            
        except ErrorInResponseException:
            print "ErrorInResponseException: LEVEL %d - %s" % (self.LEVEL, str(ERROR_STATUS[self.LEVEL]))
            STATUS = 2
            
        except:
            print "UnknownException: LEVEL %d - %s" % (self.LEVEL, str(ERROR_STATUS[self.LEVEL]))
            STATUS = 3
            
   
    def tearDown(self):
        try:
            self.driver.close()
            self.receiver.close()
        except:
            print "UnknownException in TearDown: LEVEL %d - %s" % (self.LEVEL, str(ERROR_STATUS[self.LEVEL]))
            STATUS = 3
            

    # def test_call(self):
    #     try:
    #         to = driver.find_element_by_id("to")
    #         to.send_keys(DESTINATION)
    #         driver.find_element_by_id("make_call").click()


if __name__ == "__main__":
    unittest.main()
