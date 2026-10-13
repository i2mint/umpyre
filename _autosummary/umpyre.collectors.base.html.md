# umpyre.collectors.base

Base collector class with Mapping interface.

### Classes

| [`CollectorRegistry`](#umpyre.collectors.base.CollectorRegistry)()   | Registry for managing available collectors.                  |
|------------------------------------------------------------------------|--------------------------------------------------------------|
| [`MetricCollector`](#umpyre.collectors.base.MetricCollector)()     | Abstract base for metric collectors using Mapping interface. |

### *class* umpyre.collectors.base.CollectorRegistry

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Registry for managing available collectors.

#### get(name)

Get collector class by name.

* **Return type:**
  [`type`](https://docs.python.org/3/builtins/functions.html#type)[[`MetricCollector`](#umpyre.collectors.base.MetricCollector)]

#### list_collectors()

List all registered collector names.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### register(name, collector_class)

Register a collector class.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Collector identifier
  * **collector_class** ([`type`](https://docs.python.org/3/builtins/functions.html#type)[[`MetricCollector`](#umpyre.collectors.base.MetricCollector)]) – MetricCollector subclass

### *class* umpyre.collectors.base.MetricCollector

Bases: [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping), [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC)

Abstract base for metric collectors using Mapping interface.

Collectors implement the Mapping protocol to provide dict-like access
to collected metrics, enabling flexible composition and iteration.

### Example

```pycon
>>> class SimpleCollector(MetricCollector):
...     def collect(self) -> dict:
...         return {'lines': 100, 'functions': 10}
>>> collector = SimpleCollector()
>>> collector['lines']
100
>>> list(collector)
['lines', 'functions']
```

#### *abstractmethod* collect()

Collect metrics and return as dictionary.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Dictionary of metric names to values

#### refresh()

Force re-collection of metrics.

#### to_dict()

Export all metrics as dictionary.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
