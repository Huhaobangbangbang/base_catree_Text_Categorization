
import os
import random
from lxml import etree
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from time import sleep#,zh-CN,zh;q=0.9
def get_all_url():
    """得到所有商品页面链接"""
    url_before = 'https://www.amazon.com/dp/'
    files = os.listdir('/cloud/cloud_disk/users/huh/nlp/base_catree_Text_Categorization/review_ori_database')
    url_list = []
    for file in files:
        url_after = file[:-4]
        url_path = os.path.join(url_before,url_after)
        url_list.append(url_path)
    return url_list
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
def gethtml(url0, head):
    """为了得到静态页面HTML，有对页面反应超时的情况做了些延时处理"""
    i = 0
    stop_time= random.uniform(1,5)
    sleep(stop_time)
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
def get_items(req):
    """使用Xpath解析页面，提取商品信息"""
    if (type(req) == str):
        html = etree.HTML(req)
    else:
        html = etree.HTML(req.text)
    #商品问题链接
    # question_link = html.xpath('/a[@class="a-link-normal"]/@href')
    # question_list = []
    # for question in question_link:
    #     if 'questions' in question:
    #         question_list.append(question)

    # question_list = html.xpath('//span[@data-csa-c-func-deps="aui-da-ask-log-click-csm"]/text()')
    behind_link = str(req.text).split('">See questions and answers</a>')[0].split('<a href="https://www.amazon.com/ask/questions/asin/')[1]
    end_link = 'https://www.amazon.com/ask/questions/asin/'+behind_link
    return end_link

def get_already_coped():
    files = os.listdir('/cloud/cloud_disk/users/huh/nlp/smart_home/dataset/coped_data')
    already_coped = []
    for file in files:
        already_coped.append(file[:-5])
    return already_coped


def get_id_to_link():
    #启动并初始化Chrome
    url_list = get_all_url()
    print(url_list)
    id_to_link_dict = {}
    for url in tqdm(url_list):
            driver = webdriver.Chrome(chrome_options=options)
            wait = WebDriverWait(driver, 20)
            print("正在爬取初始页面", url)
            driver.get(url)
            req, error = gethtml(url, hea)  # 默认header
            end_link = get_items(req)
            driver.quit()  # 关闭浏览器
            sleep(1)
            print(end_link)
            print(url.split('/')[-1])
            id_to_link_dict[url.split('/')[-1]] = end_link
            
    return id_to_link_dict                

id_to_link_dict = get_id_to_link()
json_path = '/cloud/cloud_disk/users/huh/nlp/smart_home/script/emdbedding/test.json'
out_file = open(json_path, "w")
import json
print(id_to_link_dict)
json.dump(id_to_link_dict, out_file, indent=6)

