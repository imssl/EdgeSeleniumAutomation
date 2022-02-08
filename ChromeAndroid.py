# Purpose of this tool is to execute automated playback tests
# with given license server API, test medias and tokens.
# Need to install Appium Server on the PC: https://appium.io/
# Need to install Android Studio and SDK tools: https://developer.android.com/studio
# pip install selenium Appium-Python-Client
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import appium
import time

# Desired capabilities for webdriver
desired_caps = {
    'platformName': 'Android',

    # Android version
    'platformVersion': '10.0',

    # Connect Android phone to the computer.
    # Device ID retrieved from Appium Server, you can also get it with adb.exe in SDK tools folder. Command: "adb devices".
    'deviceName': '2a41da30300d7ece',

    'browserName': 'Chrome',
    'goog:loggingPrefs': '{"browser": "ALL"}',
    'acceptInsecureCerts': bool(True)
}

# Calling appium
driver = appium.webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

# Open the browser and navigate to URL
driver.get("https://URL")

# Find the UI objects with Selenium.
url = driver.find_element(by=AppiumBy.XPATH, value='/html/body/div/div[2]/div[1]/div/div[1]/input')
token = driver.find_element(by=AppiumBy.XPATH, value='/html/body/div/div[2]/div[1]/div/div[2]/input')
licenseServer = driver.find_element(by=AppiumBy.XPATH, value='/html/body/div/div[2]/div[1]/div/div[3]/table/tbody/tr[2]/td[1]/input')
button = driver.find_element(by=AppiumBy.XPATH, value='/html/body/div/div[2]/div[1]/div/div[4]/button[1]')

# Clear the license server host text box.
licenseServer.clear()

# Enter the license server address to be tested.
licenseServer.send_keys("https://URL")

# Defining counter integers to be used in the function.
num = 0
count = 0


# Function to be called with parameters: test name, video URL and token.
def analyze(name, video, key):

    # Clear URL and Token text boxes.
    url.clear()
    token.clear()

    # Enter the video URL and the token
    url.send_keys(video)
    token.send_keys(key)

    # Start the stream
    button.click()

    # Use predefined counters
    global num
    global count

    # Wait for events to be printed, this can be decreased depending on performance.
    time.sleep(20)

    # Increase test counter
    num += 1

    # Grab the JS events from the browser console log using get_log() function,
    # everytime this function is called previous logs are cleared so no need to set the "logs" to null.
    logs = driver.get_log('browser')

    # Print test counter and test name.
    print("Test No:", num)
    print("Input:", name)

    # Search for event "playing" through retrieved console logs.
    for log in logs:
        if "playing" in log['message']:
            count += 1

    # If event is found then PASS, otherwise FAIL.
    if count > 0:
        print("PASS")
    elif count == 0:
        print("FAIL")
    count = 0


# Calling function with test name, video URL, token. 
# Normally these should be called from another file for a clearer code.
analyze("test","http://URL,"token")
    
driver.close()
driver.quit()
