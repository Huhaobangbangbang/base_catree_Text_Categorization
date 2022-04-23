"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/4/20 4:48 PM
"""

import os, sys, shutil, json
import os.path as osp
import pandas as pd
import logging
from csv import DictReader
import numpy as np
# 初级版本，生成一定格式的json文件，然后自己把数据填上去

def generate_json(json_path):
    sample_dict = {}
    sample_dict["samples"] = []
    for index in range(60):
        sample_content = {}
        #sample_content['sample_number'] = "{}".format(str(index))
        sample_content['id'] = ""
        sample_content['five_points'] = ""
        sample_dict["samples"].append(sample_content)
        sample_content['QA'] = []
        for index in range(5):
            QA_sample = {}
            QA_sample["sample_index"] = "{}".format(str(index+1))
            QA_sample["question"] = ""
            QA_sample["answer"] = ""
            QA_sample["customer_service"] = ""#1代表是客服，代表非客服
            sample_content['QA'].append(QA_sample)
    out_file = open(json_path, "w")
    json.dump(sample_dict,out_file, indent=6)
if __name__ == '__main__':
    json_path = '/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/new_cattree.json'
    generate_json(json_path)


