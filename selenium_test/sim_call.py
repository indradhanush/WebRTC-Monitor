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

# Chrome Settings
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

# Endpoint Configuration
ENDPOINT = "end1130723173627" 
PASSWORD = "testplivowebrtc" 
DESTINATION = "end2130723173650@phone.plivo.com"

# HTML files for test
CALLER = "file:///home/dhanush/WebRTC-Monitor/caller.html"
RECEIVER = "file:///home/dhanush/WebRTC-Monitor/receiver.html"

STATUS = 0
EXIT_LEVEL = {
    0: "FAILED_AT_START",
    1: "FAILED_AFTER_LOGIN",
    2: "FAILED_AFTER_ATTEMPT_TO_CALL_CONNECT",
    3: "FAILED_AFTER_CALL_RINGING",
    4: "FAILED_AFTER_CALL_ANSWERED",
    5: "FAILED_AFTER_CALL_TERMINATED",
    6: "FAILED_AFTER_CALLER_LOGOUT",
    7: "FAILED_AFTER_RECEIVER_LOGOUT",
    8: "TEST_SUCCESSFUL"
}


def locate_element(driver, element):
    return lambda driver: driver.find_element_by_id(element).is_displayed()


class CallerEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.LEVEL = 0
        self.TEST_CLEAN = False
        display = Display(visible=0, size=(800, 600))
        display.start()
        self.driver = webdriver.Chrome(chromedriver)
        self.receiver = webdriver.Chrome(chromedriver)
        self.receiver.get(RECEIVER)
        
    def test_webrtc(self):
        try:
            driver = self.driver
            receiver = self.receiver
            driver.get(CALLER)
            self.assertIn("Plivo Webphone Demo", driver.title)
            wait = ui.WebDriverWait(driver, 30)
            wait.until(locate_element(driver, "login_box"))
            username = driver.find_element_by_id("username")
            passwd = driver.find_element_by_id("password")
            username.send_keys(ENDPOINT)
            passwd.send_keys(PASSWORD)
            driver.find_element_by_id("btn_login").click()
            wait.until(locate_element(driver, "callcontainer"))
            self.LEVEL = 1
           
            # Test Call
            to = driver.find_element_by_id("to")
            to.send_keys(DESTINATION)
            driver.find_element_by_id("make_call").click()
            wait.until(locate_element(driver, "call_connecting"))
            self.LEVEL = 2
            wait.until(locate_element(driver, "call_ringing"))
            self.LEVEL = 3
            wait.until(locate_element(driver, "call_answered"))
            self.LEVEL = 4
            wait.until(locate_element(driver, "call_terminated"))
            self.LEVEL = 5
            wait.until(locate_element(driver, "logout_box"))
            driver.find_element_by_id("btn_logout").click()
            self.LEVEL = 6
            wait.until(locate_element(driver, "logout_box"))
            receiver.find_element_by_id("btn_logout").click()
            self.LEVEL = 7

        # Printing out for now. Needs to be a POST along with STATUS
        except TimeoutException:
            print "TimeoutException: LEVEL %d - %s" % (self.LEVEL, str(EXIT_LEVEL[self.LEVEL]))
            STATUS = 2
            
        except WebDriverException:
            print "WebDriverException: LEVEL %d - %s" % (self.LEVEL, str(EXIT_LEVEL[self.LEVEL]))
            STATUS = 2
            
        except ErrorInResponseException:
            print "ErrorInResponseException: LEVEL %d - %s" % (self.LEVEL, str(EXIT_LEVEL[self.LEVEL]))
            STATUS = 2
            
        except:
            print "UnknownException: LEVEL %d - %s" % (self.LEVEL, str(EXIT_LEVEL[self.LEVEL]))
            STATUS = 3
        
        else:
            self.TEST_CLEAN = True

    def tearDown(self):
        try:
            self.driver.close()
            self.receiver.close()
        except:
            print "UnknownException in TearDown: LEVEL %d - %s" % (self.LEVEL, str(EXIT_LEVEL[self.LEVEL]))
            STATUS = 3
        else:
            if self.TEST_CLEAN: 
                self.LEVEL = 8
                print "Test Successful: LEVEL %d" % (self.LEVEL)


if __name__ == "__main__":
    unittest.main()
