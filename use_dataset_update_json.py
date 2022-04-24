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
    for index in range(1,10):
        if 'Question' in contents[index+1][:-1]:
            break
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
    answer_tmp_num = 0
    seller_list = []
    for key,contents in sample_qa.items():
        # key是问题，contents是顾客回答的问题，使用by分割
        answer[key] = []
        answer_tmp = []
        for content in contents:

            if "By" in content:
                answer[key].append(answer_tmp)
                answer_tmp_num +=1

                if 'SELLER' or 'MANUFACTURER' in content:
                    seller_list.append(answer_tmp[0])
                answer_tmp = []
            else:
                if 'Answer:' in content:
                    answer_tmp.append(content[7:])
                else:
                    answer_tmp.append(content)


    return ids,answer,five_point_item,answer_tmp_num,seller_list

def put_words_toghter(content):
    sentence = ''
    for index in range(len(content)):
        sentence = sentence + ' ' +content[index]
    return sentence

def generate_sample(ids,answer,five_point_item,seller_list):
    sample_dict = {}
    sample_dict['asin'] = ids
    sample_dict['highlights'] = five_point_item
    sample_dict['QAS'] = []
    aftersale_list = ['Dear','Best wishes','Sincerely','Wishes']#买家里面发现了'contact''Support'
    for key,contents in answer.items():
        QA_sample = {}  # 一个问题一个sample
        QA_sample["question"] = key
        QA_sample["answers"] = []
        for content in contents:
            tmp = {}
            sentence = put_words_toghter(content)
            tmp["answer"] = sentence
            tmp["is_seller"] = '0'
            #tmp["aftersale"] = 'buyer_service'  # aftersale表示售后,0表示顾客回答，1表示售后人员回答
            for check_content in content:
                #for sentive_word in aftersale_list:
                    # if sentive_word in check_content:
                    #     tmp["aftersale"] = 'seller_service'
                if check_content in seller_list:
                    tmp["is_seller"] = '1'

            QA_sample["answers"].append(tmp)
        sample_dict['QAS'].append(QA_sample)

    return sample_dict



def generate_json(folder_path,json_path):
    files = os.listdir(folder_path)
    all_sample_dict = {}
    all_sample_dict["samples"] = []
    question_num = 0
    answer_num = 0
    for file in files:
        file_path = osp.join(folder_path, file)
        ids, answer, five_point_item,answer_tmp_num,seller_list = read_txt(file_path)
        question_num +=len(answer)
        answer_num += answer_tmp_num
        sample_dict = generate_sample(ids, answer, five_point_item,seller_list)
        all_sample_dict["samples"].append(sample_dict)


    out_file = open(json_path, "w")
    json.dump(all_sample_dict, out_file, indent=6)
    print('问题个数',question_num)
    print('回答的个数',answer_num)


if __name__ == '__main__':
    folder_path = '/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/database'
    json_path = '/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/cattree.json'
    generate_json(folder_path, json_path)





