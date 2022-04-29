"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/4/28 9:54 PM
"""
from selenium import webdriver
from time import sleep
from lxml import etree
import pandas as pd
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

def load_webdriver():
    webdriver_path = '/usr/local/bin/chromedriver'
    browser = webdriver.chrome(webdriver_path = webdriver_path)
    # load the web page
    # browser.get('https://www.amazon.com/rabbitgoo-Multi-Level-Scratching-Furniture-Climbing/dp/B0876ZGYP4/ref=sr_1_1_sspa?crid=2SV9YXLL6981T&keywords=cat%2Btree&qid=1651155266&sprefix=cat%2Btree%2Caps%2C803&sr=8-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUE5WEpYSzBPWjlPSjMmZW5jcnlwdGVkSWQ9QTAwNjc1NDEyT0NEWVE2UjdIQjVTJmVuY3J5cHRlZEFkSWQ9QTA4NTc1MzMxVkVXVU5QS1ozUUNPJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1')
    # browser.maximzie_window()


    
if __name__ == '__main__':
    load_webdriver()