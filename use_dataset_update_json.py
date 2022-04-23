"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/4/22 5:45 PM
"""
import os, sys, shutil, json
import os.path as osp

def read_txt(txt_path):
    """通过读取txt来得到信息"""
    with open(txt_path,'r') as fp:
        contents = fp.readlines()
    ids = osp.basename(txt_path)[:-4]
    five_point_item = []
    for index in range(1,6):
        five_point_item.append(contents[index+1][:-1])
    sample_qa = {}
    for index in range(len(contents)):
        line_content = contents[index][:-1]
        if 'Question' in line_content:
            question_item = line_content[9:]

            sample_qa[question_item] = []
            # 获得answer内容
            for answer_index in range(index+1,len(contents)):
                if 'Question' in contents[answer_index][:-1]:
                    break
                sample_qa[question_item].append(contents[answer_index][:-1])
    answer = {}
    for key,contents in sample_qa.items():
        # key是问题，contents是顾客回答的问题，使用by分割
        answer[key] = []
        answer_tmp = []
        for content in contents:
            if "By" in content:
                answer[key].append(answer_tmp)
                answer_tmp = []
            else:
                if 'Answer:' in content:
                    answer_tmp.append(content[7:])
                else:
                    answer_tmp.append(content)


    return ids,answer,five_point_item


def generate_sample(ids,answer,five_point_item):
    sample_dict = {}
    sample_dict['id'] = ids
    sample_dict['five_points'] = five_point_item
    sample_dict['QA'] = []
    aftersale_list = ['Dear','Best wishes','Support','contact','Sincerely']
    for key,contents in answer.items():
        QA_sample = {}  # 一个问题一个sample
        QA_sample["question"] = key
        QA_sample["QA_answer"] = []

        for content in contents:
            tmp = {}
            tmp["answer"] = content
            tmp["aftersale"] = 'buyer_service'  # aftersale表示售后,0表示顾客回答，1表示售后人员回答
            for check_content in content:
                for sentive_word in aftersale_list:
                    if sentive_word in check_content:
                        tmp["aftersale"] = 'seller_service'

            QA_sample["QA_answer"].append(tmp)
        sample_dict['QA'].append(QA_sample)

    return sample_dict



def generate_json(folder_path,json_path):
    files = os.listdir(folder_path)
    all_sample_dict = {}
    all_sample_dict["samples"] = []
    for file in files:
        file_path = osp.join(folder_path, file)
        ids, answer, five_point_item = read_txt(file_path)
        sample_dict = generate_sample(ids, answer, five_point_item)
        all_sample_dict["samples"].append(sample_dict)
    out_file = open(json_path, "w")
    json.dump(all_sample_dict, out_file, indent=6)


if __name__ == '__main__':
    folder_path = '/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/database'
    json_path = '/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/cattree.json'
    generate_json(folder_path, json_path)





