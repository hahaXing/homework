import jieba

# 打开文件
with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 使用jieba分词，将结果转化为列表类型
words = jieba.lcut(text)

# 定义一个空列表，用来存储去除标点符号后的分词结果
new_words = []

# 遍历分词列表，判断每个词是否为标点符号或特殊字符，如果不是则添加到新列表中
for word in words:
    if word.isalpha() or word.isdigit() or len(word) > 1:
        new_words.append(word)

# 将结果写入文件，并用空格隔开
with open('out.txt', 'w', encoding='utf-8') as f:
    f.write(' '.join(new_words))

#参数说明：
#1. `jieba.lcut()`：使用jieba对文本进行分词，返回一个列表类型的分词结果。
#2. `isalpha()`：判断字符串是否全部由字母组成。
#3. `isdigit()`：判断字符串是否全部由数字组成。
#4. `len(word) > 1`：判断字符串长度是否大于1，因为单个汉字或英文字母没有实际意义，所以需要去除。
#5. `join()`：将列表中的元素以指定字符（这里是空格）连接起来。


#以下是一个用Python绘制词云图代码，其中包含了详细的参数设置：

#python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# 读取文本数据
text = open('out.txt', 'r', encoding='utf-8').read()

# 设置停用词列表
stopwords = set(STOPWORDS)
stopwords.update(['有', '也', '到', '要', '了', '从'])

# 设置词云图参数
wc = WordCloud(background_color='white',
               stopwords=stopwords,
               max_words=1000,
               max_font_size=100,
               random_state=42,
               width=800,
               height=800,
               font_path="msyh.ttc",
               mask=None)

# 生成词云图
wc.generate(text)

# 设置颜色
image_colors = ImageColorGenerator(np.array(plt.imread('image_file.jpg')))

# 绘制图形
plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

#参数解释：
#- `text`: 传入的字符串，用于生成词云图。
#- `stopwords`: 停用词列表，用于过滤高频无意义的词语。
#- `background_color`: 设置词云图背景颜色，默认为`"black"`。
#- `max_words`: 设定词云图显示的最大单词数量，默认为`200`。
#- `max_font_size`: 设定词云图中单词的最大字号，默认为`100`。
#- `random_state`: 控制词云图的随机性，保证每次生成的词云图相同。
#- `width`和`height`: 设定词云图的宽度和高度。
#- `mask`: 用于定制输出形状的掩模图像。
#- `ImageColorGenerator`: 使用掩模图像的颜色来生成词云图。
#- `plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')`: 用于绘制词云图。
#- `plt.axis('off')`: 隐藏坐标轴。
#- `plt.tight_layout(pad=0)`: 设定输出图像的紧凑布局。