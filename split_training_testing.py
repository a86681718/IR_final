import csv
from random import randint

file_name = ['2015-12-30', '2015-12-31', '2016-01-02', '2016-01-03', '2016-01-04', '2016-01-05']
writer = csv.writer(open("./generated_data/concatenate_file.csv", "w"))
writer1 = csv.writer(open("./generated_data/training_file.csv", "w"))
writer2 = csv.writer(open("./generated_data/testing_file.csv", "w"))

training = []
for i in range(0, 2387):
    random = randint(1, 3562)
    while random in training:
        random = randint(1, 3562)
    training.append(random)

count = 0
index = 1
for name in file_name:
    reader = csv.reader(open("./news_data/%s_train.csv" % name, "rb"))
    for row in reader:
        writer.writerow(row)
        if row[1] == '2':
            count += 1
        else:
            if index in training:
                writer1.writerow(row)
            else:
                writer2.writerow(row)
            index += 1
print count
