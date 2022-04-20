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


def generate_json(json_path):
    sample_dict = {}
    sample_dict["samples"] = []
    for index in range(30):
        sample_content = {}
        sample_content['sample_number'] = "{}".format(str(index))
        sample_content['QA'] = ""
        sample_content['five_points'] = ""
        sample_dict["samples"].append(sample_content)
    out_file = open(json_path, "w")
    json.dump(sample_dict,out_file, indent=6)
if __name__ == '__main__':
    json_path = '/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/cattree.json'
    generate_json(json_path)


