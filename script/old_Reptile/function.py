"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/4/28 9:54 PM
"""
from selenium import webdriver
from time import sleep
import time
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import requests
import os, sys, shutil, json

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


def get_new_link(old_url):
    """通过当前页面，点击Next Page得到下一个页面的新链接"""
    # browser = webdriver.Chrome(executable_path="chromedriver")
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



def get_review_function(url_link):
    """得到当前页面的评论"""
    req, error = gethtml(url_link, hea)  # 默认header
    if (type(req) == str):
        html = etree.HTML(req)
    else:
        html = etree.HTML(req.text)
    review_element = html.xpath('//div[@class="a-section review aok-relative"]')
    # 这个profile_element是提取的用户账号链接，从而提取到用户的id
    profile_element = html.xpath('//div[@class="a-section review aok-relative"]/div/div/div/a[@class="a-profile"]/@href')
    # stars_buyer_gived是用户给的🌟
    stars_buyer_gived = html.xpath('//div[@class="a-section review aok-relative"]/div/div//i[@data-hook="review-star-rating"]/span[@class="a-icon-alt"]/text()')
    # 接下来是用户评价的时间
    time_buyer_gived = html.xpath('//div[@class="a-section review aok-relative"]/div/div/span[@data-hook="review-date"]/text()')
    # 商品购买信息
    products_information_list = html.xpath('//div[@class="a-section review aok-relative"]//a[@data-hook="format-strip"]/text()')
    #认为这个评价有用的人的个数，但是没人评价的就没有展示
    people_found_useful = html.xpath('//div[@class="a-section review aok-relative"]//span[@data-hook="helpful-vote-statement"]/text()')
    #用户的认证信息//div[@data-hook="mobley-review-content"]//span[@data-hook="msrp-avp-badge-linkless"]/text()
    verified_nonverified = html.xpath('//div[@class="a-section review aok-relative"]//span[@class="a-size-mini a-color-state a-text-bold"]/text()')

    #reviews_content = html.xpath('//div[@class="a-section review aok-relative"]//span[class="review-text-sub-contents"]/text()')
    reviews_content = html.xpath('//span[@data-hook="review-body"]/span/text()')  #  //span[@data-hook="review-body"]/span/text()是没有see more的

    #reviews_content = get_see_more_content(reviews_content)
    print(len(review_element),len(profile_element))
    sample_list = []
    for index in range(len(review_element)):
        try:
            buyer_id = profile_element[index].split('/')[3]

            star_user_str = stars_buyer_gived[index]
            star_user = str(star_user_str).split('，')[0]
            time_gived = time_buyer_gived[index]
            if len(products_information_list)>len(review_element):
                size_product = products_information_list[index*2]
                colour_product = products_information_list[index*2+1]
                verified_information = verified_nonverified[index]
                review = reviews_content[index]
                sample = generate_sample(buyer_id, star_user, time_gived, size_product, colour_product,
                                         verified_information, review)
                sample_list.append(sample)
            else:
                colour_product = products_information_list[index]
                verified_information = verified_nonverified[index]
                review = reviews_content[index]
                sample = generate_sample(buyer_id,star_user,time_gived,colour_product,verified_information,review)
                sample_list.append(sample)
        except:
            pass

    return sample_list



def generate_sample(buyer_id,star_user,time_gived,size_product,colour_product,verified_information,review):
    """获得数据，输出字典形式的sample"""
    review_sample = {}#一个评价一个sample
    review_sample['author'] = buyer_id
    review_sample['stars'] = star_user
    review_sample['date'] = time_gived
    review_sample['is_verified_purchase'] = verified_information
    review_sample['size_product'] = size_product
    review_sample['colour_product'] = colour_product
    review_sample['review'] = review

    return review_sample



def generate_sample(buyer_id,star_user,time_gived,colour_product,verified_information,review):
    """一些评论无商品信息"""
    review_sample = {}#一个评价一个sample
    review_sample['author'] = buyer_id
    review_sample['stars'] = star_user
    review_sample['date'] = time_gived
    review_sample['is_verified_purchase'] = verified_information
    review_sample['colour_product'] = colour_product
    review_sample['review'] = review

    return review_sample

def get_see_more_content(reviews_content):
    """得到see more 中的内容，去除隐藏内容"""
    new_reviews_content = []
    print(len(reviews_content))
    for index in range(1,len(reviews_content)):
        # 隐藏内容比see more中的内容在先
        first_content = reviews_content[index-1]
        later_content = reviews_content[index]
        if first_content[:-3] in later_content:
            new_reviews_content.append(later_content)
            print(later_content)
        else:
            new_reviews_content.append(first_content)
    new_reviews_content = list(set(new_reviews_content))
    return new_reviews_content




if __name__ == '__main__':
    # product_url_path = 'https://www.amazon.com/rabbitgoo-Multi-Level-Scratching-Furniture-Climbing/dp/B0876ZGYP4/ref=sr_1_1_sspa?crid=2SV9YXLL6981T&keywords=cat%2Btree&qid=1651155266&sprefix=cat%2Btree%2Caps%2C803&sr=8-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUE5WEpYSzBPWjlPSjMmZW5jcnlwdGVkSWQ9QTAwNjc1NDEyT0NEWVE2UjdIQjVTJmVuY3J5cHRlZEFkSWQ9QTA4NTc1MzMxVkVXVU5QS1ozUUNPJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1'
    # url_path = 'https://www.amazon.com/'
    url_path = 'https://www.amazon.com/dp/B0921T6QFC'
    url_path = 'https://www.amazon.com/Pawstory-Scratching-Multi-Level-Hammock-Furniture/product-reviews/B09FZ9ZV55/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
    get_review_function(url_path)




