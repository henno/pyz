# Pyz

This python script enables you to get large amount of bots with specified names into your zoom meetings / classes. It uses headless Chrome browsers.

## Instructions


1. Find out your Chrome's current version (Hamburger > Help > About)
2. Download matching Selenium Webdriver version from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads) and put it to project folder
3. Run `pip install -r requirements.txt` to install dependencies
4. Open `config.ini` and replace sample `meetingID` and sample `pwd` (from your invitation link)
5. Open `participants.txt` and replace sample persons with your own
5. Run `python3 main.py`
6. Keep the Chrome windows in foreground to keep the script from failing and watch those persons join your Zoom meeting
7. Run `pkill Chrome` to kill all Chrome processes after you finish.

Macbook Pro 2013 16GB RAM with 20 Mbit/s internet connection joined 26 bots in 50 minutes. 