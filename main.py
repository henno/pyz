from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from joblib import Parallel, delayed
from selenium.webdriver.support.wait import WebDriverWait
import time

start_time = time.perf_counter()


# Config
meetingId = '123123123'
pwd = 'Zm9IdGduRWdYNEwmcHrqZjdGUmdRQT09'
Persons = [
    "John Smith",
    "Jane Doe"
]


def join(name):
    print("Start adding " + name)
    opt = Options()
    opt.headless = True
    opt.add_argument("--disable-infobars")
    opt.add_argument("start-maximized")
    opt.add_argument("--disable-extensions")
    opt.add_experimental_option("detach", True)
    opt.add_experimental_option("prefs", {
        # Pass the argument 1 to allow and 2 to block
        "profile.default_content_setting_values.media_stream_mic": 2,
        "profile.default_content_setting_values.media_stream_camera": 2,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.notifications": 2
    })

    s = Service('./chromedriver')
    driver = webdriver.Chrome(options=opt, service=s)

    driver.get('https://us02web.zoom.us/wc/join/'+meetingId+'?pwd='+pwd)

    # Click ACCEPT COOKIES
    WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((
        By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()

    # Fill "Your name"
    driver.find_element(By.XPATH, '//*[@id="inputname"]').send_keys(name)

    # Click "Join"
    driver.find_element(By.XPATH, '//*[@id="joinBtn"]').click()

    # Click "I agree"
    driver.find_element(By.XPATH, '//*[@id="wc_agree1"]').click()

    # Change title
    driver.execute_script("document.title = '" + name + "'")

    print("End adding " + name)


Parallel(n_jobs=33)(delayed(join)(person) for person in Persons)

end_time = time.perf_counter()
print(end_time - start_time, "seconds")
