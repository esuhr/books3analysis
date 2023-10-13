from rapidfuzz import process, utils
import polars as pl
import pickle
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import json

# read in books3 data and create list of titles
with open('books_titles.pickle', 'rb') as f:
    books_titles = pickle.load(f)

# read in goodreads titles pickle file
with open('goodreads_titles.pickle', 'rb') as f:
    goodreads_titles = pickle.load(f)

# define matching function
def match_titles(title):
    """
    Function to match titles from goodreads to books3 data
    """
    # use rapidfuzz to match titles
    match = process.extractOne(title, goodreads_titles, score_cutoff=85.51, processor=utils.default_process)
    # return the match and the score
    if match:
        with open('matches.json', 'a') as f:
            json.dump({'title': title, 'match': match[0], 'score': match[1]}, f)
            f.write('\n')

def main():
    # create pool of worker processes
    with Pool(cpu_count()) as pool:
        # map titles to worker processes
        list(tqdm(pool.imap(match_titles, books_titles), total=len(books_titles)))

if __name__ == '__main__':
    main()