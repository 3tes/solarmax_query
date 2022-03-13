# solarmax_query
A python library for quering SolarMax inverters

This was create with the help of: https://github.com/bwurst/python-solarmax

You can read about the exact specifications of the protocol in the pdf in the docs folder.

## Installation
```python
pip install solarmax_query
```

## Usage
```python
from solarmax_query import SolarMax
solarmax = SolarMax(host, port, index)
```