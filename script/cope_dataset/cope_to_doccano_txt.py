"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/4/26 12:04 PM
"""
import os, sys, shutil, json
import os.path as osp
import pandas as pd
import logging
from csv import DictReader
import numpy as np
# 生成一定格式的json文件
def read_json(json_path,out_json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    sample_list = json_data['samples']

    doccano = []
    for sample in sample_list:
        ids = sample['asin']
        highlights = sample['highlights']
        QAS_content = sample['QAs']
        for sample in QAS_content:
            question = sample['question']

            answer_content = sample['answers']
            for answer_sample in answer_content:
                single_sample = ''
                single_sample = 'question:'+question + '    answer:'+answer_sample['answer']
                doccano.append(single_sample)


    end_content = []
    for sample in doccano:
        # tmp = {}
        # tmp['QA_txt'] = sample
        end_content.append("{}\n".format(sample))

    with open('../../test.txt', 'w') as fp:
        fp.writelines(end_content)
    # out_file = open(out_json_path, "w")
    # json.dump(tmp_all, out_file, indent=6)






if __name__ == '__main__':
    json_path = '/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/new_cattree.json'
    out_json_path = '/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/test.json'
    read_json(json_path,out_json_path)
