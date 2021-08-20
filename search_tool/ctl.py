import os
from pathlib import Path
import argparse
import yaml
import subprocess
from itertools import product

from .util import get_search_space

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--entry", '-e', type=str)
    parser.add_argument("--config", '-c', type=str)
    parser.add_argument("--search", '-s', type=str)
    args = parser.parse_args()

    with open(args.search) as f:
        search_space = yaml.load(f)

    keys = []
    spaces = []
    for k, v in search_space.items():
        keys.append(k)
        spaces.append(get_search_space(v))
    configs = product(*spaces)
    with open(args.config) as f:
        raw_config = yaml.load(f)
        try:
            raw_output_dir = raw_config['runtime']['output_dir']
        except ValueError:
            raw_output_dir = './outputs/'

    for i, config in enumerate(configs):
        command = ['python', '-m', args.entry, args.config]
        for j, value in enumerate(config):
            command.append(f"--{keys[j]}")
            command.append(str(value))
        command.append('--runtime.output_dir')
        new_output_dir = Path(raw_output_dir)
        suffix = ''
        for value in config:
            suffix += f"{value}_"
        suffix = suffix[:-1]
        new_output_dir = new_output_dir / suffix
        if os.path.exists(new_output_dir):
            continue
        else:
            os.makedirs(new_output_dir)
        command.append(str(new_output_dir))
        subprocess.run(command)
    print("All done")
