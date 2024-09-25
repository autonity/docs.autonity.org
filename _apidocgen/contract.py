"""Contract parser.

Loads and parses contract artefacts and converts data into Markdown.
"""

import logging
import re
from enum import StrEnum
from os import path
from typing import TypeAlias, cast

import eth_utils
from eth_typing import ABI

from .paths import Paths
from .markdown import MarkdownDocument

NATSPEC_VERSION = 1

ContractArtefactTuple: TypeAlias = tuple[ABI, dict, dict]  # abi, devdoc, userdoc
ContractConfigTuple: TypeAlias = tuple[str, dict]  # contract_name, contract_config
ElementType = StrEnum("ElementType", ("FUNCTION", "EVENT"))


def load_contract_artefacts(name: str, paths: Paths) -> ContractArtefactTuple:
    abi = cast(ABI, paths.load_abi(name))
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
    abi: ABI,
    devdoc: dict,
    userdoc: dict,
    prev_config: dict | None,
    next_config: dict | None,
    paths: Paths,
) -> None:
    logger = logging.getLogger(name)
    abi = sorted(abi, key=lambda element: element.get("name", ""))  # type: ignore
    doc = MarkdownDocument()

    doc.add_meta({"title": config["display_name"]})
    if "notice" in userdoc:
        doc.add_paragraph(userdoc["notice"])

    for element_type in (ElementType.EVENT, ElementType.FUNCTION):
        if abi_elements := eth_utils.filter_abi_by_type(str(element_type), abi):  # type: ignore
            userdoc_elements = filter_natspec_by_type(element_type, userdoc)
            devdoc_elements = filter_natspec_by_type(element_type, devdoc)

            subtitle = {
                ElementType.EVENT: "Events",
                ElementType.FUNCTION: "Functions",
            }[element_type]
            doc.add_header(2, subtitle)

            for abi_element in abi_elements:
                if abi_element["name"] in config.get("excludes", []):
                    continue

                signature = eth_utils.abi.abi_to_signature(abi_element)
                userdoc_element = userdoc_elements.get(signature, {})
                devdoc_element = devdoc_elements.get(signature, {})

                if "custom:exclude" in devdoc_element:
                    continue

                metadata = ""

                if element_type is ElementType.FUNCTION:
                    selector = eth_utils.conversions.to_hex(
                        eth_utils.abi.function_abi_to_4byte_selector(abi_element)
                    )
                    metadata = doc.format_macro(
                        '{.meta-data mutability-type="'
                        + abi_element["stateMutability"]
                        + '" selector="'
                        + selector
                        + '"}'
                    )

                github_src_link = doc.format_link(
                    abi_element["name"],
                    paths.get_github_src_url(
                        name, src_definition_regexp(abi_element, element_type)
                    ),
                )
                header = doc.format_header(3, github_src_link)

                doc.add_macro("{.method-title}\n" + header + metadata)

                if notice := userdoc_element.get("notice"):
                    doc.add_paragraph(notice)
                else:
                    logger.warning("%s is missing @notice", signature)

                if emitted_events := devdoc_element.get("custom:event"):
                    doc.add_paragraph(emitted_events)

                devdoc_params = devdoc_element.get("params", {})
                if not devdoc_params:
                    logger.warning("%s is missing @params", signature)

                inputs_table = []
                for abi_input in abi_element.get("inputs", []):
                    inputs_table.append(
                        [
                            abi_input["name"],
                            abi_input["type"],
                            devdoc_params.get(abi_input["name"], ""),
                        ]
                    )
                if inputs_table:
                    doc.add_header(4, "Parameters")
                    doc.add_table(["Name", "Type", "Description"], inputs_table)

                if abi_element.get("stateMutability") in ("view", "pure"):
                    devdoc_returns = devdoc_element.get("returns", {})
                    if not devdoc_returns:
                        logger.warning("%s is missing @returns", signature)

                    outputs_table = []
                    for i, abi_output in enumerate(abi_element.get("outputs", [])):
                        output_name = abi_output["name"] or f"_{i}"
                        outputs_table.append(
                            [
                                abi_output["name"],
                                abi_output["type"],
                                devdoc_returns.get(output_name, ""),
                            ]
                        )
                    if outputs_table:
                        doc.add_header(4, "Returns")
                        doc.add_table(["Name", "Type", "Description"], outputs_table)

    output_file = paths.get_output_file_path(config["display_name"])

    footer_attrs = [f'version="{paths.get_document_version()}"']
    if prev_config:
        link = path.relpath(
            paths.get_output_file_path(prev_config["display_name"]),
            path.dirname(output_file),
        )
        footer_attrs.append(
            f'prev-url="{link}" prev-contract="{prev_config["display_name"]}"'
        )
    if next_config:
        link = path.relpath(
            paths.get_output_file_path(next_config["display_name"]),
            path.dirname(output_file),
        )
        footer_attrs.append(
            f'next-url="{link}" next-contract="{next_config["display_name"]}"'
        )
    doc.add_macro("{.footer " + " ".join(footer_attrs) + "}")

    doc.write_to_file(output_file)
    logger.info("Generated %s", output_file)


def filter_natspec_by_type(element_type: ElementType, natspec: dict) -> dict:
    natspec_key = {ElementType.FUNCTION: "methods", ElementType.EVENT: "events"}[
        element_type
    ]
    return natspec.get(natspec_key, {})


def src_definition_regexp(
    abi_element: dict,
    element_type: ElementType,
) -> re.Pattern:
    name = abi_element["name"]
    parameter_types = [
        abi_type_to_sol_type_regexp(input["internalType"])
        for input in abi_element.get("inputs", [])
    ]

    # Match e.g. `vote(uint256 _commit, int256[] memory _reports, uint256 _salt )`
    sep = r"[\s\n]*"
    signature = rf"{name}{sep}\({sep}" + rf".+,{sep}".join(parameter_types) + r".+\)"

    regexp_for_element_type = {
        ElementType.EVENT: f"event{sep}{signature}",
        # A contract function is either a Solidity `function` or an auto-generated
        # accessor function for a public contract property
        ElementType.FUNCTION: f"(function{sep}{signature}|public[^;]+{name}{sep}[;=])",
    }[element_type]
    return re.compile(regexp_for_element_type, re.MULTILINE | re.DOTALL)


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
