"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/4/28 9:54 PM
"""
import os
from selenium import webdriver
from time import sleep
import time
from lxml import etree
import pandas as pd
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import requests


hea = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'downlink': '8',
    'ect': '4g',
    'rtt': '250',
    'Cookie': "session-id=257-3500989-3695223; i18n-prefs=GBP; ubid-acbuk=257-5950834-2508848; x-wl-uid=1bEcLG2b03/1tAwPJNyfuRH+U7J9ZaPYejSBR4HXKuYQPJtLhQbDYyO/GOMypGKXqZrG7qBkS0ng=; session-token=x04EF8doE84tE+6CXYubsjmyob/3M6fdmsQuqzD0jwl/qGdO5aRc2eyhGiwoD0TFzK1rR/yziHsDS4v6cdqT2DySFXFZ9I5OHEtgufqBMEyrA0/Scr87KKA+GWOjfVmKRuPCqOGaixZQ6AIjU3e2iFOdM+3v90NeXFI3cazZcd6x9TYCy9b5u9V8zR7ePbdP; session-id-time=2082758401l; csm-hit=tb:MAA188S1G57TNTH6HQCZ+s-T9EGT4C8FC8J74X5T7CY|1594212767446&t:1594212767446&adb:adblk_no",
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}


options = webdriver.ChromeOptions()  # 初始化Chrome
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("disable-web-security")
options.add_argument('disable-infobars')
options.add_experimental_option('excludeSwitches', ['enable-automation'])

def gethtml(url0, head):
    """为了得到静态页面HTML，有对页面反应超时的情况做了些延时处理"""
    i = 0
    while i < 5:
        try:
            html = requests.get(url=url0, headers=head, timeout=(10, 20))
            repeat = 0
            while (html.status_code != 200):  # 错误响应码重试
                print('error: ', html.status_code)
                time.sleep(20 + repeat * 5)
                repeat += 1
                html = requests.get(url=url0, headers=head, timeout=(10, 20))
                if (html.status_code != 200 and repeat == 2):
                    return html, repeat
            return html, repeat
        except requests.exceptions.RequestException:
            print('超时重试次数: ', i + 1)
            i += 1
    raise Exception()


def get_all_url():
    """得到商品中的所有链接"""
    url_before = 'https://www.amazon.com/dp/'
    files = os.listdir('/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/database')
    url_list = []
    for file in files:
        url_after = file[:-4]
        url_path = os.path.join(url_before,url_after)
        url_list.append(url_path)
    return url_list



def all_review_page(url_path):
    """翻到下一页"""
    """得到评论网页的链接"""
    browser = webdriver.Chrome(chrome_options=options)
    #browser = webdriver.Chrome(executable_path="chromedriver")
    browser.get(url_path)
    next_button = browser.find_element(By.XPATH,'//a[@data-hook="see-all-reviews-link-foot"]')
    next_button.click()
    new_url = browser.current_url

    return new_url



def get_review_function(url_link):
    """得到当前页面的评论"""
    req, error = gethtml(url_link, hea)  # 默认header
    if (type(req) == str):
        html = etree.HTML(req)
    else:
        html = etree.HTML(req.text)
    print(html)
    product_review = html.xpath('//span[@data-hook="review-body"]/span/text()')


    return product_review



def get_new_link(old_url):
    """通过当前页面，点击Next Page得到下一个页面的新链接"""
    # browser = webdriver.Chrome(executable_path="chromedriver")
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(old_url)
    next_button = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
    next_button.click()
    new_url = browser.current_url
    print(new_url)
    return new_url


if __name__ == '__main__':
    # product_url_path = 'https://www.amazon.com/rabbitgoo-Multi-Level-Scratching-Furniture-Climbing/dp/B0876ZGYP4/ref=sr_1_1_sspa?crid=2SV9YXLL6981T&keywords=cat%2Btree&qid=1651155266&sprefix=cat%2Btree%2Caps%2C803&sr=8-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUE5WEpYSzBPWjlPSjMmZW5jcnlwdGVkSWQ9QTAwNjc1NDEyT0NEWVE2UjdIQjVTJmVuY3J5cHRlZEFkSWQ9QTA4NTc1MzMxVkVXVU5QS1ozUUNPJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1'
    # url_path = 'https://www.amazon.com/'
    url_path = 'https://www.amazon.com/dp/B0921T6QFC'
    #all_review_page(url_path)
    get_new_link('https://www.amazon.com/Go-Pet-Club-Condo-67-Inch/product-reviews/B00BFFHPZM/ref=cm_cr_arp_mb_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2')


