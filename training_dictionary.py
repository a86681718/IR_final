#coding:utf-8
import jieba
import csv
import re
import math
from collections import OrderedDict
from hanziconv import HanziConv


def only_nonascii(text):
    return _ascii_letters.sub("", text)


_ascii_letters = re.compile(r'[0-9a-zA-Z]', flags=re.UNICODE)
punctuation = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '{', '}', '|', ':', ';', "'", '"',
            '<', '>', '-', '=', '[', ']', '\\', ',', '.', '/', '?', '！', '＠', '＃', '＄', '％', '＾', '＆',
            '＊', '（', '）', '＿', '＋', '『', '』', '｜', '：', '；', '“', '，', '。', '？', '＝', '「',  '」',
            '、', '《', '》', '／', '【', '】', '●', '★', '．', '‧', " "]

# Read in the stopword
stop_words = open("./generated_data/stop_word_final.txt", "r")
stop_word_list = []
for word in stop_words:
    stop_word_list.append(word.replace("\n", ""))


dic_postive ={}
dic_negative = {}
dic_term_orientation = {}
pos = 0.0
neg = 0.0
oth = 0.0
reader = csv.reader(open("./generated_data/training_file.csv", "rb"))
for row in reader:
    if row[1] == "1":
        pos += 1
    elif row[1] == "0":
        neg += 1
    elif row[1] == "2":
        oth += 1
    flag = row[1]
    temp = HanziConv.toSimplified(row[3])
    words = jieba.cut(temp, cut_all=False)
    word_is_counted = []
    for w in words:
        if w not in word_is_counted:
            word = w.encode('utf8')
            if (word not in punctuation and word not in stop_word_list) and only_nonascii(word) != "":
                if flag == '1':
                    if word not in dic_postive:
                        dic_postive[word] = 2
                    else:
                        dic_postive[word] += 1
                    if word not in dic_negative:
                        dic_negative[word] = 1
                elif flag == '0':
                    if word not in dic_negative:
                        dic_negative[word] = 2
                    else:
                        dic_negative[word] += 1
                    if word not in dic_postive:
                        dic_postive[word] = 1
            word_is_counted.append(w)


dic_negative = OrderedDict(sorted(dic_negative.items(), key=lambda t: t[1]))
dic_postive = OrderedDict(sorted(dic_postive.items(), key=lambda t: t[1]))

for i in dic_negative:
    dic_term_orientation[i] = math.log(float(dic_postive[i])/float(pos)/(float(dic_negative[i])/float(neg)))

semantic_file = open("./generated_data/semantic_orientation.txt", "w")
dic_term_orientation = OrderedDict(sorted(dic_term_orientation.items(), key=lambda t: t[1]))
for i in dic_term_orientation:
    semantic_file.write("%s, %f\n" % (i, dic_term_orientation[i]))
