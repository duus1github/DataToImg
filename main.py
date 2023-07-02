import os
import sys
import tkinter
from math import pi, sin, cos
from tkinter import Button, Tk, Label, filedialog, ttk
# from tkinter.ttk import LabelFrame
from tkinter.ttk import LabelFrame

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import gridspec
from matplotlib.font_manager import FontProperties
# todo:定义画图用到的一些参数
from matplotlib.ticker import MultipleLocator

dx, dy = 0.05, 0.05
x = np.arange(-3.0, 3.0, dx)
y = np.arange(-3.0, 3.0, dy)
extent = np.min(x), np.max(x), np.min(y), np.max(y)

matplotlib.rc("font", family='FangSong')


def cal_data(path, file_type):
    """
    计算表格数据
    :param path:
    :return:
    """
    pd_sheet1 = pd.read_excel(path)

    # TODO:计算饼状图结果
    pie_list = pd_sheet1[['所占训练百分比']].dropna(axis=0, how='any').values
    # TODO:获取能力图结果,柱状图,取每次训练的平均值
    """
    这里会不一样
        3-6：为 Runing	Jumping	Crawling	Agility	Coordination
        7-12：为 Locomotion	Movement perception	Coordination 	Agility	Stability
    """
    col_dict = {'3-6': ['Runing', 'Jumping', 'Crawling', 'Agility', 'Coordination'],
                '7-12': ['Locomotion', 'Movement perception', 'Coordination', 'Agility', 'Stability']}
    if file_type == '3-6':
        col_list = col_dict['3-6']
    else:
        col_list = col_dict['7-12']
    run, jump, climb, agi, coo = pd_sheet1[[col_list[0]]].dropna(axis=0, how='any').values, \
                                 pd_sheet1[[col_list[1]]].dropna(axis=0, how='any').values, \
                                 pd_sheet1[[col_list[2]]].dropna(axis=0, how='any').values, \
                                 pd_sheet1[[col_list[3]]].dropna(axis=0, how='any').values, \
                                 pd_sheet1[[col_list[4]]].dropna(axis=0, how='any').values
    ability = [run.mean(), jump.mean(), climb.mean(), agi.mean(), coo.mean()]
    # TODO:高效占比，
    inco = pd_sheet1[['未完成次数']].dropna(axis=0, how='any').values
    all = pd_sheet1[['训练次数']].dropna(axis=0, how='any').values

    effic_list = []
    for _index in zip(inco, all):
        effic_list.append((_index[1] - _index[0]) / _index[1])

    # 计算单个有效数据
    effic = 1 - (sum(inco) / sum(all))
    return pie_list, ability, effic_list, effic


def plot_pie(pie_list, ax):
    # TODO:绘制扇形图
    pie_label = '跑步模式训练', '跳跃模式训练', '爬动模式训练', '灵敏训练', '综合协调性训练'
    pie_data = [int(_i * 100) for _i in pie_list.transpose()[0]]
    label = []
    for i, v in enumerate(pie_data):
        pie_text = str(int(v)) + '%'
        label.append(pie_text)
    # 定义扇形图，返回标签位置和文字内容
    #todo:判断一下扇形图最大的值，<40:200  >40:220
    if (pie_data[0]<40):
        angle=200
    else:
        angle=220
    colors = ['navy', 'yellowgreen', 'salmon', 'dodgerblue', 'gold']
    wedges, texts = ax.pie(pie_data, startangle=angle, counterclock=False,colors=colors, textprops=dict(color="w"), radius=1.7)

    kw = dict(arrowprops=dict(arrowstyle="-", color='white', linewidth=1.8))
    print(pie_data)
    # todo:字体位置定义
    textx_list = [1.7, 1.8, 2, 2.1, 1.8]  # 1,
    texty_list = [1.35, 0.75, 0.1,-0.55, -1.3 ]
    ang_list = [20, 40, 40, 40, 30]  # 1,4,3,2
    # todo:线条起始位置定义
    x_list = [0.03, 1,0.91, 0, -0.7]
    y_list = [1.25, 0.5,  -0.2,-0.8, -1.25]
    for i, p in enumerate(wedges):
        # todo:定义标签的位置
        x = x_list[i]
        y = y_list[i]
        connectionstyle = "angle,angleA={},angleB=0".format(ang_list[i])
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        # text_x = 1.35 * x
        # text_y = 1.4 * y
        text_x = textx_list[i]
        text_y = texty_list[i]

        # ax.annotate(label[i], xy=(x, y), xytext=(text_x, text_y),  # xytext表示文字的终点位置
        #             horizontalalignment=horizontalalignment, **kw, fontsize=20)
        print('label:', label[i], ' ', x, y, ' ', text_x, text_y, ' ', ang_list[i])

        # ha =  {-1: "right", 1: "left"}[int(np.sign(x))]
        # ax.annotate(label[i], xy=(x, y), xytext=(text_x, text_y),  # xytext表示文字的终点位置
        #             arrowprops=dict(facecolor='mediumblue', shrink=0.05),horizontalalignment=horizontalalignment, **kw, fontsize=20)
        ax.annotate(label[i], xy=(x, y), xytext=(text_x, text_y),  # xytext表示文字的终点位置
                    fontsize=25, **kw, color='mediumblue')


def format_axes(*args):
    for ax in args[0]:
        ax.set_facecolor('none')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        # ax.text(0.5, 0.5, "%s" % (ax._children), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False, bottom=False, left=False)


def plot_effic(effic, ax):
    """
    绘制环状图
    :param effic:
    :param ax:
    :return:
    """
    int_effic = int(effic[0] * 100)
    effic_list = [int_effic, 100 - int_effic]

    wedgeprops = {'width': 0.3, 'edgecolor': 'gainsboro', 'linewidth': 1}
    colors = ['gold', 'gainsboro']
    ax.pie(effic_list, wedgeprops=wedgeprops, startangle=60, colors=colors, radius=1.7)
    ax.text(-1.27, -0.45, str(int_effic) + '%', fontsize=50, color='white', fontweight='bold', )


def plot_ability(ability, ax):
    """
    绘制横柱状图，横向展示每个模式的训练次数
    :param ability:数据%
    :param ax3:
    :return:
    """

    label = ('跑步模式训练', '跳跃模式训练', '爬动模式训练', '灵敏训练', '综合协调性训练')
    # colors = ['greenyellow', 'red', 'deepskyblue', 'gold', 'darkblue']
    colors = ['darkblue', 'gold', 'deepskyblue', 'red', 'greenyellow']

    y_pos = sorted(np.arange(len(label)),reverse=True)

    b = ax.barh(y_pos, ability, 0.4, color=colors, align="center")
    ax.set_xticks(range(0, 100, 10))
    i = 0
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, ' ' + '%d' % int(w), ha='left', va='center', color='white',
                fontsize=15)
        i += 1

    # ax.set_yticklabels(label)


def plot_text(ax1, ax2, ax3, text_list):
    """
    绘制标头学生的相关成绩图信息
    :param ax1:
    :param ax2:
    :return:
    """
    bbox = {'facecolor': 'indigo', 'alpha': 0.5, 'pad': 10}

    # ax1.text(0.1,0.2, r'an equation: $E=mc^2$', fontsize=15)
    ax1.text(0.1, 0.2, text_list[0], fontsize=25, horizontalalignment='left', color='white', fontweight='bold')
    ax2.text(0, 0, text_list[2].split('.')[0], fontsize=25, color='white', fontweight='bold')
    ax3.text(0.1, 0.2, text_list[1], fontsize=25, color='white', fontweight='bold')


def data_processing(in_path, out_path):
# def data_processing():
    # TODO:获取文件夹下的子文件
    dir_path = 'data'
    file_list = os.listdir(dir_path)
    for _file in file_list:
        file_path = os.path.join(dir_path, _file)
        text_list = _file.split('-')
        age = text_list[1]
        if int(age)<=6 and int(age)>=3:
            file_type='3-6'
        else:
            file_type='7-12'
        pie_list, ability, effic_list, effic = cal_data(file_path, file_type)

        """
        0-7：背景图为back0-7.jpg
        8-12:背景图为back8-12.jpg
        """
        if file_type == '3-6':
            photo_path = 'back0-7.jpg'
        else:
            photo_path = 'back8-12.jpg'
        # ====================
        # TODO:添加背景图片
        img = plt.imread(photo_path)
        fig = plt.figure(figsize=(10, 17))
        plt.rcParams['font.family'] = ['serif']
        # plt.rcParams['font.sans-serif'] = ['Times New Roman']
        plt.imshow(img)  # left=0,right=1,bottom=0,top=1,,
        plt.xticks([])
        plt.axis('off')
        gs0 = gridspec.GridSpec(1, 1, figure=fig)

        gs00 = gridspec.GridSpecFromSubplotSpec(1000, 2000, subplot_spec=gs0[0])
        ax1 = fig.add_subplot(gs00[243:263, 1230:1430])  # 放如学名字等文字name
        ax2 = fig.add_subplot(gs00[270:290, 1350:1400])  # 性别
        ax3 = fig.add_subplot(gs00[275:295, 1700:1850])  # 年龄
        ax4 = fig.add_subplot(gs00[360:600, 230:750])  # 放扇形图
        ax5 = fig.add_subplot(gs00[630:730, 150:650])  # 环状高效图
        ax6 = fig.add_subplot(gs00[640:740, 1245:1900])  # 横线柱状图

        # todo:绘制表头学生的姓名相关信息
        plot_text(ax1, ax2, ax3, text_list)
        # todo:训练模式的权重比例
        plot_pie(pie_list, ax4)

        # TODO:绘制训练高效图
        plot_effic(effic, ax5)

        # TODO:绘制学生能力图：
        plot_ability(ability, ax6)

        format_axes([ax1, ax2, ax3, ax4, ax5, ax6])

        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

        # plt.show()
        # todo:保存图片
        file_name = _file.split('.')[0]
        plt.savefig('{}.png'.format(out_path + '/' + file_name), dpi=600, bbox_inches='tight', pad_inches=0)
    sys.exit()


def control():
    in_path, out_path = get_path()
    data_processing(in_path, out_path)


def clicked_area():
    # file_path = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__))
    file_path = filedialog.askdirectory()

    entry1.set(file_path)
    return file_path


def clicked_trace():
    # file_path = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__))
    file_path = filedialog.askdirectory()
    entry2.set(file_path)
    return file_path


def get_path():
    res1 = entry1.get()
    res2 = entry2.get()
    # res3 = number.get()
    return res1, res2


window = Tk()
window.title("DGPSystem")

window.geometry("450x150")
lbl1 = Label(window, text="表格位置")
lbl1.grid(column=0, row=0)  # 用于确定hello的位置的
entry1 = tkinter.StringVar()
txt1 = tkinter.Entry(window, textvariable=entry1, width=30).grid(column=1, row=0)
btn1 = Button(window, text="选择文件", command=clicked_area).grid(column=2, row=0)
# todo:第二行的位置
lbl2 = Label(window, text="图片位置").grid(column=0, row=1)
entry2 = tkinter.StringVar()
txt2 = tkinter.Entry(window, textvariable=entry2, width=30).grid(column=1, row=1)
btn2 = Button(window, text="选择文件", command=clicked_trace).grid(column=2, row=1)

# TODO:下拉选项框
# Label(window, text="数据类型  ").grid(row=3, column=0)
# number = tkinter.StringVar()
# numberChosen = ttk.Combobox(window, width=27, textvariable=number)
# numberChosen['values'] = ("3-6", "7-12")  # 设置下拉列表的值
# numberChosen.grid(column=1, row=3)  # 设置其在界面中出现的位置 column代表列 row 代表行
# numberChosen.current(0)

# Label(window,text="数据类型  ").grid(row=3, column=0)
# E7 = tkinter.Spinbox(values=("0-7岁", "7-12岁"),width=28).grid(row=3, column=1)

btn4 = Button(window, text='开始分析', command=control, width=20).grid(row=4, columnspan=3)

window.mainloop()

if __name__ == '__main__':
    pass
    # data_processing()
