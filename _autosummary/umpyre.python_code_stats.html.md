# umpyre.python_code_stats

Get stats about packages. Your own, or other’s.
Things like…
(Note that these will probably not work as doctests, since results are sensisitive to other slight system differences
(such as python version etc.))

```pycon
>>> import collections
>>> modules_info_df(collections)
                      lines  empty_lines  ...  num_of_functions  num_of_classes
collections.__init__   1280          189  ...                 1               9
collections.abc           3            1  ...                 0              25

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

### Functions

| `get_objs`(root, k)                                                                                |                                                                                                 |
|----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| `lines`(string)                                                                                    |                                                                                                 |
| [`modules_info_df`](#umpyre.python_code_stats.modules_info_df)(root[, filepath_filt, ...])       | A pandas DataFrame of stats of the root (package or directory thereof).                         |
| [`modules_info_df_stats`](#umpyre.python_code_stats.modules_info_df_stats)(root[, filepath_filt, ...]) | A pandas Series of statistics over all modules of some root (package or directory thereof).     |
| [`modules_info_gen`](#umpyre.python_code_stats.modules_info_gen)(root[, filepath_filt, on_error]) | Yields statistics (as dicts) of modules under the root module or directory of a python package. |
| `no_test_folder`(path)                                                                             |                                                                                                 |
| `only_py_ext`(path)                                                                                |                                                                                                 |
| [`stats_of`](#umpyre.python_code_stats.stats_of)(modules[, filepath_filt, ...])           | A dataframe of stats of the input modules.                                                      |

### umpyre.python_code_stats.modules_info_df(root, filepath_filt=<function <lambda>>, index_field=None, on_error='ignore')

A pandas DataFrame of stats of the root (package or directory thereof).

* **Parameters:**
  * **root** – module or directory path
  * **filepath_filt** – filepath filter function or regular expression
  * **index_field** – function or field string that should be used for the indexing of modules
  * **on_error** – What to do when an error occurs when extracting information from a module.
    Values are ‘ignore’, ‘print’, or ‘raise’
* **Returns:**
  A DataFrame whose rows contain information for each module

```pycon
>>> import urllib
>>> df = modules_info_df(urllib)
>>> df
                    lines  empty_lines  ...  num_of_functions  num_of_classes
urllib.error           78           18  ...                 0               3
urllib.request       2774          410  ...                23              28
urllib.__init__         1            1  ...                 0               0
urllib.response        81           24  ...                 0               4
urllib.robotparser    274           36  ...                 0               4
urllib.parse         1166          199  ...                46              16

[6 rows x 7 columns]
```

### umpyre.python_code_stats.modules_info_df_stats(root, filepath_filt=<function <lambda>>, index_field=None, on_error='ignore')

A pandas Series of statistics over all modules of some root (package or directory thereof).

* **Parameters:**
  * **root** – module or directory path
  * **filepath_filt** – filepath filter function or regular expression
  * **index_field** – function or field string that should be used for the indexing of modules
  * **on_error** – What to do when an error occurs when extracting information from a module.
    Values are ‘ignore’, ‘print’, or ‘raise’
* **Returns:**
  A Series whose rows containing statistics

```pycon
>>> import json
>>> df = modules_info_df_stats(json)
>>> df
lines                      1301.000000
empty_lines                 178.000000
comment_lines                50.000000
docs_lines                  218.000000
function_lines              585.000000
num_of_functions             14.000000
num_of_classes                3.000000
empty_lines_ratio             0.136818
comment_lines_ratio           0.038432
function_lines_ratio          0.449654
mean_lines_per_function      41.785714
dtype: float64
>>> modules_info_df_stats('collections.abc')
lines                      1276.000000
empty_lines                 190.000000
comment_lines                73.000000
docs_lines                  133.000000
function_lines              138.000000
num_of_functions              1.000000
num_of_classes               34.000000
empty_lines_ratio             0.148903
comment_lines_ratio           0.057210
function_lines_ratio          0.108150
mean_lines_per_function     138.000000
dtype: float64
```

### umpyre.python_code_stats.modules_info_gen(root, filepath_filt=<function <lambda>>, on_error='ignore')

Yields statistics (as dicts) of modules under the root module or directory of a python package.

* **Parameters:**
  * **root** – module instance, dot path, or directory path
  * **filepath_filt** – filepath filter function or regular expression
  * **on_error** – What to do when an error occurs when extracting information from a module.
    Values are ‘ignore’, ‘print’, ‘raise’, or ‘yield’
* **Returns:**
  A generator of dicts

### umpyre.python_code_stats.stats_of(modules, filepath_filt=<function <lambda>>, index_field=None, on_error='ignore')

A dataframe of stats of the input modules.

* **Parameters:**
  * **modules** – list of importable names
  * **root** – module or directory path
  * **filepath_filt** – filepath filter function or regular expression
  * **index_field** – function or field string that should be used for the indexing of modules
  * **on_error** – What to do when an error occurs when extracting information from a module.
    Values are ‘ignore’, ‘print’, or ‘raise’
* **Returns:**

```pycon
>>> df = stats_of(['urllib', 'json', 'collections'])
>>> assert set(df.index.values).issuperset(
...     {'empty_lines_ratio', 'comment_lines_ratio', 'function_lines_ratio', 'mean_lines_per_function'})
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
