# umpyre.config

Configuration loading and validation for umpyre.

### Classes

| [`Config`](#umpyre.config.Config)([config_path, config_dict])   | Configuration manager for umpyre metrics collection.   |
|---------------------------------------------------------------------------------------|--------------------------------------------------------|

### Exceptions

| [`ConfigError`](#umpyre.config.ConfigError)   | Raised when configuration is invalid.   |
|----------------------------------------------------------------|-----------------------------------------|

### *class* umpyre.config.Config(config_path=None, config_dict=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Configuration manager for umpyre metrics collection.

#### collector_config(collector_name)

Get configuration for a specific collector.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

#### *classmethod* from_dict(config)

Create config from dictionary.

* **Return type:**
  [`Config`](#umpyre.config.Config)

#### *classmethod* from_file(path)

Load config from YAML file.

* **Return type:**
  [`Config`](#umpyre.config.Config)

#### get(\*keys, default=None)

Get nested config value.

* **Parameters:**
  * **\*keys** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Nested keys (e.g., ‘collectors’, ‘wily’, ‘enabled’)
  * **default** ([`Any`](https://docs.python.org/3/library/typing.html#typing.Any)) – Default value if key not found
* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)
* **Returns:**
  Config value or default

```pycon
>>> config = Config(config_dict={'collectors': {'wily': {'enabled': True}}})
>>> config.get('collectors', 'wily', 'enabled')
True
>>> config.get('collectors', 'missing', default='default_value')
'default_value'
```

#### is_collector_enabled(collector_name)

Check if a collector is enabled.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

#### *property* retention_strategy *: [str](https://docs.python.org/3/builtins/stdtypes.html#str)*

Get data retention strategy.

#### *property* storage_branch *: [str](https://docs.python.org/3/builtins/stdtypes.html#str)*

Get the storage branch name.

#### *property* storage_formats *: [list](https://docs.python.org/3/builtins/stdtypes.html#list)[[str](https://docs.python.org/3/builtins/stdtypes.html#str)]*

Get enabled storage formats.

#### to_dict()

Export config as dictionary.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *exception* umpyre.config.ConfigError

Bases: [`Exception`](https://docs.python.org/3/builtins/exceptions.html#Exception)

Raised when configuration is invalid.
