import json
import logging
import subprocess

from .contract import ContractArtefactTuple, ContractConfigTuple
from .paths import Paths

logger = logging.getLogger("solc")


def compile_contracts(
    contracts: list[ContractConfigTuple], paths: Paths
) -> list[ContractArtefactTuple]:
    logger.info("Compiling contracts: %s", ", ".join(name for name, _ in contracts))
    src_files = [paths.find_src_file(name) for name, _ in contracts]

    process = subprocess.run(
        ["solc", "--combined-json", "abi,devdoc,userdoc"] + src_files,
        capture_output=True,
        text=True,
    )
    if process.returncode and process.stderr:
        logger.error(process.stderr)
    process.check_returncode()
    combined_json = json.loads(process.stdout)

    artefacts = []
    for name, _ in contracts:
        for key, value in combined_json["contracts"].items():
            if key.split(":")[-1] == name:
                artefacts.append((value["abi"], value["devdoc"], value["userdoc"]))
                break
        else:
            assert False

    return artefacts
