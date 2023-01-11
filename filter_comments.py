import pandas as pd
import os
from tqdm import tqdm


def find_all_files(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith(".feather"):
                fullname = os.path.join(root, f)
                yield fullname, f


def main():
    video_count = 0
    comment_count = 0
    for file, filename in find_all_files('./csv/'):
        print("Processing ", file)
        df = pd.read_feather(file)
        comment_count += len(df)
        video_count += df['video_id'].nunique()
        df1 = df[~(df['comment_display'].isna()) & (df['comment_display'].str.contains('<a href=\"http'))]
        df1.to_csv('./comments_with_URL/' + filename.replace('feather', 'csv'), index=False)
        del df
        del df1
    print("video count: ", video_count)
    print("comment count: ", comment_count)


if __name__ == "__main__":
    main()