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

    # Regex pattern to remove time
    time_pattern = re.compile(r'\[\s*\d{1,2}:\d{2}\s*(AM|PM)\s*\]\s')
    date_line_pattern = re.compile(r'^-+ .* -+$')
    speaker_pattern = re.compile(r'^\[[^\]]+\]')

    output_lines = []
    buffer = ''

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if date_line_pattern.match(stripped):
            if buffer:
                output_lines.append(buffer)
                buffer = ''
            output_lines.append(stripped)
            continue

        # Remove timestamp
        without_time = re.sub(time_pattern, '', stripped)

        if speaker_pattern.match(without_time):
            # New conversation started
            if buffer:
                output_lines.append(buffer)
            buffer = without_time
        else:
            buffer += ' ' + without_time

    if buffer:
        output_lines.append(buffer)
        
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print('-----[PREPROCESS]-----')
    print(f'Preprocessed txt file saved as: {output_txt}')

    convert_txt_to_json(output_txt)

    print('-----[PREPROCESS COMPLETE]-----\n')

    return partner_name, first_line

def convert_txt_to_json(output_txt):
    output_json = 'preprocessed.json'

    with open(output_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Initialize variables
    chat_blocks = []
    current_block = None
    message_block = []

    # Regex pattern to detect the data separators
    date_pattern = re.compile(r'^---------------\s*(.*?)\s*---------------$')

    # Use re.DOTALL to allow '.' to match newline characters
    message_pattern = re.compile(r'\[(.*?)\]\s*(.*)', re.DOTALL)

    for line in lines:
        line = line.strip()

        # Match date separator
        date_match = date_pattern.match(line)

        if date_match:
            # Save the current block before starting a new line
            if current_block:
                current_block['messages'] = message_block
                chat_blocks.append(current_block)

            # Start a new block for the new date
            current_block = {'date': date_match.group(1), 'messages': []}
            message_block = []  # reset message block
        elif line:
            # Match messages in the format [sender] [time] message
            message_match = message_pattern.match(line)

            if message_match:
                sender = message_match.group(1)
                message = message_match.group(2).strip()
                message_block.append({'sender': sender, 'message': message})
    
    if current_block:
        current_block['messages'] = message_block
        chat_blocks.append(current_block)

    # Write the result to the output JSON file
    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(chat_blocks, json_file, ensure_ascii=False, indent=4)

    print(f'Conversion complete! File saved as {output_json}')