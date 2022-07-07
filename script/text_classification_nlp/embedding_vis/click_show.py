"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/6/30 7:49 PM
"""
import numpy as np
import matplotlib.pyplot as plt


def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    points = tuple(zip(xdata[ind], ydata[ind]))
    print('the point of the sentence', x_to_sentence[xdata[ind][0]])

def get_pos():
    """得到点位置信息"""
    with open('inf.txt','r') as fp:
        contents = fp.readlines()
    pos = []
    x_to_sentence = {}
    for sample in contents:
        x = float(sample.split()[0])
        y = float(sample.split()[1])
        pos.append([x,y])
        sentence_str = ''
        for sample in  sample.split()[2:]:
            sentence_str +=' '+sample
        x_to_sentence[x] = sentence_str

    return pos,x_to_sentence


def show_pic(pos,x_to_sentence):
    fig, ax = plt.subplots()
    ax.set_title('click and show sentence')
    for i in range(len(pos)):
        line, = ax.plot(pos[i][0], pos[i][1], 'o',
                        picker=True, pickradius=5)  # 5 points tolerance
    fig.canvas.mpl_connect('pick_event', onpick)
    plt.show()



if __name__ == '__main__':
    # fig.canvas.mpl_connect('pick_event', onpick)
    # plt.show()
    pos,x_to_sentence = get_pos()
    show_pic(pos, x_to_sentence)
