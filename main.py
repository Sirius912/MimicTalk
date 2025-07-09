import os
from change_filename import change_filename
from preprocess import preprocessing_txt

# in the case of loading a KakaoTalk txt file and using it unchanged
original_path = r'C:\Users\kangj\MimicTalk\KakaoTalk_20250709_1356_12_268_prof.txt'

original_file, input_file, input_path = change_filename(original_path)

partner_name = preprocessing_txt(input_file, 'partner_name.txt')

