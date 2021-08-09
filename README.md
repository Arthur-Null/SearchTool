# SearchTool

A simple tool for quick grid search for machine learning experiments

## Install

```
python setup.py install
```

## Usage

```
from search_tool.local import run_exps

config = {
    "log_dir": ".",
    "search": {"a": {"type": "choice", "value": [1, 2, 3, 4]}, "b": {"type": "range", "value": [0, 5, 1]}},
}


def run(config):
    print(config)


run_exps(config, run)


"""
OUTPUT:
{'a': 1, 'b': 0, 'log_dir': './0/'}
{'a': 1, 'b': 1, 'log_dir': './1/'}
{'a': 1, 'b': 2, 'log_dir': './2/'}
{'a': 1, 'b': 3, 'log_dir': './3/'}
{'a': 1, 'b': 4, 'log_dir': './4/'}
{'a': 2, 'b': 0, 'log_dir': './5/'}
{'a': 2, 'b': 1, 'log_dir': './6/'}
{'a': 2, 'b': 2, 'log_dir': './7/'}
{'a': 2, 'b': 3, 'log_dir': './8/'}
{'a': 2, 'b': 4, 'log_dir': './9/'}
{'a': 3, 'b': 0, 'log_dir': './10/'}
{'a': 3, 'b': 1, 'log_dir': './11/'}
{'a': 3, 'b': 2, 'log_dir': './12/'}
{'a': 3, 'b': 3, 'log_dir': './13/'}
{'a': 3, 'b': 4, 'log_dir': './14/'}
{'a': 4, 'b': 0, 'log_dir': './15/'}
{'a': 4, 'b': 1, 'log_dir': './16/'}
{'a': 4, 'b': 2, 'log_dir': './17/'}
{'a': 4, 'b': 3, 'log_dir': './18/'}
{'a': 4, 'b': 4, 'log_dir': './19/'}
"""
```

## TODO

[ ] More types of search spaces.
[ ] Search on multiple machines base on redis.
