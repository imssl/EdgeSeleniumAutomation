# Purpose of this tool is to execute automated playback tests
# with given license server API, test vectors and tokens.
# pip3 install selenium
# Safari tab > Preferences > Advanced Tab > Check "Show Develop menu" > Develop Tab > "Allow Remote Automation"

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess as sp

# Defining counter integers to be used in the function.
testCount = 0


# Function to be called with parameters: test name, video URL and token.
def analyze(name, video, key):
        driver = webdriver.Safari()
        driver.maximize_window()
        driver.get('http://URL')

        # Find the UI objects with Selenium.
        time.sleep(3)
        url = driver.find_element(By.ID, "url")
        cert = driver.find_element(By.ID, "certUrl")
        token = driver.find_element(By.ID, "token")
        licenseServer = driver.find_element(By.ID, "license-server")
        button = driver.find_element(By.ID, "open-player")

        # Clear the license server host text box.
        licenseServer.clear()

        # Enter the video URL and the token
        url.send_keys(video)
        token.send_keys(key)

        # Send FairPlay license certificate
        cert.send_keys("https://URL")

        # Enter the license server address to be tested.
        licenseServer.send_keys("https://URL")

        # Start the stream
        button.click()

        # Scroll down to video
        driver.execute_script("window.scrollTo(0,200)")

        # Use predefined counters
        global testCount

        # Increase test counter
        testCount += 1

        # Print test counter and test name
        print("Test No:", testCount)
        print("Input:", name)

        time.sleep(5)

        # Check if a video media is playing on MacOS.
        pmset = sp.getoutput("pmset -g | grep sleep")

        if "Safari" in pmset and "coreaudiod" in pmset:
            print("PASS")
        else:
            print("FAIL")

        print("")

        driver.close()


analyze("name","video","token")
