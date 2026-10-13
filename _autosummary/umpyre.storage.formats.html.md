# umpyre.storage.formats

JSON and CSV serialization for metrics.

### Functions

| [`deserialize_metrics`](#umpyre.storage.formats.deserialize_metrics)(file_path[, format])       | Deserialize metrics from file.   |
|-------------------------------------------------------------------------------------------------|----------------------------------|
| [`serialize_metrics`](#umpyre.storage.formats.serialize_metrics)(data, output_path[, format]) | Serialize metrics to file.       |

### umpyre.storage.formats.deserialize_metrics(file_path, format='json')

Deserialize metrics from file.

* **Parameters:**
  * **file_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to input file
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Format (‘json’ or ‘csv’)
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Metric dictionary

### umpyre.storage.formats.serialize_metrics(data, output_path, format='json')

Serialize metrics to file.

* **Parameters:**
  * **data** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Metric dictionary
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to output file
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Format (‘json’ or ‘csv’)
