import yaml
import chardet

my_file = 'file.yaml'

dict_to_yaml = {
    "MyList": ["one", "two"],
    "MyNumber": 99,
    "MyDict": {
        "Letter1": '\u14DF',
        "Letter2": '\u0488'
    }
}


def write_to_yaml(filename):
    with open(filename, 'w', encoding='utf-8') as f_n:
        yaml.dump(dict_to_yaml, f_n, default_flow_style=False, allow_unicode=True)


def read_yaml(filename):
    with open(filename, 'rb') as f_n:
        file_encoding = chardet.detect(f_n.read())["encoding"]
        print(file_encoding)
    with open(filename, 'r', encoding=file_encoding) as f_n:
        for line in f_n:
            print(line, end='')


if __name__ == '__main__':
    write_to_yaml(my_file)
    read_yaml(my_file)
