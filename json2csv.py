import os
import json
from io import StringIO
import pandas as pd
import csv
from datetime import datetime

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 50)
csv.field_size_limit(500 * 1024 * 1024)


def find_all_files(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith(".json"):
                fullname = os.path.join(root, f)
                yield fullname


def main():
    new_df = pd.DataFrame()
    json_file_path = './output/'
    output_path = './csv/comments_' + str(datetime.timestamp(datetime.now())) + ".feather"
    for json_file in find_all_files(json_file_path):
        print(json_file)
        with open(json_file, 'r', encoding='utf-8') as json_file:
            data_json_str = json_file.read()
        df = pd.read_json(StringIO(data_json_str))
        new_df = pd.concat([df, new_df], ignore_index=True)

    new_df.to_feather(output_path)


if __name__ == '__main__':
    main()
