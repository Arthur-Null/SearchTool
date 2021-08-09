from search_tool.local import run_exps

config = {
    "log_dir": ".",
    "search": {"a": {"type": "choice", "value": [1, 2, 3, 4]}, "b": {"type": "range", "value": [0, 5, 1]}},
}


def run(config):
    print(config)


run_exps(config, run)
