"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/5/23 5:35 PM
"""
from translate import Translator
translator= Translator(to_lang="zh")
from tqdm import tqdm
def analyse_txt():
    with open('./question.txt','r') as fp:
        contents = fp.readlines()
    en_zh_list = []
    for sample in tqdm(contents):
        tmp_sentence = sample[:-1]
        translation = translator.translate(tmp_sentence)
        en_zh_list.append("{} *** {}\n".format(tmp_sentence,translation))
    with open('./en_zh_question.txt') as f:
        f.writelines(en_zh_list)
analyse_txt()
# translation = translator.translate("")
