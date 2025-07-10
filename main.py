import os
import argparse
from preprocess import preprocessing_txt

parser = argparse.ArgumentParser()
parser.add_argument('input_txt', type=str, help="File name to read")
args = parser.parse_args()
input_txt = args.input_txt

try:
    with open(input_txt, 'r', encoding='utf-8') as f:
        # Preprocess input file
        partner_name, title = preprocessing_txt(input_txt)

        print(title, '생성')

except FileNotFoundError:
    print(f'{input_txt} not found.')

