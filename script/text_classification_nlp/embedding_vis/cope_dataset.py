"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/6/30 7:19 PM
"""
import os, sys, shutil, json
import os.path as osp
import pandas as pd
import logging
import numpy as np


def analyse_json(json_path):
    # 生成一定格式的json文件
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    dataset_list = []
    huggingface_dataset = {}
    num = len(json_data)
    train_num = int(num / 10) * 7
    test_num = int(num / 10 * 9)
    for sample in json_data:
        cope_sample = {}
        try:
            en_text = sample['data']['text'].split('***')[0]
            label = sample['annotations'][0]['result'][0]['value']['choices'][0]
            if label == 'yes':
                tmp_label = 1
            elif label == 'no':
                tmp_label = 0
            else:
                break
            cope_sample['text'] = en_text
            cope_sample['label'] = tmp_label

            dataset_list.append(cope_sample)
            # dataset_list.append("{} {}\n".format(en_text,tmp_label))

        except:
            pass

    huggingface_dataset['train'] = dataset_list[:train_num]
    huggingface_dataset['unsupervised'] = dataset_list[train_num:test_num]
    huggingface_dataset['test'] = dataset_list[test_num:]
    json_path = '/cloud/cloud_disk/users/huh/dataset/nlp_dataset/question_dataset/process_data/cattree_personality.json'
    out_file = open(json_path, "w")
    json.dump(huggingface_dataset, out_file, indent=6)
    return huggingface_dataset


def put_wrong_sample_into_txt():
    wrong_sample_folder = '/cloud/cloud_disk/users/huh/dataset/nlp_dataset/question_dataset/process_data/catree_personality_2.0/wrong_sample'
    wrong_sample_list = os.listdir(wrong_sample_folder)
    wrong_txt_list = []
    for sample in wrong_sample_list:
        sample_path = osp.join(wrong_sample_folder, sample)
        with open(sample_path, 'r') as f:
            json_data = json.load(f)

        wrong_txt_list.append("{} {}\n".format(json_data['text'], json_data['label']))
    with open(
            '/cloud/cloud_disk/users/huh/dataset/nlp_dataset/question_dataset/process_data/catree_personality_2.0/wrong_sample.txt',
            'w') as fp:
        fp.writelines(wrong_txt_list)


def get_unrepeat_txt():
    json_path = '/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/script/text_classification_nlp/embedding_vis/catree_personality_2.0.json'
    # 生成一定格式的json文件
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    str_en_text = []
    for sample in json_data:
        en_text = sample['data']['text'].split('***')[0]
        # str_en_text += en_text+' '
        str_en_text.append("{}\n".format(en_text))
    return str_en_text


def get_unrepeat_str():
    json_path = '/cloud/cloud_disk/users/huh/dataset/nlp_dataset/question_dataset/ori/en_ch_cattree_personality.json'
    # 生成一定格式的json文件
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    str_en_text = ''
    for sample in json_data:
        en_text = sample['data']['text'].split('***')[0]
        str_en_text += en_text + ' '

    return str_en_text


if __name__ == '__main__':
    json_path = '/cloud/cloud_disk/users/huh/dataset/nlp_dataset/question_dataset/ori/en_ch_cattree_personality.json'
    # analyse_json(json_path)
    # str_en_text = get_unrepeat_txt(json_path)














    str_en_text = get_unrepeat_txt()
    with open('/cloud/cloud_disk/users/huh/dataset/nlp_dataset/question_dataset/scripts/huhao.txt', 'w') as fp:
        fp.writelines(str_en_text)
