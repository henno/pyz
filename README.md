# Pyz

This python script enables you to get large amount of bots with specified names into your zoom meetings / classes. It uses headless Chrome browsers.

## Instructions

1. Run `git clone https://github.com/henno/pyz` in terminal to clone this repo to your computer.
2. Find out your Chrome's current version (Hamburger > Help > About)
2. Download matching Selenium Webdriver version from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads) and put it to project folder
3. Run `pip install -r requirements.txt` to install dependencies
4. Open `main.py` and replace sample `meetingID` and sample `pwd` (from your invitation link) and `Persons` list content 
5. Run `python3 main.py`
6. Watch those persons join your Zoom meeting :)
7. Run `pkill Chrome` (or taskkill /im chrome.exe in Windows) to get clean up all the hidden Chrome processes after the meeting is over. It takes about 2 minutes if you kill Chromes while the meeting is ongoing before they disappear from the meeting.