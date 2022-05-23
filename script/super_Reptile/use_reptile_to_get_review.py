"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/5/5 10:12 PM
"""
import os
import random
from lxml import etree
import re
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from function import get_all_url,all_review_page,get_review_function
from function import get_new_link,save_data #这个函数是点击Next page得到下一个页面,save_data函数是将已有信息保存到json
from function import gethtml  # 为了得到静态页面HTML，有对页面反应超时的情况做了些延时处理
from tqdm import tqdm
from time import sleep#,zh-CN,zh;q=0.9
hea = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'En-Us',
    'cache-control': 'max-age=0',
    'downlink': '8',
    'ect': '4g',
    'rtt': '250',
    'Cookie': "session-id=257-3500989-3695223; i18n-prefs=GBP; ubid-acbuk=257-5950834-2508848; x-wl-uid=1bEcLG2b03/1tAwPJNyfuRH+U7J9ZaPYejSBR4HXKuYQPJtLhQbDYyO/GOMypGKXqZrG7qBkS0ng=; session-token=x04EF8doE84tE+6CXYubsjmyob/3M6fdmsQuqzD0jwl/qGdO5aRc2eyhGiwoD0TFzK1rR/yziHsDS4v6cdqT2DySFXFZ9I5OHEtgufqBMEyrA0/Scr87KKA+GWOjfVmKRuPCqOGaixZQ6AIjU3e2iFOdM+3v90NeXFI3cazZcd6x9TYCy9b5u9V8zR7ePbdP; session-id-time=2082758401l; csm-hit=tb:MAA188S1G57TNTH6HQCZ+s-T9EGT4C8FC8J74X5T7CY|1594212767446&t:1594212767446&adb:adblk_no",
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
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


def initializate_options():
    """初始化"""
    # 启动并初始化Chrome
    options = webdriver.ChromeOptions()  # 初始化Chrome
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("disable-web-security")
    options.add_argument('disable-infobars')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    return options
options = initializate_options()


def get_price(html):
    """获得商品价格"""
    x_price = html.xpath('//span[@class="a-offscreen"]/text()')  # 价格
    try:
        product_price = x_price[0]
    except:
        product_price = '0'
        print('product_price无法读取')

    return product_price


def get_items(req):
    """使用Xpath解析页面，提取商品信息"""
    if (type(req) == str):
        html = etree.HTML(req)
    else:
        html = etree.HTML(req.text)
    #商品总体评分
    #product_star = html.xpath('//div[@id="averageCustomerReviews_feature_div"]//span[@id="acrPopover"]/@title')[0]  # 星级
    product_star = html.xpath('//div[@id="averageCustomerReviews_feature_div"]//@title')
    product_rate0 = html.xpath('//span[@id="acrCustomerReviewText"]/text()')[0]  # 评论总数
    review_num = re.sub("\D", "", product_rate0)
    print('参与打分的总人数: ', review_num)
    # 商品的5点
    five_point_review = html.xpath('//div[@id="featurebullets_feature_div"]//ul//span[@class="a-list-item"]/text()')  # 五点描述

    return product_star,review_num,five_point_review


def get_review(url_path,review_num):
    """得到商品评价"""
    product_review = [] #所有页面的评论信息
    tmp_link = all_review_page(url_path)
    while(len(product_review)<int(review_num)):
        try:
            review_tmp = get_review_function(tmp_link)
            product_review += review_tmp
            tmp_link = get_new_link(tmp_link) # 翻到下一页
            if tmp_link =='':
                print('已经采集了',len(product_review),'条数据')
                break
        #except selenium.common.exceptions.NoSuchElementException:
        except:
            if len(product_review)<20:
                print('采集失败')
                break
            else:
                print('已经采集了',len(product_review),'条数据')
                break
    return product_review


def get_already_coped():
    files = os.listdir('/cloud/cloud_disk/users/huh/nlp/base_catree_Text_Categorization/script/super_Reptile/data')
    already_coped = []
    for file in files:
        already_coped.append(file[:-5])
    return already_coped

if __name__ == '__main__':
    #启动并初始化Chrome
    url_list = get_all_url()

    already_coped_list = get_already_coped()
    for url in tqdm(url_list):
            if url[-10:] in already_coped_list:
                pass
            else:
                stop_time= random.uniform(60,150)
                sleep(stop_time)
                driver = webdriver.Chrome(chrome_options=options)
                wait = WebDriverWait(driver, 20)
                postal = "20237"  # 华盛顿
                print("正在爬取初始页面", url)
                driver.get(url)
                req, error = gethtml(url, hea)  # 默认header
                product_star,review_num,five_point_review = get_items(req)
                product_review = get_review(url,review_num)
                save_data(product_star, review_num, five_point_review, product_review, url)
                driver.quit()  # 关闭浏览器






