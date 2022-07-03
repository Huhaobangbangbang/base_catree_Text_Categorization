"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/7/2 10:06 AM
"""
import os, sys, shutil, json
import os.path as osp
import pandas as pd
import logging
import numpy as np


def get_question_to_dict(json_path):
    """ 得到问题对应标签的字典"""
    question_to_dict = {}
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    for sample in json_data:

        try:
            en_text = sample['data']['text'].split('***')[0]
            label = sample['annotations'][0]['result'][0]['value']['choices'][0]
            if label == 'yes':
                tmp_label = 1
            elif label == 'no':
                tmp_label = 0
            question_to_dict[en_text] = tmp_label
        except:
            tmp_label = 0
            question_to_dict[en_text] = tmp_label

    return question_to_dict


def check_difference(company_question_to_dict,hu_question_to_dict):
    """查找差异"""
    diff_txt = []
    for sample in company_question_to_dict:
        if company_question_to_dict[sample]!=hu_question_to_dict[sample]:
            diff_txt.append("{} {}\n".format(sample,hu_question_to_dict[sample],))
    with open('diff.txt','w') as fp:
        fp.writelines(diff_txt)

if __name__ == '__main__':
    json_path = '/Users/huhao/Downloads/catree_personality_others.json'
    company_question_to_dict = get_question_to_dict(json_path)
    json_path = '/Users/huhao/Downloads/catree_personality_2.0.json'
    hu_question_to_dict = get_question_to_dict(json_path)
    check_difference(company_question_to_dict, hu_question_to_dict)













