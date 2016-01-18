#coding:utf-8
from hanziconv import HanziConv

stop_file = open("./other_data/stop_word.txt", 'r')
stop_word_array = []
for line in stop_file:
    temp = line.replace("\n", "")
    temp = HanziConv.toSimplified(temp)
    if temp not in stop_word_array:
        stop_word_array.append(temp)

stop_file1 = open("./generated_data/stop_word_final.txt", "w")
for i in stop_word_array:
    stop_file1.write(i.encode('utf8')+"\n")