import io
import random
import sys
import tkinter
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import requests
import sv_ttk
import re
import urllib.request,urllib.error
import bs4
import os
import json
import urllib.parse
from fake_useragent import UserAgent
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import unittest

cookie = {
    'login_referer': 'https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000',
    '_uid': '111884',
    '__client_id': '4f1bbbf98da6e49a6c98727320089c851c18d53c',
    'C3VK': 'aa6e71',
}


data=[]
baseUrl = "https://www.luogu.com.cn/problem/"
BaseUrl = "https://www.luogu.com.cn/problem/list?"
baseUrlSolution = "https://www.luogu.com.cn/problem/solution/"
savePath = r"C:\Users\86135\Desktop\Homework-main\\"

#单元测试
def sub(a,b):
    return a-b
class TestSubFunction(unittest.TestCase):
    def test_sub(self):
        result=sub(7,1)
        self.assertEqual(result,6)
def get_tm_MD(html):
    bs = bs4.BeautifulSoup(html,"html.parser")
    core = bs.select("article")[0]
    md = str(core)
    th=""
    pattern1 = re.compile(r'<h1>.*?</h1>')
    matches = re.findall(pattern1, md)
    th=matches[0]
    th = re.sub("<h1>", "",th)
    th = re.sub("</h1>", "", th)
    md = re.sub("<h1>","# ",md)
    md = re.sub("<h2>","## ",md)
    md = re.sub("<h3>","#### ",md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>","",md)
    return md,th
def get_tj_MD(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    encoded_content_element = soup.find('script')
    encoded_content = encoded_content_element.text
    start = encoded_content.find('"')
    end = encoded_content.find('"', start + 1)
    encoded_content = encoded_content[start + 1:end]
    decoded_content = urllib.parse.unquote(encoded_content)
    decoded_content = decoded_content.replace('\/', '/')
    decoded_content = decoded_content.encode('utf-8').decode('unicode_escape')
    start = decoded_content.find('"content":"')
    end = decoded_content.find('","type":"题解"')
    decoded_content = decoded_content[start + 11:end]
    return decoded_content
def save_tm_Data(data,filename):
  file = open(filename,"w",encoding="utf-8")
  for d in data:
    file.writelines(d)
  file.close()
class Button(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame", padding=15)
        self.columnconfigure(0, weight=1)
        self.add_widgets()
    def add_widgets(self):
        self.entry = ttk.Entry(self)
        combo_list = ["关键词","字符串", "动态规划", "搜索", "数学", "图论", "计算几何", "树形数据结构", "博弈论", "多项式", "数论", "启发式搜索", "哈希"]
        self.combobox = ttk.Combobox(self, values=combo_list)
        self.combobox.current(0)
        self.combobox.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        combo_list1 = ["选择难度", "暂未评定", "入门", "普及-", "普及/提高-", "普及+/提高", "提高+/省选-", "省选/NOI-", "NOI/NOI+/CTSC"]
        self.combobox1 = ttk.Combobox(self, values=combo_list1)
        self.combobox1.current(0)
        self.combobox1.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('number of title')
        self.ax.set_ylabel('Crawl progress')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=9, column=0)
        self.separator = ttk.Separator(self)
        self.separator.grid(row=5, column=0, pady=10, sticky="ew")
        self.button = ttk.Button(self, text="点击")
        self.button.grid(row=6, column=0, padx=5, pady=10, sticky="ew")
        self.title_text = tkinter.StringVar()
        self.title_label = ttk.Label(self, textvariable=self.title_text)
        self.title_label.grid(row=7, column=0, padx=5, pady=(10, 0), sticky="w")
        self.progressbar = ttk.Progressbar(self, length=200)
        self.progressbar.grid(row=8, column=0, pady=10)
        def click():
            global kw, difficulty
            kw = self.combobox.get()
            difficulty1 = self.combobox1.get()
            global savePath
            savePath = str(difficulty1) + '-' + kw
            if not os.path.exists(savePath):
                os.mkdir(savePath)
            for i in range(len(combo_list1)):
                if combo_list1[i] == difficulty1:
                    difficulty = i - 1
            Td = BaseUrl + "&difficultyy=" + str(difficulty) + "&keyword=" + str(kw)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            resp = requests.get(Td, headers=headers)
            pattern = re.compile(r'(<a\shref=".*?">)*?')
            pattern = re.findall(pattern, resp.text)
            tm = []
            for x in pattern:
                if (x != ""):
                    tm.append(x[9:14])
            count = 0
            progress = range(1, count + 1)
            for i in range(len(tm)):
                count += 1
                if (count > 20):#先爬取20题
                    break
                title = "正在爬取第{}题,题目编号为".format(i + 1)+tm[i]
                self.title_text.set(title)
                self.title_label.update()
                self.update()
                print("正在爬取第{}题\n".format(i), end="")
                self.title_label.configure(text="正在爬取第{}题,题目编号为".format(i)+tm[i])
                self.title_label.update()
                url = baseUrl + tm[i]
                r = requests.get(url, headers=headers, cookies=cookie)
                htmltm = r.text
                url = baseUrlSolution + tm[i]
                r = requests.get(url, headers=headers, cookies=cookie)
                htmlso = r.text
                if htmltm == "error":
                    print("爬取失败，可能是不存在该题或无权查看")
                else:
                    problemMD, th = get_tm_MD(htmltm)
                    solutionMD = get_tj_MD(htmlso)
                    print("爬取成功！正在保存\n", end="")
                    self.ax.plot(progress[:i + 1], progress[:i + 1], 'b-')
                    self.ax.set_xlim([1, count + 1])
                    self.ax.set_ylim([0, count + 1])
                    self.canvas.draw()
                    self.ax.relim()
                    self.ax.autoscale_view()
                    self.title_label.configure(text="正在爬取第{}题,题目编号为".format(i + 1)+tm[i])
                    self.title_label.update()
                    cleaned_m = re.sub(r'[\\/:*?"<>|\[\]]', '-', tm[i])
                    cleaned_th = re.sub(r'[\\/:*?"<>|\[\]]', '-', th)
                    folder_path = os.path.join(savePath, f"{cleaned_m}-{cleaned_th}")
                    if not os.path.exists(folder_path):
                        os.mkdir(folder_path)
                    problem_file_path = os.path.join(folder_path, f"{tm[i]} {th}.md")
                    solution_file_path = os.path.join(folder_path, f"{tm[i]} {th}-题解.md")
                    save_tm_Data(problemMD, problem_file_path)
                    save_tm_Data(solutionMD, solution_file_path)
                    global data
                    data.append(tm[i] + " " + th)
                    print("保存成功!\n")
            self.title_text.set("爬取完毕")  # 更新标题的显示文本
        self.button.config(command=click)
class app(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        Button(self).grid(
            row=0, column=1, rowspan=2, padx=10, pady=(10, 0), sticky="nsew"
        )
def main():
    root = tkinter.Tk()
    root.title("CrawlerGUI")
    sv_ttk.set_theme("dark")
    app(root).pack(expand=True)
    root.mainloop()
if __name__ == "__main__":
    kw=""
    time=0
    difficulty=0
    al=0
    main()
    #unittest.main()  #进行单元测试