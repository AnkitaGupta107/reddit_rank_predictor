import os

import pandas as pd


# Create your views here.

def get_filenames():
    cwd_path = os.getcwd()
    dir_path = os.path.join(cwd_path, 'data')
    filenames = os.listdir(dir_path)
    return filenames, dir_path


def get_dataframe(filename, dir_path):
    df = pd.read_csv(os.path.join(dir_path, filename))
    return df


def get_headers(filename, dir_path):
    df = get_dataframe(filename, dir_path)
    header_list = df.columns.values.tolist()
    return header_list


"""
Headers:
['created_utc', 'score', 'domain', 'id', 'title', 'author', 'ups', 'downs', 'num_comments', 'permalink', 'selftext',
'link_flair_text', 'over_18', 'thumbnail', 'subreddit_id', 'edited', 'link_flair_css_class', 'author_flair_css_class',
 'is_self', 'name', 'url', 'distinguished']
"""


def check_headers_for_all_files():
    files, dir_path = get_filenames()
    old_header = None
    counter = 0
    for file in files:
        new_header = get_headers(file, dir_path)
        if counter == 0:
            old_header = new_header
            counter = 1
            continue

        if cmp(old_header, new_header) != 0:
            break
        old_header = new_header
        counter += 1

        if counter > 10:  # TODO remove this later
            return counter
    return counter


def sort_as_per_score(filename, dir_path):
    df = get_dataframe(filename, dir_path)
    df = df.sort_values('score', ascending=False)
    df2 = df.head(3)
    df2.to_csv('2.csv', mode='a', header=False)


def get_post_from_sub_reddit_file(post_id, sub_reddit_file):
    cwd_path = os.getcwd()
    dir_path = os.path.join(cwd_path, 'data')
    file_path = os.path.join(dir_path, sub_reddit_file)
    df = pd.read_csv(file_path)
    value = df[df['id'] == post_id]
    return value


def score_predictor():
    post_id = raw_input('Enter ID of the post: ')
    sub_reddit_file = raw_input('Enter csv file name: ')

    value = get_post_from_sub_reddit_file(post_id, sub_reddit_file)
    top_score = value['ups'] - value['downs']
    score, actual_score = 0, 0
    if not top_score.empty:
        score = top_score.values[0]
        actual_score = value['score'].values[0]
    return score, actual_score


def search_sub_reddits():
    search_query = raw_input('Enter search query: ')
    files, dir_path = get_filenames()
    df = pd.DataFrame()
    for file in files:
        file_path = os.path.join(dir_path, file)
        sub_reddit_df = pd.read_csv(file_path)
        values = sub_reddit_df[sub_reddit_df['title'].str.contains(search_query, case=False)]
        df = df.append(values)

    df = df.sort(['score', 'created_utc'], ascending=False)
    return df


# get_post_from_sub_reddit_file('17o3du', '30ROCK.csv')


if __name__ == '__main__':
    predicted_score, actual_score = score_predictor()
    print "Predicted Score: ", predicted_score
    print "Actual Score: ", actual_score

    print "\n\n------------------------------------------------\n\n"
    searched_df = search_sub_reddits()
    print searched_df
