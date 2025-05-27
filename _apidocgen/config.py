"""Configuration schema and validation."""

import toml
from schema import Optional, Schema, SchemaError  # type: ignore

CONFIG_SCHEMA = Schema(
    {
        "autonity": {
            "src_dir": str,
            "github_url": str,
        },
        "contracts": {
            "output_dir": str,
            str: {
                Optional("display_name"): str,
                Optional("excludes"): [str],
            },
        },
    }
)


def load_toml(file: str) -> dict:
    with open(file) as f:
        return toml.load(f)


def validate_config(config: dict) -> None:
    try:
        CONFIG_SCHEMA.validate(config)
    except SchemaError as err:
        # Hide "During handling of the above exception, another exception occurred"
        raise SchemaError(f"Invalid configuration\n{err}") from None
