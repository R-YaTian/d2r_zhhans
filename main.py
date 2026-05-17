import os
import shutil
import argparse

_converter = None

def get_converter():
    global _converter
    if _converter is None:
        try:
            from opencc_purepy import OpenCC
        except ImportError as exc:
            raise ImportError(
                "opencc_purepy is required when use_swap=False. "
                "Install it with: pip install opencc-purepy"
            ) from exc

        # Initialize OpenCC converter (Traditional Chinese to Simplified Chinese)
        _converter = OpenCC.from_dicts(
            config="tw2sp",
            overrides={
                "tw_phrases_rev": "./dicts/TWPhrasesRev.txt",
            },
        )
    return _converter

def convert_zhTW_to_zhCN(src_dir, output_dir, use_swap=False):
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Source directory '{src_dir}' not found.")
    os.makedirs(output_dir, exist_ok=True)

    converter = None
    if not use_swap:
        converter = get_converter()

    for filename in os.listdir(src_dir):
        folder_path = os.path.join(src_dir, filename)

        if filename.endswith(".json"):
            # read original file
            with open(folder_path, 'r', encoding='utf-8-sig') as file:
                content = file.read()

            # save lines to list
            lines = content.split('\n')
            line_index_tw = 0
            line_index_cn = 0

            for i, line in enumerate(lines):
                if use_swap:
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
                else:
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--swap", action="store_true", help="Swap zhTW and zhCN values")
    args = parser.parse_args()

    # Remove existing output data directory before generating new files
    data_dir = 'zhhans/zhhans.mpq/data/local'
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
        print(f"Removed existing data directory: {data_dir}")

    output_dir_str = 'zhhans/zhhans.mpq/data/local/lng/strings'
    if args.swap:
        # Swap mode: only process string files and exit early.
        convert_zhTW_to_zhCN('Source', output_dir_str, use_swap=True)
        return

    output_dir_legacy = 'zhhans/zhhans.mpq/data/local/lng/strings-legacy'
    # Convert zhTW to zhCN and save to output folder
    convert_zhTW_to_zhCN('Source', output_dir_str)
    try:
        convert_zhTW_to_zhCN('Source-legacy', output_dir_legacy)
        # Extract font_chi.7z to the target directory
        import py7zr
        font_archive = 'font_chi.7z'
        extract_dir = 'zhhans/zhhans.mpq/data/local/font/chi'
        if os.path.exists(font_archive):
            os.makedirs(extract_dir, exist_ok=True)
            with py7zr.SevenZipFile(font_archive, mode='r') as z:
                z.extractall(path=extract_dir)
            print(f"Extracted {font_archive} to {extract_dir}")
        else:
            print(f"{font_archive} not found. Skipping font extraction.")
            if os.path.exists(output_dir_legacy):
                shutil.rmtree(output_dir_legacy)
    except FileNotFoundError:
        print("Source-legacy folder not found. Skipping conversion for legacy files.")
    except ImportError:
        print("py7zr module not found. Please install it to extract font files.")

if __name__ == "__main__":
    main()
