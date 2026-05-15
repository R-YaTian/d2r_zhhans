import os
import sys
import dictionary_lib as custom_dict_lib
sys.modules['opencc_purepy.dictionary_lib'] = custom_dict_lib
from opencc_purepy import OpenCC

# Initialize OpenCC converter (Traditional Chinese to Simplified Chinese)
converter = OpenCC('tw2sp')

def convert_zhTW_to_zhCN(src_dir, output_dir):
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Source directory '{src_dir}' not found.")
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(src_dir):
        folder_path = os.path.join(src_dir, filename)

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
            with open(os.path.join(output_dir, filename), 'w', encoding='utf-8-sig') as new_file:
                new_file.write('\n'.join(lines))

if __name__ == "__main__":
    # Convert zhTW to zhCN and save to output folder
    convert_zhTW_to_zhCN('Source', 'zhhans/zhhans.mpq/data/local/lng/strings')
    try:
        convert_zhTW_to_zhCN('Source-legacy', 'zhhans/zhhans.mpq/data/local/lng/strings-legacy')
    except FileNotFoundError:
        print("Source-legacy folder not found. Skipping conversion for legacy files.")
