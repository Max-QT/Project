"""
作者：Max
日期：2021年08月11日
"""

import jieba  # 分词
from matplotlib import pyplot as plt  # 绘图，数据可视化，生成图片
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图像处理
import numpy as np  # 矩阵运算
import sqlite3  # 数据库

# 准备词云所需的文字
con = sqlite3.connect("PHOH.db")
cur = con.cursor()
sql = 'select abstract from PHOH_sale'
data = cur.execute(sql)
text = ''
for item in data:
    # print(item)
    if item[0] is not None:
        text = text + item[0]
cur.close()
con.close()

# 分词
cut = jieba.cut(text)
string = ' '.join(cut)
print(len(string))

# 生成遮罩图片
img = Image.open(r'football.jfif')
img_array = np.array(img)  # 将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path="STKAITI.TTF",  # 字体
    stopwords=["的", "和", '等', '于', '年', "是", "你", "了", "都", "最", "在", "不", "就是", "一个", "不会", "与", "让", "有", "被", "不是",
               "这样", "没有", "就"]
)
wc.generate_from_text(string)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')  # 是否显示坐标轴

# plt.show()  # 显示生成的词云图片
plt.savefig(r'WordCloud.jpg', dpi=500)  # 保存生成的词云图片， dpi:分辨率
