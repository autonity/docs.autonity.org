"""Contract parser.

Loads and parses contract artefacts and converts data into Markdown.
"""

import logging
import re
from enum import Enum
from os import path
from typing import TypeAlias

from . import DEBUG
from .paths import Paths
from .markdown import MarkdownDocument

NATSPEC_VERSION = 1

ContractArtefactTuple: TypeAlias = tuple[list[dict], dict, dict]  # abi, devdoc, userdoc
ContractConfigTuple: TypeAlias = tuple[str, dict]  # contract_name, contract_config
ItemType = Enum("ItemType", ("CONTRACT", "FUNCTION", "EVENT"))


def load_contract_artefacts(name: str, paths: Paths) -> ContractArtefactTuple:
    abi = paths.load_abi(name)
    devdoc = paths.load_devdoc(name)
    userdoc = paths.load_userdoc(name)

    assert isinstance(abi, list), "Invalid ABI file format"
    assert isinstance(userdoc, dict), "Invalid NatSpec file format"
    assert isinstance(devdoc, dict), "Invalid NatSpec file format"
    assert devdoc["version"] == NATSPEC_VERSION, "Unsupported NatSpec version"
    assert devdoc["kind"] == "dev", "Unexpected NatSpec document 'kind'"
    assert userdoc["version"] == NATSPEC_VERSION, "Unsupported NatSpec version"
    assert userdoc["kind"] == "user", "Unexpected NatSpec document 'kind'"

    return (abi, devdoc, userdoc)


def generate_contract_doc(
    name: str,
    config: dict,
    abi: list[dict],
    devdoc: dict,
    userdoc: dict,
    prev_config: dict | None,
    next_config: dict | None,
    paths: Paths,
) -> None:
    logger = logging.getLogger(name)

    abi = sorted(abi, key=lambda item: item.get("name", ""))

    doc = MarkdownDocument()
    doc.add_meta({"title": config["display_name"]})

    if "notice" in userdoc:
        doc.add_paragraph(userdoc["notice"])
    if "details" in devdoc:
        doc.add_paragraph(devdoc["details"])

    for item_type in (ItemType.EVENT, ItemType.FUNCTION):
        if abi_items := filter_abi_items(abi, item_type):
            userdoc_items = filter_natspec_items(userdoc, item_type)
            devdoc_items = filter_natspec_items(devdoc, item_type)

            subtitle = {
                ItemType.EVENT: "Events",
                ItemType.FUNCTION: "Functions",
            }[item_type]
            doc.add_header(2, subtitle)

            for abi_item in abi_items:
                if abi_item["name"] in config.get("excludes", []):
                    continue

                signature_for_lookup = get_abi_signature_for_lookup(abi_item)
                userdoc_item = userdoc_items.get(signature_for_lookup, {})
                devdoc_item = devdoc_items.get(signature_for_lookup, {})

                signature_for_title = get_abi_signature_for_title(abi_item)

                if "custom:exclude" in devdoc_item:
                    continue
                if not (userdoc_item or devdoc_item):
                    logger.warning("%s is undocumented", signature_for_title)

                if link := paths.get_github_src_url(
                    name, src_definition_regexp(abi_item, item_type)
                ):
                    item_title = doc.format_link(signature_for_title, link)
                elif DEBUG:
                    raise RuntimeError(
                        f"{signature_for_lookup} could not be linked to source code"
                    )
                else:
                    logger.warning(
                        "%s could not be linked to source code", signature_for_lookup
                    )
                    item_title = signature_for_title
                doc.add_header(3, item_title)

                if notice := userdoc_item.get("notice"):
                    doc.add_paragraph(notice)

                if details := devdoc_item.get("details"):
                    doc.add_paragraph(details)

                if emitted_events := devdoc_item.get("custom:event"):
                    doc.add_paragraph(emitted_events)

                inputs_table = []
                for abi_input in abi_item.get("inputs", []):
                    inputs_table.append(
                        [
                            abi_input["name"],
                            abi_input["type"],
                            devdoc_item.get("params", {}).get(abi_input["name"], ""),
                        ]
                    )
                if inputs_table:
                    doc.add_header(4, "Parameters")
                    doc.add_table(["Name", "Type", "Description"], inputs_table)

                if item_type is ItemType.FUNCTION and is_view_function(abi_item):
                    outputs_table = []
                    for i, abi_output in enumerate(abi_item.get("outputs", [])):
                        output_name = abi_output["name"] or f"_{i}"
                        outputs_table.append(
                            [
                                abi_output["name"],
                                abi_output["type"],
                                devdoc_item.get("returns", {}).get(output_name, ""),
                            ]
                        )
                    if outputs_table:
                        doc.add_header(4, "Returns")
                        doc.add_table(["Name", "Type", "Description"], outputs_table)

    output_file = paths.get_output_file_path(config["display_name"])

    nav_links = []
    if prev_config:
        link = path.relpath(
            paths.get_output_file_path(prev_config["display_name"]),
            path.dirname(output_file),
        )
        nav_links.append(
            f'prev-url="{link}" prev-contract="{prev_config["display_name"]}"'
        )
    if next_config:
        link = path.relpath(
            paths.get_output_file_path(next_config["display_name"]),
            path.dirname(output_file),
        )
        nav_links.append(
            f'next-url="{link}" next-contract="{next_config["display_name"]}"'
        )
    if nav_links:
        doc.add_macro("{.footer-navigation " + " ".join(nav_links) + "}")

    doc.write_to_file(output_file)
    logger.info("Generated %s", output_file)


def get_abi_signature_for_title(abi_item: dict) -> str:
    # Doesn't expand struct types
    abi_inputs = abi_item.get("inputs", [])
    return abi_item["name"] + "({})".format(
        ",".join(abi_input["type"] for abi_input in abi_inputs)
    )


def get_abi_signature_for_lookup(abi_item: dict) -> str:
    # Expands struct types
    params = [
        _abi_input_to_singature_type(abi_input)
        for abi_input in abi_item.get("inputs", [])
    ]
    return abi_item["name"] + "({})".format(",".join(params))


def _abi_input_to_singature_type(abi_input: dict) -> str:
    if abi_input["type"] == "tuple":
        tuple_elems = [
            _abi_input_to_singature_type(abi_component)
            for abi_component in abi_input["components"]
        ]
        return "({})".format(",".join(tuple_elems))
    return abi_input["type"]


def is_view_function(abi_item: dict) -> bool:
    return abi_item["stateMutability"] in ("view", "pure")


def filter_abi_items(abi: list[dict], item_type: ItemType) -> list[dict]:
    abi_type = {ItemType.FUNCTION: "function", ItemType.EVENT: "event"}[item_type]
    return [item for item in abi if item["type"] == abi_type]


def filter_natspec_items(natspec: dict, item_type: ItemType) -> dict:
    natspec_key = {ItemType.FUNCTION: "methods", ItemType.EVENT: "events"}[item_type]
    return natspec.get(natspec_key, {})


def src_definition_regexp(
    abi_item: dict,
    item_type: ItemType,
) -> re.Pattern:
    name = abi_item["name"]
    parameter_types = [
        abi_type_to_sol_type_regexp(input["internalType"])
        for input in abi_item.get("inputs", [])
    ]

    # Match e.g. `vote(uint256 _commit, int256[] memory _reports, uint256 _salt )`
    sep = r"[\s\n]*"
    signature = rf"{name}{sep}\({sep}" + rf".+,{sep}".join(parameter_types) + r".+\)"

    regexp_for_item_type = {
        ItemType.EVENT: f"event{sep}{signature}",
        # A contract function is either a Solidity `function` or an auto-generated
        # accessor function for a public contract property
        ItemType.FUNCTION: f"(function{sep}{signature}|public.+{name}{sep}[;=])",
    }[item_type]
    return re.compile(regexp_for_item_type, re.MULTILINE | re.DOTALL)


def abi_type_to_sol_type_regexp(internal_type: str) -> str:
    # E.g. `struct Oracle.RoundData` in ABI is `RoundData` in Solidity code
    type_parts = internal_type.split(" ")
    if type_parts[0] in ("enum", "struct", "contract"):
        return type_parts[-1].split(".")[-1]

    # `int256` in ABI can either be `int` or `int256` in Solidity code
    # https://docs.soliditylang.org/en/v0.8.27/types.html
    internal_type = re.sub(r"(u?int)(256)(\[\])?$", r"(\1\3|\1\2\3)", internal_type)

    # In array types e.g. `int256[]` the brackets should be escaped
    return internal_type.replace("[]", r"\[\]")
