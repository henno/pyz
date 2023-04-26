import sys

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
import time
import configparser

# Start timer
start_time = time.perf_counter()

# Check that chromedriver is installed (both on Win and macOS)
try:
    s = Service("./chromedriver")
    s.start()
    s.stop()
except Exception as e:
    print("Chromedriver is not installed. Please download it from https://chromedriver.chromium.org/downloads and "
          "place it in the same folder as this script.")
    sys.exit(1)

# Check that meetingId is set (is not 111)
config = configparser.ConfigParser()
config.read("config.ini")
if config.get("Settings", "meetingId") == "111" or config.get("Settings", "meetingId") == "":
    print("Please set your meetingId in config.ini")
    sys.exit(1)

# Create a list to store all active WebDrivers
drivers = []

# Create a counter to count the number of participants
participant_counter = 0

# Read configuration from INI file
config = configparser.ConfigParser()
config.read("config.ini")

# Get Zoom configuration values
meetingId = config.get("Settings", "meetingId")
pwd = config.get("Settings", "meetingPwd")


def debug_message(name, message, severity=0):
    # Create timestamp
    timestamp = time.strftime("%H:%M:%S", time.localtime())

    # Read debug_level from config
    debug_level = config.get("Settings", "debug_level")

    if isinstance(severity, str):
        severity = int(severity)

    if isinstance(debug_level, str):
        debug_level = int(debug_level)

    if severity <= debug_level:
        print(f"[{timestamp}] {name}: {message}")


def click_element(driver, name, element_description, xpath, delay=0):
    debug_message(name, f"Clicking {xpath}", 1)
    while True:
        try:
            time.sleep(delay)
            WebDriverWait(driver, 20).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, xpath)
                )
            ).click()
            break  # break the loop if the click is successful
        except StaleElementReferenceException:
            # Make beep
            print("\a", end="")

            print("\033[91mCould not click\033[0m", file=sys.stderr)
            user_input = input("Press R to retry or S to skip: ").lower()
            if user_input == "r":
                continue  # retry clicking the element
            elif user_input == "s":
                break  # skip clicking the element
        except Exception as e:
            if isinstance(e, selenium.common.exceptions.ElementClickInterceptedException):
                print("\033[91mFailed to click\033[0m", file=sys.stderr)
                user_input = input("Press R to retry or S to skip: ").lower()
                if user_input == "r":
                    continue  # retry clicking the element
                elif user_input == "s":
                    break  # skip clicking the element
            else:
                raise e


def join(participant_name):
    # Print the count of the person
    global participant_counter
    participant_counter += 1
    debug_message(participant_name, f"is ({participant_counter}/{len(Persons)}) participant", 0)



    # Start timer
    start_time = time.perf_counter()

    # Set up options
    debug_message(participant_name, "Setting up options", 1)
    opt = Options()

    # Set up options
    opt.add_argument("--disable-infobars")
    opt.add_argument("start-maximized")
    opt.add_argument("--disable-extensions")
    opt.add_argument("--ignore-certificate-errors")
    opt.add_argument("--allow-running-insecure-content")

    # Set headless mode
    if config.get("Settings", "headless") == "True":
        debug_message(participant_name, "Setting up headless mode", 1)
        opt.add_argument("--headless")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--window-size=1920,1080")

    # opt.add_experimental_option("detach", True)
    opt.add_experimental_option(
        "prefs",
        {
            # Pass the argument 1 to allow and 2 to block
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2,
        },
    )

    # Create WebDriver instance
    s = Service("./chromedriver")
    driver = webdriver.Chrome(options=opt, service=s)

    # Add the new WebDriver instance to the list of active drivers
    drivers.append(driver)

    # Open meeting URL
    debug_message(participant_name, f"Opening meeting URL... https://us02web.zoom.us/wc/join/{meetingId}?pwd={pwd}", 1)
    driver.get(f"https://us02web.zoom.us/wc/join/{meetingId}?pwd={pwd}")

    # Click "Accept cookies"
    click_element(driver, participant_name, "Accept cookies", "//button[@id='onetrust-accept-btn-handler']")

    # Click Accept conditions
    click_element(driver, participant_name, "Accept conditions", '//*[@id="wc_agree1"]')

    # Fill "Your name"
    click_element(driver, participant_name, "name box", '//*[@id="inputname"]')
    driver.find_element(By.XPATH, '//*[@id="inputname"]').send_keys(participant_name)

    # Click "Join meeting"
    click_element(driver, participant_name, "Join", '//*[@id="joinBtn"]')

    # Click "Preview join"
    click_element(driver, participant_name, "Preview join", '//*[@class="preview-join-button"]')

    # Change title
    debug_message(participant_name, "Changing title", 1)
    driver.execute_script(f"document.title = '{participant_name}'")

    # Measure time
    end_time = time.perf_counter()

    # Set the global debug_level to "info" to print only the first and last debug messages
    debug_level = "info"

    # Round the time to int
    end_time = int(end_time - start_time)

    debug_message(participant_name, f"Finished in {end_time} seconds")


print("Starting...")

# Read names from file
with open("participants.txt", "r") as f:
    Persons = f.read().splitlines()

# Join each person to the meeting
for person in Persons:
    join(person)

# Print the total time in human-readable format
print(f"Finished in {time.strftime('%H:%M:%S', time.gmtime(time.perf_counter() - start_time))}")

# Play beep
print("\a", end="")

# Suggest to run pkill Chrome to kill all Chrome processes
print("Run 'pkill Chrome' to kill all Chrome processes")