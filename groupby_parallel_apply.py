import multiprocessing
import time
import numpy as np
import pandas as pd

from sklearn import linear_model
from functools import partial
from typing import List


def _split_list(list_to_split: List, num_chunks: int):
    """Splits a list into approx. equally sized chunks
    Source: https://stackoverflow.com/a/2135920"""
    k, m = divmod(len(list_to_split), num_chunks)
    return [
        list_to_split[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)]
        for i in range(num_chunks)
    ]

# function needs to return grouping variable as well
def get_b1_coef(df, x_str, y_str, var_group_str):
    X = df[[x_str]].values
    y = df[[y_str]].values
    lm = linear_model.LinearRegression().fit(X, y)
    coef_list = lm.coef_
    coef_float = pd.DataFrame({var_group_str:df[var_group_str].unique(),
                 "b1":coef_list.item(0)})
    return coef_float


if __name__ == "__main__":
    # simulate data
    n_ids = 100
    n_rep = 10 # repeats per id
    x_vals = np.arange(-4.5, 5.5)
    ids = np.repeat(np.arange(1, n_ids+1), n_rep)
    x = np.tile(x_vals, n_ids)
    y = x * np.random.normal(loc=1, scale=3, size=len(x)) # positive releationship overall
    df = pd.DataFrame({"id":ids, "x":x, "y":y})

    f_partial = partial(get_b1_coef, x_str="x", y_str="y", var_group_str="id")
    list_to_process_no_names = [group for name, group in df.groupby("id")]

    p = multiprocessing.Pool(2)
    start = time.time()
    list_result = []
    for x in p.imap(f_partial, list_to_process_no_names):
        list_result.append(x)

    df_coefs_parallel = pd.concat(list_result, ignore_index=True)
    df_coefs_parallel.to_feather("data/df_coefs_parallel.feather")