# umpyre.schema

Versioned schema for metrics storage and migration support.

### Classes

| [`MetricSchema`](#umpyre.schema.MetricSchema)([version])   | Versioned schema for metrics storage with migration support.   |
|----------------------------------------------------------------------------|----------------------------------------------------------------|

### *class* umpyre.schema.MetricSchema(version='1.0')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Versioned schema for metrics storage with migration support.

#### *classmethod* create_metric_data(commit_sha, metrics, commit_message=None, python_version=None, workflow_status=None, collection_duration=None)

Create a standardized metric data structure.

* **Parameters:**
  * **commit_sha** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Git commit SHA
  * **metrics** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Dictionary of collected metrics
  * **commit_message** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional commit message
  * **python_version** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional Python version string
  * **workflow_status** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)]) – Optional workflow status dict
  * **collection_duration** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`float`](https://docs.python.org/3/builtins/functions.html#float)]) – Optional collection time in seconds
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Standardized metric dictionary

#### *classmethod* current_version()

Return the current schema version.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### *classmethod* migrate(data, from_version)

Migrate data from old schema version to current version.

* **Parameters:**
  * **data** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Metric data in old format
  * **from_version** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Version of the input data
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Migrated data in current schema format

#### *classmethod* validate(data)

Validate that data conforms to schema.

* **Parameters:**
  **data** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Metric data to validate
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if valid, raises ValueError otherwise
