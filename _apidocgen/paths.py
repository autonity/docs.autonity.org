import glob
import json
import re
import subprocess
from functools import cache
from itertools import chain
from os import path
from typing import Any


class Paths:
    autonity_dir: str
    build_dir: str
    output_dir: str
    src_dir: str
    github_url: str

    def __init__(
        self, output_dir: str, autonity_dir: str, autonity_config: dict[str, str]
    ):
        self.output_dir = output_dir
        self.autonity_dir = path.abspath(path.realpath(autonity_dir))
        self.build_dir = path.join(self.autonity_dir, autonity_config["build_dir"])
        self.src_dir = path.join(self.autonity_dir, autonity_config["src_dir"])
        self.github_url = autonity_config["github_url"]

    def load_abi(self, contract_name: str) -> list[dict[str, Any]]:
        return load_json(path.join(self.build_dir, f"{contract_name}.abi"))

    def load_userdoc(self, contract_name: str) -> dict[str, Any]:
        return load_json(path.join(self.build_dir, f"{contract_name}.docuser"))

    def load_devdoc(self, contract_name: str) -> dict[str, Any]:
        return load_json(path.join(self.build_dir, f"{contract_name}.docdev"))

    def get_output_file_path(self, contract_display_name: str) -> str:
        git_tag = get_git_tag(self.autonity_dir)
        return path.join(
            self.output_dir, git_tag, contract_display_name.replace(" ", "-") + ".md"
        )

    def get_github_src_url(self, contract_name: str, regexp: re.Pattern) -> str | None:
        src_file = self.find_src_file(contract_name)
        return self._get_github_src_url_recursively(src_file, regexp, [])

    def _get_github_src_url_recursively(
        self,
        src_file: str,
        regexp: re.Pattern,
        checked_files: list[str],
    ) -> str | None:
        # Prevent infinite recursion
        if src_file in checked_files:
            return None
        checked_files.append(src_file)

        code = read_file(src_file)

        if match := regexp.search(code):
            lineno = code[: match.span()[0]].count("\n") + 1
            return self.construct_github_src_url(src_file, lineno)

        for rel_import in parse_solidity_imports(src_file):
            abs_import = path.abspath(path.join(path.dirname(src_file), rel_import))
            if url := self._get_github_src_url_recursively(
                abs_import, regexp, checked_files
            ):
                return url

        return None

    @cache
    def find_src_file(self, contract_name: str) -> str:
        if paths := glob.glob(
            path.join(self.src_dir, "**", f"{contract_name}.sol"), recursive=True
        ):
            return paths[0]
        raise RuntimeError(f"Could not find {contract_name}.sol in {self.src_dir}")

    def construct_github_src_url(self, src_file: str, lineno: int) -> str:
        relpath = path.relpath(src_file, self.autonity_dir)
        git_tag = get_git_tag(self.autonity_dir)
        return f"{self.github_url}/tree/{git_tag}/{relpath}#L{lineno}"


def load_json(file: str) -> Any:
    with open(file) as f:
        return json.load(f)


@cache
def get_git_tag(repo_root: str) -> str:
    return subprocess.check_output(
        ["git", "describe", "--tags"], cwd=repo_root, text=True
    ).strip()


@cache
def read_file(file: str) -> str:
    with open(file) as f:
        return f.read()


def parse_solidity_imports(file: str) -> list[str]:
    quote = r"['\"]"
    matches = re.findall(
        rf"(import +{quote}(.+?){quote}|import.+from +{quote}(.+?){quote})",
        read_file(file),
        re.MULTILINE,
    )
    return [item for item in chain(*[match[1:] for match in matches]) if item != ""]
