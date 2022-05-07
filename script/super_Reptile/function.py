"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/5/5 10:13 PM
"""
from selenium import webdriver
from time import sleep
import time
from lxml import etree
from selenium.webdriver.common.by import By
import requests
import os, json
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
    """得到所有商品页面链接"""
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

    html, repeat = gethtml(url_path, hea)
    html = etree.HTML(html.text)
    new_url = html.xpath('//a[@data-hook="see-all-reviews-link-foot"]/@href')
    new_url = 'https://www.amazon.com/' + new_url[0]
    return new_url

def get_new_link(old_url):
    """通过当前页面，点击Next Page得到下一个页面的新链接"""
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(old_url)
    next_button = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
    next_button.click()
    new_url = browser.current_url
    return new_url

def save_data(product_star,review_num,five_point_review,product_review,url):
    """通过传过来的数据保存到json文件下"""
    ids = url[-10:]
    sample_dict = {}
    sample_dict['asin'] = ids
    sample_dict['stars'] = product_star
    sample_dict['review_num'] = review_num
    sample_dict['highlights'] = five_point_review
    sample_dict['reviews'] = product_review
    json_path = os.path.join('/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/review_database/',ids+'.json')
    out_file = open(json_path, "w")
    json.dump(sample_dict, out_file, indent=6)

def generate_sample(buyer_id,star_user,time_gived,size_product,colour_product,verified_information,review,review_title,people_found_useful_information):
    """获得数据，输出字典形式的sample"""
    review_sample = {}#一个评价一个sample
    review_sample['author'] = buyer_id
    review_sample['stars'] = star_user
    review_sample['date'] = time_gived
    review_sample['is_verified_purchase'] = verified_information
    review_sample['size_product'] = size_product
    review_sample['colour_product'] = colour_product
    review_sample['people_found_useful_num'] = people_found_useful_information
    review_sample['review_title'] = review_title
    review_sample['review'] = review

    return review_sample

def get_review_function(url_link):
    """得到当前页面的评论"""
    html, _ = gethtml(url_link, hea)  # 默认header
    # ISO-8859-1
    html = etree.HTML(html.text)
    review_element = html.xpath('//div[@data-hook="review"]')
    # 商品购买信息
    review_sample_list = []
    # 商品购买信息
    products_information_list = html.xpath('//div[@class="a-section review aok-relative"]//a[@data-hook="format-strip"]/text()')

    for index in range(len(review_element)):
            sample = review_element[index]
            html_str = str(etree.tostring(sample))
            colour_product = ''
            size_product = ''
            buyer_id, star_user, time_gived, review_content, review_title = cope_string(html_str)
            current_str = html_str.split('<span data-hook="review-body"')[0]
            if 'Vine' in current_str:
                verified_information = 'Vine Customer Review of Free Product'
            else:
                verified_information = 'verified Purchase'
            try:
                if len(products_information_list)>len(review_element):
                    size_product = products_information_list[index*2]
                    colour_product = products_information_list[index*2+1]
                else:
                    colour_product = products_information_list[index]
            except IndexError:
                pass
            people_found_useful_information = get_found_useful_information_num(html_str)
            review_sample = generate_sample(buyer_id,star_user,time_gived,size_product,colour_product,verified_information,review_content,review_title,people_found_useful_information)
            review_sample_list.append(review_sample)
    return review_sample_list

def get_found_useful_information_num(html_str):
    """得到大家认为其有用信息的个数"""
    try:
        current_str = html_str.split('<div class="cr-helpful-button aok-float-left">')[0].split('cr-vote-text">')[1]
        people_found_useful_information =current_str.split(' &#')[0] + ' people found this helpful'
    except:
        people_found_useful_information = '0 people found this helpful'
    return people_found_useful_information


def cope_string(html_str):
    """处理网页中的字符串，过滤得到我们想要的东西"""
    # 用户的id
    account_str = html_str.split('/gp/profile/')[1]
    account = account_str.split('/')[0]
    # 用户给的🌟
    stars_buyer_gived_str = html_str.split('<span class="a-icon-alt">')[1]
    stars_buyer_gived = stars_buyer_gived_str.split('</span>')[0].split('&#')[0]
    # 接下来是用户评价的时间
    time_buyer_gived_str = html_str.split('review-date">')[1].split('</span><div class=')[0]
    review_content_str = html_str.split('data-hook="review-body"')[1]
    review_content = review_content_str.split('<span>')[1].split('</span>')[0]
    review_title_str = html_str.split('data-hook="review-title"')[1].split('<span data-hook="review-date"')[0]
    review_title = review_title_str.split('<span>')[1].split('</span>')[0]

    return account,stars_buyer_gived,time_buyer_gived_str,review_content,review_title



if __name__ == '__main__':
    options = initializate_options()
    url_path = 'https://www.amazon.com/dp/B0921T6QFC'
    url_path = 'https://www.amazon.com/Pawstory-Scratching-Multi-Level-Hammock-Furniture/product-reviews/B09FZ9ZV55/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2'
    #url_path = 'https://www.amazon.com/Pawstory-Scratching-Multi-Level-Hammock-Furniture/product-reviews/B09FZ9ZV55/ref=cm_cr_arp_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber=3'
    get_review_function(url_path)


