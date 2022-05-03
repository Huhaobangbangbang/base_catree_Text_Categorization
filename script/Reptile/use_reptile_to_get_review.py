"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/4/28 9:54 PM
"""
import requests
from lxml import etree
import time
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from function import get_all_url,all_review_page,get_review_function
from tqdm import tqdm
from function import get_new_link #这个函数是点击Next page得到下一个页面
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

hea_0 = {
        #'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        #'accept-encoding': 'gzip, deflate, br',
        #'accept-language': 'zh-CN,zh;q=0.9',
        #'cache-control': 'max-age=0',
        'downlink': '1.5',
        'ect': '3g',
        'rtt': '300',
        #'Cookie': "session-id=141-3132077-2152004; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_CN; sp-cdn=\"L5Z9:CN\"; x-wl-uid=10tVwZ45eSXqIpeD5HaRaEZWh15W7H+vfi+XqqFlEGrT7tDZnDY5T/tN95e+9xgX+MWXBse7hC5A=; ubid-main=134-3335690-9399343; session-token=2+RCbdp4M2oj5rIKbi4cUwACUf85OmSwpSfM6Ivx6nA2Bi4hINPvjwpQy2IQvZxkN/xqDCLmTyBDTXaZxBGrEWhyHTEkhFb4He197smVmXFqsEIhF8GoSsCyJNctIJZWR1SJkbd/liAdOpkdAUYV59W+4xnXcq/ZJMQ0RkCkmis8aFuu7JKH6VmFoZv9QeIA; csm-hit=tb:G2VNCYGMS99K5WSAF3WK+s-M9HQ7RS4JN5SAWD8M20Z|1594365538625&t:1594365538625&adb:adblk_no",
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.8 Safari/537.36'
    }

# 数据导入
#url_list = ['https://www.amazon.com/BEWISHOME-Scratching-Perches-Kitten-MMJ20L/dp/B09DG3L7XW/ref=sr_1_1_sspa?crid=BSR7GFCGZCQ2&keywords=cat+tree&qid=1651475245&sprefix=cat+tree%2Caps%2C410&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzTFNVVTE0T1Y3WVVXJmVuY3J5cHRlZElkPUEwNTc1NTUxM1FQS05CNDA4N01BUCZlbmNyeXB0ZWRBZElkPUExMDM0ODk1TFgzSkVGS1pVWTlJJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==',  # 美国
#            'https://www.amazon.com/Indoor-Cats%EF%BC%8CMulti-Level-Scratching-Climbing-Kittens/dp/B09JS3BTSL/ref=sr_1_2_sspa?crid=BSR7GFCGZCQ2&keywords=cat+tree&qid=1651475858&sprefix=cat+tree%2Caps%2C410&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyVEVDVjJKRkdIOVJGJmVuY3J5cHRlZElkPUEwOTUyOTg5M0kzUFRHMlFRRkg3NCZlbmNyeXB0ZWRBZElkPUEwMzE3Nzk0NVpMNjBFNUFVR0RFJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==',
#           'https://www.amazon.com/deformable-Apartment-Furniture-Activity-Center/dp/B08YMTC4L3/ref=sr_1_3_sspa?crid=BSR7GFCGZCQ2&keywords=cat%2Btree&qid=1651475858&sprefix=cat%2Btree%2Caps%2C410&sr=8-3-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyVEVDVjJKRkdIOVJGJmVuY3J5cHRlZElkPUEwOTUyOTg5M0kzUFRHMlFRRkg3NCZlbmNyeXB0ZWRBZElkPUEwOTgxMzI0VDlBQTgzNEhNVEY1JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1']
url_list = get_all_url()

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


def change_address(postal):
    while True:
        try:
            driver.find_element_by_id('glow-ingress-line1').click()
            # driver.find_element_by_id('nav-global-location-slot').click()
            time.sleep(1)
        except Exception as e:
            driver.refresh()
            time.sleep(3)
            continue
        try:
            driver.find_element_by_id("GLUXChangePostalCodeLink").click()
            time.sleep(2)
        except:
            pass
        try:
            driver.find_element_by_id('GLUXZipUpdateInput').send_keys(postal)
            time.sleep(1)
            break
        except Exception as NoSuchElementException:
            try:
                driver.find_element_by_id('GLUXZipUpdateInput_0').send_keys(postal.split('-')[0])
                time.sleep(1)
                driver.find_element_by_id('GLUXZipUpdateInput_1').send_keys(postal.split('-')[1])
                time.sleep(1)
                break
            except Exception as NoSuchElementException:
                driver.refresh()
                time.sleep(3)
                continue
        print("重新选择地址")
    driver.find_element_by_id('GLUXZipUpdate').click()
    time.sleep(1)
    driver.refresh()


def get_price_id(html):
    """获得商品价格"""
    x_price = html.xpath('//span[@class="a-offscreen"]/text()')  # 价格
    try:
        product_price = x_price[0]
    except:
        product_price = '0'

    return product_price

def get_id(html):
    product_id = html.xpath('//input[@id="ftSelectAsin"]/@value')  # id//*[@id="ftSelectAsin"]
    print(product_id)
    return product_id


def get_items(req):
    """使用Xpath解析页面，提取商品信息"""
    if (type(req) == str):
        html = etree.HTML(req)
    else:
        html = etree.HTML(req.text)
    #商品总体评分
    product_star = html.xpath('//div[@id="averageCustomerReviews_feature_div"]//span[@id="acrPopover"]/@title')[0]  # 星级
    print(product_star)
    product_rate0 = html.xpath('//div[@id="averageCustomerReviews_feature_div"]//span[@id="acrCustomerReviewText"]/text()')[
        0]  # 评论总数
    review_num = re.sub("\D", "", product_rate0)
    print('评论总数: ', review_num)
    # 商品的5点
    five_point_review = html.xpath('//div[@id="featurebullets_feature_div"]//ul//span[@class="a-list-item"]/text()')  # 五点描述

    return product_star,review_num,five_point_review





def get_review(driver,url_path,review_num):
    """得到商品评价"""
    product_review = []
    tmp_link = all_review_page((url_path))
    index = 0
    while(len(product_review)<int(review_num)):
        try:
            review_tmp = get_review_function(tmp_link)
            product_review += review_tmp
            tmp_link = get_new_link(tmp_link)
            print(len(product_review))
            index+=1
            if index>5:
                break
        except:
            product_review = list(set(product_review))
    product_review = list(set(product_review))
    print('此商品采集的评论个数为：',len(product_review))
    return product_review


if __name__ == '__main__':
    #启动并初始化Chrome
    options = webdriver.ChromeOptions()  # 初始化Chrome
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("disable-web-security")
    options.add_argument('disable-infobars')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(chrome_options=options)
    #driver = webdriver.Chrome( executable_path = "chromedriver") #可视化执行任务
    wait = WebDriverWait(driver, 20)
    driver.maximize_window()
    row = 2
    # 修改邮政编码为20237（华盛顿），进而得到美国的正确价格
    search_page_url = 'https://www.amazon.com/s?k=cat+tree'
    postal = "20237"  # 华盛顿
    print("正在爬取初始页面", search_page_url)
    driver.get(search_page_url)
    time.sleep(1)
    change_address(postal)  # 更改邮寄地址
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-list")))
    for url in tqdm(url_list):
        req, error = gethtml(url, hea)  # 默认header
        product_star,review_num,five_point_review = get_items(req)

        product_review = get_review(driver,url,review_num)
        break

    driver.quit()  # 关闭浏览器


