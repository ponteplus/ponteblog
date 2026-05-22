#!/usr/bin/env python3
"""Atualiza a linha title: no front matter (evita sed com caracteres especiais)."""
import re
import sys


def yaml_double_quoted(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def main() -> None:
    if len(sys.argv) != 3:
        sys.stderr.write("uso: set-post-title.py <arquivo.md> <título>\n")
        sys.exit(1)

    path, title = sys.argv[1], sys.argv[2]
    new_line = f"title: {yaml_double_quoted(title)}\n"

    with open(path, encoding="utf-8") as f:
        content = f.read()

    content, count = re.subn(
        r"^title:.*$", new_line, content, count=1, flags=re.MULTILINE
    )
    if count != 1:
        sys.stderr.write(f"title: não encontrado em {path}\n")
        sys.exit(1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
