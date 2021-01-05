import csv
in_file = open('C:/Users/Mara Sferdian/Downloads/solar-1900+timeanddate.txt', 'r')
out_file = open('C:/Users/Mara Sferdian/Downloads/solar-1900+timeanddate.csv', 'w', newline='')

lines = in_file.readlines()
eclipses_dict = {}
writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
for line in lines:
    stripped_line = line.strip().replace('[','').replace(']','').replace("'",'')
    splitted_line = stripped_line.split(",")
    if splitted_line[2] in eclipses_dict.keys():
        eclipses_dict[splitted_line[2]].append(splitted_line[0])
    else:
        eclipses_dict[splitted_line[2]] = [splitted_line[0]]

regions = ['africa', 'asia', 'antarctica','atlantic','arctic', 'australia', 'europe', 'indian-ocean','north-america','pacific', 'south-america']
regions.insert(0,'Date')
writer.writerow(regions)
for key in eclipses_dict:
    row = [key.replace(' ','')]
    for i in range(1, len(regions)):
        if regions[i] in eclipses_dict[key]:
            row.append('true')
        else:
            row.append('false')
    writer.writerow(row)
out_file.close()
