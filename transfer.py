import csv

with open('example.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        with open(f'row_{i}.txt', 'w', encoding='utf-8') as txtfile:
            txtfile.write(','.join(row))