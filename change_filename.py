import os

def change_filename(original_filepath):
    # get file name from path
    original_file = os.path.basename(original_filepath)

    # split from the right at the last underscore
    parts = original_file.rsplit('_', 1)

    if len(parts) == 2:
        new_file = parts[1]
    else:
        new_file = original_file

    # rename the file
    folder_path = os.path.dirname(original_filepath)
    new_filepath = os.path.join(folder_path, new_file)
    os.rename(original_filepath, new_filepath)

    print(f"[RENAME]File renamed from '{original_file}' to '{new_file}'")

    return original_file, new_file, new_filepath
