import argparse
from preprocess import preprocessing_txt

parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=str, help="File name to read")
args = parser.parse_args()
input_file = args.input_file

try:
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print(f'{input_file} not found.')

partner_name = preprocessing_txt(input_file, 'partner_name.txt')