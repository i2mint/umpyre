# umpyre
Code analysis and quality metrics


To install:	```pip install umpyre```


# Examples of use

Get stats about packages. Your own, or other's.

Note: These examples will probably not work as doctests, 
since results are sensitive to other slight system differences (such as python version etc.))

```pydocstring
>>> from umpyre import modules_info_df
>>> import collections
>>> modules_info_df(collections)
                      lines  empty_lines  ...  num_of_functions  num_of_classes
collections.__init__   1280          189  ...                 1               9
collections.abc           3            1  ...                 0              25
<BLANKLINE>
[2 rows x 7 columns]
>>> modules_info_df_stats(collections.abc)
lines                      1283.000000
empty_lines                 190.000000
comment_lines                79.000000
docs_lines                  133.000000
function_lines              138.000000
num_of_functions              1.000000
num_of_classes               34.000000
empty_lines_ratio             0.148090
comment_lines_ratio           0.061574
function_lines_ratio          0.107560
mean_lines_per_function     138.000000
dtype: float64
```

Multiple packages (nice for comparing).

```pydocstring
>>> from umpyre import stats_of
>>> stats_of(['urllib', 'json', 'collections'])
                              urllib         json  collections
empty_lines_ratio           0.157293     0.136503     0.148090
comment_lines_ratio         0.075217     0.038344     0.061574
function_lines_ratio        0.212391     0.448620     0.107560
mean_lines_per_function    13.463768    41.785714   138.000000
lines                    4374.000000  1304.000000  1283.000000
empty_lines               688.000000   178.000000   190.000000
comment_lines             329.000000    50.000000    79.000000
docs_lines                425.000000   218.000000   133.000000
function_lines            929.000000   585.000000   138.000000
num_of_functions           69.000000    14.000000     1.000000
num_of_classes             55.000000     3.000000    34.000000
```
