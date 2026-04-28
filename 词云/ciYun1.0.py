#以下是使用tkinter库编写的Python程序，实现了所需功能：

#python
import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import codecs

class CloudWordsApp:
    global banned_text
    global keywords_text
    def __init__(self, master):
        self.master = master
        master.title("星云词1.0")
        master.geometry("800x500")
        master.configure(background='skyblue')

        self.import_excel_button = tk.Button(master, text="导入表格(Excel表格)", command=self.import_excel_text)
        self.import_excel_button.pack(pady=20)

        self.import_data_button = tk.Button(master, text="导入数据文本(txt文本)", command=self.import_data_text)
        self.import_data_button.pack(pady=20)

        self.import_banned_words_button = tk.Button(master, text="导入禁用词(被禁用词语将不与显示，格式为txt文本)", command=self.import_banned_words)
        self.import_banned_words_button.pack(pady=20)

        self.import_keywords_button = tk.Button(master, text="导入重点词(增加指定词语20%权重，格式为txt文本)", command=self.import_keywords)
        self.import_keywords_button.pack(pady=20)

        self.import_image_button = tk.Button(master, text="导入图片（默认白色部分为底色，其他颜色按比例影响文字）", command=self.Set_Images)
        self.import_image_button.pack(pady=20)

        self.import_show_button = tk.Button(master, text="显示云图", command=self.Cloud_Display, bg="darkgreen")
        self.import_show_button.pack(pady=20)

    def import_excel_text(self):
        file_path = filedialog.askopenfilename()
        data = pd.read_excel(file_path, sheet_name=None)
        all_data = pd.concat(data.values())
        all_data.to_csv('excel_out.txt', sep='\t', index=False)
        text = open('excel_out.txt', 'r', encoding='utf-8').read()
        self.data_clearn(text)

    def import_data_text(self):
        file_path = filedialog.askopenfilename()
        try:
            with codecs.open(file_path, 'r', encoding='utf-8') as f:
                data_text = f.read()
        except UnicodeDecodeError:
            print('编码格式不是utf-8')

        #with open(file_path, 'r', encoding='utf-8') as f:

        self.data_clearn(data_text)

    def data_clearn(self, data_text):
        pattern = re.compile(r'[^\u4e00-\u9fa5]')  # 匹配非中文字符
        new_data_text = pattern.sub('', data_text)
        words = jieba.lcut(new_data_text)
        new_words = []
        for word in words:
            if word.isalpha() or word.isdigit() or len(word) > 1:
                new_words.append(word)

        with open('out.txt', 'w', encoding='utf-8') as f:
            f.write(' '.join(new_words))
        messagebox.showinfo(title="提示", message="文件导入成功！")

    def import_banned_words(self):
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r', encoding='utf-8') as f:
            banned_text = f.read()

    def import_keywords(self):
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r', encoding='utf-8') as f:
            keywords_text = f.read()
    def Set_Images(self):
        global image_path
        image_path = filedialog.askopenfilename()
        if image_path == "":
            messagebox.showinfo(title="提示", message="图片导入失败！")
        else:
            messagebox.showinfo(title="提示", message="图片导入成功！")

    def Cloud_Display(self):
        text = open('out.txt', 'r', encoding='utf-8').read()

        stopwords = set(STOPWORDS)
        stopwords.update(['我', '你', '他', '她', '有', '也', '到', '要', '了', '从'])

        wc = WordCloud(background_color='white',
                       stopwords=stopwords,
                       max_words=1000,
                       max_font_size=100,
                       random_state=42,
                       width=800,
                       height=800,
                       font_path="msyh.ttc",
                       mask=None)

        wc.generate(text)
        global image_path
        image_colors = ImageColorGenerator(np.array(plt.imread(image_path)))
        plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.show()


root = tk.Tk()
app = CloudWordsApp(root)
root.mainloop()

#在这个程序中，我们定义了一个名为
#`CloudWordsApp`
#的类来管理应用程序。在类的构造函数中，我们实例化了三个按钮，并将它们绑定到对应的方法上。

#每个按钮的方法都使用
#`filedialog`
#模块中的
#`askopenfilename()`
#方法来打开文件选择器让用户选择需要导入的文件。

#在每个方法中，我们需要编写导入文件的代码。在这里为了简化问题，我们暂时省略了这部分代码。实际应用中，可以根据文件类型使用不同的方式来读取文件内容。