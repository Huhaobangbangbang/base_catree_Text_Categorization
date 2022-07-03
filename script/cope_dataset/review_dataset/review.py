"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/7/3 9:46 PM
"""
import os, sys, shutil, json
import os.path as osp
import pandas as pd
import numpy as np
from yaml import dump
import os, sys, shutil, json
import os.path as osp
import pandas as pd
import numpy as np
from tqdm import tqdm
import random


def generate_json(dataset_path, dataset_name, positive_sample_list, negative_sample_list, netural_sample_all):
    """生成json文件"""
    index = 0
    random.shuffle(positive_sample_list)
    random.shuffle(negative_sample_list)
    random.shuffle(netural_sample_all)
    val_num = 0
    for cope_sample in tqdm(positive_sample_list):
        train_num = int(len(positive_sample_list) / 10 * 7)
        test_num = int(len(positive_sample_list) / 10 * 9)
        index += 1
        train_path = osp.join(dataset_path, 'train', "{}_{}.json".format(index, dataset_name))
        val_path = osp.join(dataset_path, 'val', "{}_{}.json".format(index, dataset_name))
        test_path = osp.join(dataset_path, 'test', "{}_{}.json".format(index, dataset_name))
        if index < test_num and index > train_num:
            out_file = open(val_path, "w")
            json.dump(cope_sample, out_file, indent=6)
            val_num += 1
        if index <= train_num:
            out_file = open(train_path, "w")
            json.dump(cope_sample, out_file, indent=6)
        if index >= test_num:
            out_file = open(test_path, "w")
            json.dump(cope_sample, out_file, indent=6)
    n_index = 0
    print(val_num)
    for cope_sample in tqdm(negative_sample_list):
        train_num = int(len(negative_sample_list) / 10 * 7)
        test_num = int(len(negative_sample_list) / 10 * 9)
        index += 1
        n_index += 1
        train_path = osp.join(dataset_path, 'train', "{}_{}.json".format(index, dataset_name))
        val_path = osp.join(dataset_path, 'val', "{}_{}.json".format(index, dataset_name))
        test_path = osp.join(dataset_path, 'test', "{}_{}.json".format(index, dataset_name))
        if n_index < test_num and n_index > train_num:
            out_file = open(val_path, "w")
            json.dump(cope_sample, out_file, indent=6)
            val_num += 1
        if n_index <= train_num:
            out_file = open(train_path, "w")
            json.dump(cope_sample, out_file, indent=6)
        if n_index >= test_num:
            out_file = open(test_path, "w")
            json.dump(cope_sample, out_file, indent=6)
    print(val_num)
    k_index = 0
    for cope_sample in tqdm(netural_sample_all):
        train_num = int(len(netural_sample_all) / 10 * 7)
        test_num = int(len(netural_sample_all) / 10 * 9)
        index += 1
        k_index += 1
        train_path = osp.join(dataset_path, 'train', "{}_{}.json".format(index, dataset_name))
        val_path = osp.join(dataset_path, 'val', "{}_{}.json".format(index, dataset_name))
        test_path = osp.join(dataset_path, 'test', "{}_{}.json".format(index, dataset_name))
        if k_index < test_num and k_index > train_num:
            out_file = open(val_path, "w")
            json.dump(cope_sample, out_file, indent=6)
            val_num += 1

        if k_index <= train_num:
            out_file = open(train_path, "w")
            json.dump(cope_sample, out_file, indent=6)
        if k_index >= test_num:
            out_file = open(test_path, "w")
            json.dump(cope_sample, out_file, indent=6)
    print(val_num)


# 生成一定格式的json文件
def read_json(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    pos_sample = []
    neg_sample = []
    netural_sample = []
    sample_list = json_data['reviews']
    for sample in sample_list:
        point = int(sample['stars'][:1])
        review_content = sample['review']
        review_sample = {}
        review_sample['text'] = review_content

        if point <= 2:
            review_sample['label'] = 0
            neg_sample.append(review_sample)
        if point >= 4:
            review_sample['label'] = 1
            pos_sample.append(review_sample)
        if point == 3:
            review_sample['label'] = 2
            netural_sample.append(review_sample)
    return neg_sample, pos_sample, netural_sample


def generate_all_samples(pos_sample_all, neg_sample_all, netural_sample_all):
    """生成所有样本的json"""
    sample_list = pos_sample_all + neg_sample_all + netural_sample_all
    review_sample = {}
    review_sample['samples'] = sample_list
    out_file = open(
        '/cloud/cloud_disk/users/huh/nlp/base_catree_Text_Categorization/script/cope_dataset/review_dataset/postive_negitive_review_dataset/data.json',
        "w")
    json.dump(review_sample, out_file, indent=6)
    print('总例子个数为', len(sample_list))


if __name__ == '__main__':
    folder_path = '/cloud/cloud_disk/users/huh/nlp/base_catree_Text_Categorization/script/super_Reptile/data'
    json_list = os.listdir(folder_path)
    pos_sample_all = []
    neg_sample_all = []
    netural_sample_all = []
    for json_name in json_list:
        json_path = osp.join(folder_path, json_name)
        neg_sample, pos_sample, netural_sample = read_json(json_path)
        pos_sample_all += pos_sample
        neg_sample_all += neg_sample
        netural_sample_all += netural_sample
    # dataset_path = '/cloud/cloud_disk/users/huh/nlp/base_catree_Text_Categorization/script/cope_dataset/review_dataset/postive_negitive_review_dataset'
    # dataset_name = dataset_path.split('/')[-1]
    # print(len(pos_sample_all),len(neg_sample_all),len(netural_sample_all))
    # generate_json(dataset_path,dataset_name,pos_sample_all,neg_sample_all,netural_sample_all)
    generate_all_samples(pos_sample_all, neg_sample_all, netural_sample_all)