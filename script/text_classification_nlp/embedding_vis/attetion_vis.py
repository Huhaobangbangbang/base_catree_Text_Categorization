"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/6/19 12:21 PM
"""
# import spacy
# from spacy import displacy
# # nlp = spacy.load('en_core_web_sm')
# # piano_class_text = (' My cats is situated  '  ' How many scratch posts does this piece have? '
# #   'Has anyone  cat ever used the ladder? Mine really isnt much of a jumper, and she may actually need to use it. ')
#
# piano_class_text = ('Great Piano Academy is situated'
#     ' in Mayfair or the City of London and has'
#      ' world-class piano instructors.')
# nlp = spacy.load('en_core_web_sm')
# piano_class_doc = nlp(piano_class_text)
# for ent in piano_class_doc.ents:
#     print(ent.text, ent.start_char, ent.end_char,
#           ent.label_, spacy.explain(ent.label_))
#
# displacy.serve(piano_class_doc, style='ent')

import cv2

image = cv2.imread('/Users/huhao/Downloads/WechatIMG54.jpeg')
print(image.shape)

