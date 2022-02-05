# Purpose of this tool is to execute automated playback tests
# with given license server API, test vectors and tokens.
# pip install msedge-selenium-tools selenium pillow opencv-python
import time
import os
import cv2
from PIL import Image
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Defining desired capabilities for Edge Driver:
# https://docs.microsoft.com/en-us/microsoft-edge/webdriver-chromium/capabilities-edge-options
capabilities = DesiredCapabilities.EDGE
capabilities['ms:loggingPrefs'] = {'browser': 'ALL'}
capabilities['acceptInsecureCerts'] = bool(True)

# Defining options for Edge Driver
# https://docs.microsoft.com/en-us/microsoft-edge/webdriver-chromium/capabilities-edge-options
options = EdgeOptions()
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
options.use_chromium = True
options.add_argument("--start-maximized")

# Defining counter integers to be used in the function.
testCount = 0
eventCount = 0


# Function to be called with parameters: test name, video URL and token.
def analyze(name, video, key):
    # Deleting a stored license.
    try:
        os.remove(r"licenseFileDirectory")
    except OSError:
        pass

    # Setting Edge Driver to variable "driver".
    # Edge driver directory in your PC must be set to "executable_path".
    # If you are getting errors, download the driver manually from here:
    # https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    driver = Edge(executable_path=r"C:\Users\{user}\Documents\edgedriver_win64\msedgedriver.exe",
                  capabilities=capabilities, options=options)

    # Open the browser and navigate to URL
    driver.get('https://URL')

    # Find the UI objects with Selenium.
    url = driver.find_element(By.ID, "url")
    token = driver.find_element(By.ID, "token")
    button = driver.find_element(By.ID, "open-player")
    licenseServer = driver.find_element(By.ID, "license-server")
    keySystemPreset = Select(driver.find_element(By.ID, 'key-system-selector'))

    # Selecting a dropdown menu
    keySystemPreset.select_by_visible_text('KeySystem')

    # Clear the license server host text box.
    licenseServer.clear()

    # Enter the license server address to be tested.
    licenseServer.send_keys("https://LicenseServerURL")

    # Clear URL and Token text boxes.
    url.clear()
    token.clear()

    # Enter the video URL and the token
    url.send_keys(video)
    token.send_keys(key)

    # Start the stream
    button.click()

    # Scroll down to video
    driver.execute_script("window.scrollTo(0,200)")

    # Use predefined counters
    global testCount
    global eventCount

    # Wait for events to be printed, this can be decreased depending on performance.
    time.sleep(15)

    # Increase test counter
    testCount += 1

    # EVENT TEST
    # Grab the JS events from the browser console log using get_log() function,
    # everytime this function is called previous logs are cleared so no need to set the "logs" to null.
    logs = driver.get_log('browser')

    # Print test counter and test name
    print("Test No:", testCount)
    print("Input:", name)

    # Search for event "playing" through retrieved console logs.
    for log in logs:
        if "playing" in log['message']:
            eventCount += 1

    # If event is found then PASS, otherwise FAIL.
    if eventCount > 0:
        print("Event Test: PASS")
    elif eventCount == 0:
        print("Event Test: FAIL")

    # Setting event Count to zero for next iterations.
    eventCount = 0

    # Image Test is commented out because when we disable hardware acceleration on Edge, DRM videos are not streamed.
    # IMAGE TEST
    # Find the video player location and size.
    element = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[1]/div/div/video")
    location = element.location
    size = element.size
 
    # Save screenshot of whole page.
    driver.save_screenshot("shot.png")
 
    # Re-arrange video player location and size for proper image test.
    x = location['x'] + 150
    y = location['y'] - 150
    w = size['width'] + 100
    h = size['height'] + 100
    width = x + w
    height = y + h
 
    # Crop the taken image with calculated location and size.
    im = Image.open('shot.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save('image.png')
 
    # Expected image in specified time.
    image = cv2.imread('default.png')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram = cv2.calcHist([gray_image], [0],
                             None, [256], [0, 256])
 
    # Screenshot image taken in specified time, we expect image to be similar as possible.
    image = cv2.imread('image.png')
    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram1 = cv2.calcHist([gray_image1], [0],
                              None, [256], [0, 256])
 
    # Define euclidean distances
    c1, c2 = 0, 0
 
    # Euclidean distance between images
    i = 0
    while i < len(histogram) and i < len(histogram1):
        c1 += (histogram[i] - histogram1[i]) ** 2
        i += 1
    c1 = c1 ** (1 / 2)

    If image is close enough then PASS, otherwise FAIL.
    if c1 > 100000:
        print("Image Test: FAIL")
    else:
        print("Image Test: PASS")

    # Need to delete stored license, to delete it we need to close the browser.
    driver.close()
    driver.quit()

    # Wait for browser to close completely, this can be decreased depending on performance.
    time.sleep(3)

    # Deleting a stored license.
    try:
        os.remove(r"licenseFileDirectory")
    except OSError:
        pass

    # Delete previous screenshots.
    os.remove("shot.png")
    os.remove("image.png")


# Calling function with test name, video URL, token. Normally these should be called from another file for a clearer code.
analyze("test","http://URL,"token")
