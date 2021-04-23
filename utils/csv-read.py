import csv
with open('C:/Users/Mara Sferdian/Downloads/lunar-1900+timeanddate.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(row)
            line_count += 1
    print(f'Processed {line_count} lines.')
