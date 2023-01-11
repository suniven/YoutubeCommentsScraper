import pandas as pd


def main():
    start = 0
    step = 20000
    csv_file_path = './VideoId.csv'
    save_path = './'
    url_df = pd.read_csv(csv_file_path, encoding='utf-8', engine='python', na_values='null')
    count = url_df.shape[0]
    while count > 0:
        if count < step:
            end = url_df.shape[0]
        else:
            end = start + step
        block_df = url_df.iloc[start:end, :]
        block_df.to_csv(save_path + "{0}-{1}.csv".format(start, end - 1), index=False)
        count -= step
        start = end


if __name__ == '__main__':
    main()
