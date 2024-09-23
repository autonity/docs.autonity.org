"""Markdown documentation generator."""

import os
from os import path


class MarkdownDocument:
    _text = ""

    @staticmethod
    def format_link(text: str, url: str) -> str:
        return f"[{text}]({url})"

    @staticmethod
    def format_header(level: int, text: str) -> str:
        return "#" * level + " " + text + "\n"

    @staticmethod
    def format_macro(text: str) -> str:
        return "::: " + text + "\n:::\n"

    def add_meta(self, metadata: dict[str, str]) -> None:
        self._text += (
            "---\n"
            + "\n".join(f'{key}: "{value}"' for key, value in metadata.items())
            + "\n---\n\n"
        )

    def add_header(self, level: int, text: str) -> None:
        self._text += self.format_header(level, text) + "\n"

    def add_paragraph(self, text: str) -> None:
        self._text += text + "\n\n"

    def add_macro(self, text: str) -> None:
        self._text += self.format_macro(text) + "\n"

    def add_table(
        self,
        col_names: list[str],
        rows: list[list[str]],
        remove_empty_cols: bool = True,
    ) -> None:
        assert all(
            len(col_names) == len(row) for row in rows
        ), "All table rows must have the same number of columns"

        if remove_empty_cols:
            for c in range(len(col_names) - 1, -1, -1):
                if not any(row[c] for row in rows):
                    col_names = [col_names[i] for i in range(len(col_names)) if c != i]
                    for r in range(len(rows)):
                        rows[r] = [rows[r][i] for i in range(len(rows[r])) if c != i]

        self._text += "| " + " | ".join(col_names) + " |\n"
        self._text += "| --- " * len(col_names) + "|\n"
        for row in rows:
            self._text += "| " + " | ".join(row) + " |\n"
        self._text += "\n"

    def write_to_file(self, file: str) -> None:
        os.makedirs(path.dirname(file), exist_ok=True)
        with open(file, "w") as f:
            f.write(self._text.strip())
