WebRTC-Monitor
==============

WebRTC monitoring tool for Plivo-WebRTC service.

This tool uses selenium to run chrome in a headless mode and uses two sip
endpoint to simulate a call. It first opens an instance of chrome and logs in
with an endpoint credential with receiver.html 

A second instance of chrome is fired and it logs in with the second endpoint
credentials via caller.html; This endpoint attempts a call to the receiver.html

To set up a system the clone the repo and then the following is necessary before the test can be run on the system:

1. sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

2. wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

3. sudo apt-get update --force-yes

4. sudo apt-get install -qq --force-yes xvfb imagemagick google-chrome-stable

5. sudo apt-get install unzip

6. wget https://chromedriver.googlecode.com/files/chromedriver_linux64_2.1.zip

7. unzip -a chromedriver_linux64_2.1.zip

8. pip install -r requirements.txt (Preferably in a virtualenv)

The selenium tests are on the branch >> selenium

It is also important to configure the paths for caller.html, reciever.html and
the chromedriver in the test code. 

Currently the test prints out the exception if any. It needs to be configured
to POST the exception message to a monitoring Server. Also the endpoints have
to be configured.

When the test fails it sends out a LEVEL to indicate the point at which it
failed.

LEVEL 0: "FAILED_AT_START"

LEVEL 1: "FAILED_AFTER_LOGIN"

LEVEL 2: "FAILED_AFTER_ATTEMPT_TO_CALL_CONNECT"

LEVEL 3: "FAILED_AFTER_CALL_RINGING"

LEVEL 4: "FAILED_AFTER_CALL_ANSWERED"

LEVEL 5: "FAILED_AFTER_CALL_TERMINATED"

LEVEL 6: "FAILED_AFTER_CALLER_LOGOUT"

LEVEL 7: "FAILED_AFTER_RECEIVER_LOGOUT"

LEVEL 8: "TEST_SUCCESSFUL"

The test runs with listen_mode set to True and thus doesn not ask for any media
permissions.

Running the test: python selenium_test/sim_call.py
