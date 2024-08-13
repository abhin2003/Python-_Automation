import base64
import time
import threading
from adbutils import adb
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#appium --use-plugin=images


generalized_phone_for_mobileapp_automation = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "11199313A4110880",
    "udid": "11199313A4110880",
    "appPackage": "io.metamask",
    "appActivity": ".MainActivity",
    "imageMatchThreshold": 0.2,
    "getMatchedImageResult": True,
    "nativeWebScreenshot": True,
    "ensureWebviewsHavePages": True,
    "language": "en",
    "locale": "US",
    "noReset": True,
    "newCommandTimeout": 3600,
    "appium:autoGrantPermissions": True
}

appium_server_url = "http://127.0.0.1"
active_drivers = []

def setup_driver(device_serial, port):
    capabilities = generalized_phone_for_mobileapp_automation.copy()
    capabilities["deviceName"] = device_serial
    capabilities["udid"] = device_serial
    appium_server_url_local = f"{appium_server_url}:{port}"
    options = UiAutomator2Options().load_capabilities(capabilities)
    driver = webdriver.Remote(command_executor=appium_server_url_local, options=options)
    active_drivers.append(driver)
    return driver

def safe_sleep(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining = end_time - time.time()
        if remaining <= 0:
            break
        try:
            threading.Event().wait(timeout=min(remaining, 0.1))
        except Exception:
            if stop_flag.is_set():
                raise KeyboardInterrupt
            

driver = setup_driver('11199313A4110880', 4723)
safe_sleep(10)


print("If you want to click by image or ID selector ")
print("1 for Click by image")
print("2 for Click by Id selector")
n = int(input("Enter the user choice: "))

if n == 1:
    image_path = "images\metamask_unlock.jpg"
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        driver.update_settings({
            "getMatchedImageResult": True,
            "imageElementTapStrategy": "w3cActions",
            "imageMatchThreshold": 0.7,
            "imageMatchMethod": "TM_CCOEFF_NORMED",
            "fixImageFindScreenshotDims": False,
            "fixImageTemplateSize": False,
            "autoUpdateImageElementPosition": True
        })
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.IMAGE, encoded_image))
        ).click()
        print("Clicked the image successfully.")
    except Exception as e:
        print(f"Error while clicking the image: {e}")
 

elif n == 2: 
    try:
        unlockID = driver.find_element(by=AppiumBy.XPATH , value='//android.view.ViewGroup[@resource-id="log-in-button"]/android.widget.Button') 
        unlockID.click()
        print("Clicked using ID selector")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("Enter a valid choice")
    driver.quit()
