import os
import sys
import dictionary_lib as custom_dict_lib
sys.modules['opencc_purepy.dictionary_lib'] = custom_dict_lib

from opencc_purepy import OpenCC

# output folder
output_folder = 'zhhans/zhhans.mpq/data/local/lng/strings'

# makedirs(if not exist)
os.makedirs(output_folder, exist_ok=True)

# Initialize OpenCC converter (Traditional Chinese to Simplified Chinese)
converter = OpenCC('tw2sp')

for filename in os.listdir('Source'):
    folder_path = os.path.join('Source', filename)

    if filename.endswith(".json"):
        # read original file
        with open(folder_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()

        # save lines to list
        lines = content.split('\n')

        for i, line in enumerate(lines):
            if '"zhTW":' in line:
                # Find "zhTW" key
                zhTW_index = line.find('"zhTW":') + len('"zhTW":')
                # Get "zhTW" content and convert using OpenCC
                zhTW_content = line[zhTW_index:]
                # Convert traditional Chinese to simplified Chinese
                zhCN_content = converter.convert(zhTW_content[:-1])
                # Replace zhTW content with converted text
                line_tmp = line[:zhTW_index]
                line_tmp += zhCN_content + zhTW_content[-1]
                lines[i] = line_tmp

        # Write data to new JSON files
        with open(os.path.join(output_folder, filename), 'w', encoding='utf-8-sig') as new_file:
            new_file.write('\n'.join(lines))
