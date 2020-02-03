import csv
import arrow 


def read_csv():
    with open('raw_data/raw_10.csv', 'rU') as csv_file:
        csv.field_size_limit(1131072)
        spamreader = csv.reader((line.replace('\0','') for line in csv_file), delimiter=",", dialect=csv.excel_tab)
        # spamreader = csv.reader(csv_file)
        new_line = []
        aaa = 1
        for row in spamreader:
            print(aaa)
            l_index = len(new_line)

            if len(row) == 0:
                continue

            if l_index == 0:
                new_line = new_line + row
            elif 8 > l_index > 0:
                new_line[l_index-1] = new_line[l_index-1] + row[0]
                new_line = new_line + row[1:]

            if len(new_line) > 8:
                for var in new_line[3:]:
                    try:
                        arrow.get(var)
                        break
                    except:
                        new_line[2] = new_line[2] + new_line[3]
                        new_line.pop(3)

            if len(new_line) > 8:
                for var in new_line[8:]:
                        new_line[7] = new_line[7] + new_line[8]
                        new_line.pop(8)
                            
            if len(new_line) == 8:
                aaa += 1
                if aaa > 2756140:
                    print(new_line)
                new_line = []


            if len(new_line) > 8:
                # print(new_line)
                raise ValueError('this logix is not work')
  

        # print(aaa)
# hashlib.md5(open('src/raw_data/raw_10a.csv', 'rb').read()).hexdigest()

# read_csv()