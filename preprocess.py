def preprocessing_txt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        first_line = lines[0].strip()


    # save partner name
    partner_name = None

    if first_line.endswith(" 님과 카카오톡 대화"):
        partner_name = first_line[: -len(" 님과 카카오톡 대화")].strip()

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_file)

    print(f'[PRE]Preprocessing complete! File saved as: {output_file}')

    return partner_name