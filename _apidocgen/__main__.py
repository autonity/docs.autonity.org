"""Markdown API reference documentation generator for docs.autonity.org."""

import argparse
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import path

from .compiler import compile_contracts
from .config import load_toml, validate_config
from .contract import (
    ContractArtefactTuple,
    ContractConfigTuple,
    generate_contract_doc,
    load_contract_artefacts,
)
from .paths import Paths
from .observer import run_file_observer

PROG = "apidocgen"

DEFAULT_AUTONITY_PATH = "autonity"
DEFAULT_CONFIG_FILE = "apidoc.toml"


def main() -> None:
    if os.environ.get("DEBUG") not in ("1", "true", "True"):
        sys.tracebacklimit = 0

    args = parse_args()
    config = load_toml(args.config)
    validate_config(config)

    paths = Paths(
        config["contracts"]["output_dir"],
        args.autonity,
        config["autonity"],
    )
    configs = sorted(
        [
            (name, value)
            for name, value in config["contracts"].items()
            if name != "output_dir"
        ],
        key=lambda item: item[0].casefold(),
    )

    if args.watch:

        def compile_and_generate() -> None:
            artefacts = compile_contracts(configs, paths)
            generate_contract_docs(artefacts, configs, paths)

        compile_and_generate()
        run_file_observer(paths.src_dir, ".sol", compile_and_generate)
    else:
        artefacts = [load_contract_artefacts(name, paths) for name, _ in configs]
        generate_contract_docs(artefacts, configs, paths)


def generate_contract_docs(
    artefacts: list[ContractArtefactTuple],
    configs: list[ContractConfigTuple],
    paths: Paths,
) -> None:
    assert len(artefacts) == len(configs)

    # Add missing defaults to config
    for name, config in configs:
        config["display_name"] = config.get("display_name", name)

    # Remove old bindings because the config might have been changed
    shutil.rmtree(paths.output_dir, ignore_errors=True)

    pending_tasks = []
    executor = ThreadPoolExecutor()

    for i in range(len(configs)):
        _, prev_config = configs[i - 1] if i > 0 else (None, None)
        _, next_config = configs[i + 1] if i < len(configs) - 1 else (None, None)

        pending_tasks.append(
            executor.submit(
                generate_contract_doc,
                *configs[i],
                *artefacts[i],  # type: ignore
                prev_config,
                next_config,
                paths,
            )
        )

    for completed_task in as_completed(pending_tasks):
        if exception := completed_task.exception():
            executor.shutdown()
            raise exception


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=PROG, description=__doc__)
    parser.add_argument(
        "--autonity",
        metavar="DIR",
        default=DEFAULT_AUTONITY_PATH,
        help="the Autonity repository root directory [default: ./{}]".format(
            path.relpath(DEFAULT_AUTONITY_PATH, os.getcwd())
        ),
    )
    parser.add_argument(
        "--config",
        metavar="FILE",
        default=DEFAULT_CONFIG_FILE,
        help="the configuration TOML file [default: ./{}]".format(
            path.relpath(DEFAULT_CONFIG_FILE, os.getcwd())
        ),
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help=(
            "watch the source directory for changes and regenerate the documentation "
            "when contracts are modified"
        ),
    )
    return parser.parse_args()


main()
