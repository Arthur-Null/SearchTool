"""
Merge a amulet submit config file.
"""
import yaml
import click
import copy
from itertools import product


def get_space(d: dict):
    if d["spec"] == "discrete":
        return d["values"]
    else:
        raise ValueError("Unknown spec type: {}".format(d["spec"]))


@click.command()
@click.argument("config-file", type=click.File("r"))
@click.option("--merge-paras", "-m", type=str, multiple=True, default=["dataset", "seed"])
@click.option("--out-file", type=str, default="./submit.yml")
def merge_submit(config_file, merge_paras, out_file):
    submit = yaml.load(config_file, Loader=yaml.FullLoader)
    name = submit["search"]["job_template"]["name"]
    run_command = submit["search"]["job_template"]["command"][-1]
    searches = submit["search"]["params"]
    print(f"original search space: {len(list(product(*[get_space(d) for d in searches])))}")
    merged_searches = [d for d in searches if d["name"] in merge_paras]
    searches = [d for d in searches if d["name"] not in merge_paras]
    print(f"merged search space: {len(list(product(*[get_space(d) for d in searches])))}")
    outdir_command = "--runtime.output_dir $$AMLT_OUTPUT_DIR/"
    for para in merge_paras:
        name = name.replace("{" + para + "}", "")
        name = name.replace("__", "_")
    if name[-1] == "_":
        name = name[:-1]
    spaces = [get_space(d) for d in merged_searches]
    search_space = list(product(*spaces))

    run_commands = []
    for para_combined in search_space:
        this_run_command = copy.deepcopy(run_command)
        this_outdir_command = copy.deepcopy(outdir_command)
        for i, para in enumerate(merge_paras):
            this_run_command = this_run_command.replace("{" + para + "}", str(para_combined[i]))
            this_outdir_command += str(para_combined[i]) + "_"
        if this_outdir_command[-1] == "_":
            this_outdir_command = this_outdir_command[:-1]
        this_run_command += " " + this_outdir_command
        run_commands.append(this_run_command)
    submit["search"]["job_template"]["name"] = name
    submit["search"]["job_template"]["command"] = submit["search"]["job_template"]["command"][:-1] + run_commands
    submit["search"]["params"] = searches
    with open(out_file, "w") as f:
        yaml.dump(submit, f)


if __name__ == "__main__":
    merge_submit()
