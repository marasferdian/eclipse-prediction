
import csv
in_file = open('C:/Users/Mara Sferdian/Downloads/moon-passage-v2.txt', 'r')
out_file = open('C:/Users/Mara Sferdian/Downloads/moon-passage-v2.csv', 'w', newline='')
lines = in_file.readlines()
writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
fieldnames = lines[0].strip().split()
writer.writerow(fieldnames)
for line in lines:
    stripped_line = line.strip()
    splitted_line = stripped_line.split()
    # if len(splitted_line) != len(fieldnames):
    #     print(splitted_line)
    #     dateTimeAsc = splitted_line[0] + " " + splitted_line[1]
    #     line = []
    #     line.append(dateTime)
    #     length = splitted_line[2] + " " + splitted_line[3] + " " + splitted_line[4]
    #     line.append(length)
    #     distanceFromMean = splitted_line[5] + splitted_line[6]
    #     line.append(distanceFromMean)
    #     line.append(splitted_line[7])
    #     writer.writerow(line)
    # else:
    #     writer.writerow(splitted_line)
    if len(splitted_line) == 4:
        dateTimeAsc = splitted_line[0] + " " + splitted_line[1]
        dateTimeDesc = splitted_line[2] + " " +splitted_line[3]
        line = []
        line.append(dateTimeAsc)
        line.append(dateTimeDesc)
        writer.writerow(line)
out_file.close()
