# Purpose of this tool is to execute automated playback tests
# with given license server API, test vectors and tokens.
# pip3 install selenium pillow opencv-python
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from PIL import Image
import time
import cv2
import os

# Defining desired capabilities for Chrome Driver:
# https://chromedriver.chromium.org/capabilities
capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = {'browser': 'INFO'}
capabilities['acceptInsecureCerts'] = bool(True)

# Defining options for Chrome Driver:
# https://chromedriver.chromium.org/capabilities
opts = Options()
opts.add_argument("--start-maximized")

# Setting Chrome Driver to variable "driver".
# Chrome driver directory in your PC must be set to "executable_path".
# If you are getting errors, download the driver manually from here:
# https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome(executable_path=r"C:\Users\{user}\Documents\chromedriver_win32\chromedriver.exe",
                          desired_capabilities=capabilities, options=opts)

# Open the browser and navigate to URL
driver.get('https://URL')

# Find the UI objects with Selenium.
url = driver.find_element(By.ID, "url")
token = driver.find_element(By.ID, "token")
licenseServer = driver.find_element(By.ID, "license-server")
button = driver.find_element(By.ID, "open-player")

# Clear the license server host text box.
licenseServer.clear()

# Enter the license server address to be tested.
licenseServer.send_keys("https://URL ")

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

    # Scroll down to video
    driver.execute_script("window.scrollTo(0,200)")

    # Use predefined counters
    global num
    global count

    # Wait for events to be printed, this can be decreased depending on performance.
    time.sleep(15)

    # Increase test counter
    num += 1

    # EVENT TEST
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
        print("Event Test: PASS")
    elif count == 0:
        print("Event Test: FAIL")
    count = 0

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

    # If image is close enough then PASS, otherwise FAIL.
    if c1 > 100000:
        print("Image Test: FAIL")
    else:
        print("Image Test: PASS")

    # Delete previous screenshots.
    os.remove("shot.png")
    os.remove("image.png")

# Calling function with test name, video URL, token. Normally these should be called from another file for a clearer code.
analyze("test","http://URL,"token")

driver.close()
driver.quit()
