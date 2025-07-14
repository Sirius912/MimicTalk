import re
import json

def preprocessing_txt(input_txt):
    output_txt = 'preprocessed.txt'

    with open(input_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        first_line = lines[0].strip()

    # Save partner name
    partner_name = None

    if first_line.endswith(" 님과 카카오톡 대화"):
        partner_name = first_line[: -len(" 님과 카카오톡 대화")].strip()

    # Remove the first 3 lines (metadata, date)
    lines = lines[3:]

    # Define patterns to filter out time, date line, speaker
    time_pattern = re.compile(r'\[\s*\d{1,2}:\d{2}\s*(AM|PM)\s*\]\s')
    date_line_pattern = re.compile(r'^-+ .* -+$')
    speaker_pattern = re.compile(r'^\[[^\]]+\]')

    output_lines = []
    buffer = '' # Temporarily stores the current speaker's message

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Detect date line and store buffer to output_lines
        if date_line_pattern.match(line):
            if buffer:
                if not check_message(buffer): # True: detected special cases
                    output_lines.append(buffer)
                buffer = ''
            continue

        # Remove timestamp. [speacker] [time] message -> [speaker] message
        line = re.sub(time_pattern, '', line)

        if speaker_pattern.match(line):
            if buffer:
                if not check_message(buffer): # True: detected special cases
                    output_lines.append(buffer)
            buffer = line # Store current line to buffer
        else: # When the message is not finished, i.e., written across multiple lines using \n
            buffer += ' ' + line
        
    if buffer:
        if not check_message(buffer):
            output_lines.append(buffer)

    # Write the result to the output txt file
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print('-----[PREPROCESS]-----')
    print(f'Preprocessed txt file saved as: {output_txt}')

    convert_txt_to_json(output_txt)

    print('-----[PREPROCESS COMPLETE]-----\n')

    return partner_name, first_line, output_txt

def check_message(msg):
    # Extract message (excluding speaker)
    message = re.match(r'^\[[^\]]+\]\s*(.*)', msg)
    if not message:
        return False
    
    message = message.group(1).strip()

    # Remove messages such as photos, videos, and emojis
    if re.fullmatch(r'(사진|동영상|이모티콘)(\s*\d+장)?', message.strip()):
        return True

    # Define patterns to filter out remittance-related messages
    patterns = [
        re.compile(r'[\d,]+원을 보냈어요. 송금 받기 전까지 보낸 분은 내역 상세화면에서 취소할 수 있어요.'),
        re.compile(r'[\d,]+원을 받았어요. 받은 카카오페이머니는 송금 및 온/오프라인 결제도 가능해요.'),
        re.compile(r'[\d,]+원 자동환불 예정 내일 낮 12시에 자동 환불될 예정입니다. 송금 받기를 완료해 주세요.')
    ]

    for pattern in patterns:
        if pattern.fullmatch(message):
            return True

    # Remove file transfer messages
    if re.search(r'파일: ', message.strip()):
        return True

    return False

def convert_txt_to_json(output_txt):
    output_json = 'preprocessed.json'

    with open(output_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Initialize list to store all messages
    message_block = []

    # Pattern to match [sender] message
    message_pattern = re.compile(r'\[(.*?)\]\s*(.*)')

    for line in lines:
        line = line.strip()

        match = message_pattern.match(line)
        if match:
            sender = match.group(1)
            message = match.group(2)
            message_block.append({
                'sender': sender,
                'message': message
            })

    # Write the result to the output JSON file
    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(message_block, json_file, ensure_ascii=False, indent=4)

    print(f'Conversion complete! File saved as {output_json}')