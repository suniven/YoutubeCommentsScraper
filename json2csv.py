import os
import json
from io import StringIO

import pandas as pd

if __name__ == '__main__':
    df = pd.read_json(StringIO(data_json_str))
    df.to_csv('../csv/1989660417_comments.csv', index=False)
