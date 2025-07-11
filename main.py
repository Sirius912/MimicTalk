import argparse
from preprocess import preprocessing_txt
from text_generation import text_generation

parser = argparse.ArgumentParser()
parser.add_argument('input_txt', type=str, help="File name to read")
args = parser.parse_args()
input_txt = args.input_txt

try:
    with open(input_txt, 'r', encoding='utf-8') as f:
        # Preprocess input file
        partner_name, title = preprocessing_txt(input_txt)

        question = 'Type your question'
        print('Question:', question)
        
        text_generation(input_txt, partner_name, question)

except FileNotFoundError:
    print(f'[ERROR] {input_txt} not found.')