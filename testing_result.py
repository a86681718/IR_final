import csv
import jieba
from hanziconv import HanziConv

so_file = open("./generated_data/semantic_orientation.txt", "r")
semantic_orientation = {}
for word in so_file:
    temp = (word.replace("\n", "")).split(", ")
    semantic_orientation[temp[0]] = temp[1]

reader = csv.reader(open("./generated_data/testing_file.csv", "rb"))
true_postive = 0
false_positive = 0
true_negative = 0
false_negative = 0
for row in reader:
    temp = HanziConv.toSimplified(row[3])
    words = jieba.cut(temp, cut_all=False)
    score = 0.0
    for w in words:
        word = w.encode('utf8')
        if word in semantic_orientation:
            score += float(semantic_orientation[word])
    if score >= 0 and row[1] == '1':
        true_postive += 1
    elif score >= 0 and row[1] == '0':
        false_positive += 1
    elif score < 0 and row[1] == '0':
        true_negative += 1
    elif score < 0 and row[1] == '1':
        false_negative += 1

print true_postive, false_positive
print false_negative, true_negative
print "Accuracy: %f" % (float(true_postive + true_negative)/float(true_postive + true_negative + false_positive + false_negative))
print "Precision: %f" % (float(true_postive)/float(true_postive + false_positive))
print "Recall: %f" % (float(true_postive)/float(true_postive + false_negative))
