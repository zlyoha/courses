import csv
import fnmatch
import os
import re

import chardet

listOfFiles = os.listdir('.')
pattern = "info_*.txt"
main_data = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]


def getdata():
    os_prod_re = re.compile(r'^Изготовитель системы:\s*(.*)')
    os_name_re = re.compile('^Название ОС:\s*(.*)')
    os_code_re = re.compile('^Код продукта:\s*(.*)')
    os_type_re = re.compile('^Тип системы:\s*(.*)')

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    for filename in listOfFiles:
        if fnmatch.fnmatch(filename, pattern):
            print(filename)
            with open(filename, mode='rb') as file:
                file_encoding = chardet.detect(file.read())['encoding']
            with open(filename, mode='r', encoding=file_encoding) as file:
                for line in file:
                    if re.match(os_prod_re, line):
                        os_prod_list.append(re.match(os_prod_re, line).group(1))
                    elif re.match(os_name_re, line):
                        os_name_list.append(re.match(os_name_re, line).group(1))
                    elif re.match(os_code_re, line):
                        os_code_list.append(re.match(os_code_re, line).group(1))
                    elif re.match(os_type_re, line):
                        os_type_list.append(re.match(os_type_re, line).group(1))

    return os_prod_list, os_name_list, os_code_list, os_type_list


def write_to_csv(filename):
    os_prod_list, os_name_list, os_code_list, os_type_list = getdata()
    print(os_prod_list, os_name_list, os_code_list, os_type_list)
    with open(filename, mode='w') as file:
        file_writer = csv.DictWriter(file, delimiter=';', fieldnames=main_data)
        file_writer.writeheader()
        for i in range(len(os_prod_list)):
            row = dict(zip(main_data, [os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]]))
            print(row)
            file_writer.writerow(row)


if __name__ == '__main__':
    write_to_csv('result.csv')
