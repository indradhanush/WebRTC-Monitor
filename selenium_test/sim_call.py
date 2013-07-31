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

#LEVEL 1=Login; 2=Call_Connecting; 3=Call_Ringing; 4=Call_Answered; 5=Call_terminated
LEVEL = 0  

ERROR_STATUS = {
    0: "FAILED_AT_START",
    1: "FAILED_AFTER_LOGIN",
    2: "FAILED_AFTER_ATTEMPT_TO_CALL_CONNECT",
    3: "FAILED_AFTER_CALL_RINGING",
    4: "FAILED_AFTER_CALL_ANSWERED",
    5: "FAILED_AFTER_CALL_TERMINATED"
}

class CallerEndpoint(unittest.TestCase):
    
    def setUp(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        self.driver = webdriver.Chrome(chromedriver)
        self.receiver = webdriver.Chrome(chromedriver)
        self.receiver.get("file:///home/dhanush/WebRTC-Monitor/receiver.html")
        
    def test_login(self):
        try:
            driver = self.driver
            driver.get("file:///home/dhanush/WebRTC-Monitor/caller.html")
            self.assertIn("Plivo Webphone Demo", driver.title)
            wait = ui.WebDriverWait(driver, 30)
            wait.until(lambda driver: driver.find_element_by_id("login_box"))
            username = driver.find_element_by_id("username")
            passwd = driver.find_element_by_id("password")
            username.send_keys(ENDPOINT)
            passwd.send_keys(PASSWORD)
            driver.find_element_by_id("btn_login").click()
            wait.until(lambda driver: driver.find_element_by_id(
                                            "callcontainer").is_displayed())
            LEVEL = 1
           
            # Test Call
            to = driver.find_element_by_id("to")
            to.send_keys(DESTINATION)
            driver.find_element_by_id("make_call").click()
            wait.until(lambda driver: driver.find_element_by_id(
                                            "call_connecting").is_displayed())
            LEVEL = 2
            wait.until(lambda driver: driver.find_element_by_id(
                                            "call_ringing").is_displayed())
            LEVEL = 3
            wait.until(lambda driver: driver.find_element_by_id(
                                            "call_answered").is_displayed())
            LEVEL = 4
            wait.until(lambda driver: driver.find_element_by_id(
                                            "call_terminated").is_displayed())
            LEVEL = 5
            

        # Printing out for now. Needs to be a POST along with STATUS
        except TimeoutException:
            print "TimeoutException: LEVEL %d - %s" % (LEVEL, str(ERROR_STATUS[LEVEL]))
            STATUS = 2
            sys.exit()
        except WebDriverException:
            print "WebDriverException: LEVEL %d - %s" % (LEVEL, str(ERROR_STATUS[LEVEL]))
            STATUS = 2
            sys.exit()
        except ErrorInResponseException:
            print "ErrorInResponseException: LEVEL %d - %s" % (LEVEL, str(ERROR_STATUS[LEVEL]))
            STATUS = 2
            sys.exit()
        except:
            print "UnknownException: LEVEL %d - %s" % (LEVEL, str(ERROR_STATUS[LEVEL]))
            STATUS = 3
            sys.exit()
    
    # def test_call(self):
    #     try:
    #         to = driver.find_element_by_id("to")
    #         to.send_keys(DESTINATION)
    #         driver.find_element_by_id("make_call").click()


if __name__ == "__main__":
    unittest.main()
