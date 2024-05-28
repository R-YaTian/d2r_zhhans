import os

# output folder
output_folder = 'zhhans/zhhans.mpq/data/local/lng/strings'

# makedirs(if not exist)
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir('Source'):
    folder_path = os.path.join('Source', filename)

    if filename.endswith(".json"):
        # read original file
        with open(folder_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()

        # save lines to list
        lines = content.split('\n')

        line_index_tw = 0
        line_index_cn = 0
        zhTW_content = ''
        zhCN_content = ''

        for i, line in enumerate(lines):
            if '"zhTW":' in line:
                # Find "zhTW" key
                zhTW_index = line.find('"zhTW":') + len('"zhTW":')
                # Get "zhTW" content
                zhTW_content = line[zhTW_index:]
                line_index_tw = i

            if '"zhCN":' in line:
                # Find "zhCN" key
                zhCN_index = line.find('"zhCN":') + len('"zhCN":')
                # Get "zhCN" content
                zhCN_content = line[zhCN_index:]
                line_index_cn = i

            if line_index_tw != 0 and line_index_cn != 0:
                line_tmp = lines[line_index_tw]
                line_tmp = line_tmp.replace(zhTW_content, zhCN_content + ',')
                lines[line_index_tw] = line_tmp
                line_tmp = lines[line_index_cn]
                line_tmp = line_tmp.replace(zhCN_content, zhTW_content[:-1])
                lines[line_index_cn] = line_tmp
                line_index_tw = 0
                line_index_cn = 0
                zhTW_content = ''
                zhCN_content = ''

        # Write data to new JSON files
        with open(os.path.join(output_folder, filename), 'w', encoding='utf-8-sig') as new_file:
            new_file.write('\n'.join(lines))
