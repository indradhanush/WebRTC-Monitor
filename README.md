WebRTC-Monitor
==============

WebRTC monitoring tool for Plivo-WebRTC

Initially the project was intended to be run at travis-ci.org to check for failed builds in the process of automating a WebRTC call. But because of a known bug with Chrome, and the limitation that the test has to be run in chrome, the chrome instance fails to launch headlessly in travis-ci. So I have alternatively used Selenium to automate the calls. The working code lives in the branch "selenium". So please do checkout the selenium branch before continuing. 

Note: Not merged the code to master in the hope that the known limitation will be fixed in the near future, as running builds in the travis-ci looks like a cleaner solution but not feasible at the moment. Hope Google fix it soon. :)
