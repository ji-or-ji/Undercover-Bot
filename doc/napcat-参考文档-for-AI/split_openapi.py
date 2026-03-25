from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


DEFAULT_SOURCE = Path(r"d:\Users\seewo\Desktop\Undercover-Bot\doc\napcat-参考文档-for-AI\OpenAPI.md")
DEFAULT_OUTPUT = Path(r"d:\Users\seewo\Desktop\Undercover-Bot\doc\napcat-参考文档-for-AI\OpenAPI")
INVALID_WINDOWS_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
HEADING_PATTERN = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*$")
FENCE_PATTERN = re.compile(r"^\s*(```|~~~)")
RESERVED_WINDOWS_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}


def normalize_heading_text(text: str) -> str:
    cleaned = re.sub(r"\s+#*$", "", text).strip()
    return cleaned if cleaned else "未命名"


def sanitize_segment(name: str) -> str:
    value = INVALID_WINDOWS_CHARS.sub(" ", name)
    value = re.sub(r"\s+", " ", value).strip().rstrip(".")
    if not value:
        value = "未命名"
    if value.upper() in RESERVED_WINDOWS_NAMES:
        value = f"{value}_"
    return value


def write_text(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding="utf-8", newline="\n")


def get_unique_name(base_name: str, used: dict[str, int]) -> str:
    index = used.get(base_name, 0) + 1
    used[base_name] = index
    if index == 1:
        return base_name
    return f"{base_name}_{index}"


def split_markdown(source: Path, output: Path, clean_output: bool) -> tuple[int, int]:
    lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
    preamble: list[str] = []
    h1_sections: list[dict] = []
    current_h1: dict | None = None
    current_h2: dict | None = None
    in_fence = False

    for line in lines:
        if FENCE_PATTERN.match(line):
            in_fence = not in_fence

        heading = HEADING_PATTERN.match(line) if not in_fence else None
        if heading:
            level = len(heading.group(1))
            title = normalize_heading_text(heading.group(2))
            if level == 1:
                current_h1 = {"title": title, "lines": [line], "h2": []}
                h1_sections.append(current_h1)
                current_h2 = None
                continue
            if level == 2:
                if current_h1 is None:
                    current_h1 = {"title": "未分类", "lines": ["# 未分类\n\n"], "h2": []}
                    h1_sections.append(current_h1)
                current_h1["lines"].append(line)
                current_h2 = {"title": title, "lines": [line]}
                current_h1["h2"].append(current_h2)
                continue

        if current_h1 is None:
            preamble.append(line)
            continue

        current_h1["lines"].append(line)
        if current_h2 is not None:
            current_h2["lines"].append(line)

    if clean_output and output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    write_text(output / "index.md", preamble)

    h1_dir_count = 0
    h2_dir_count = 0
    h1_name_count: dict[str, int] = {}

    for h1 in h1_sections:
        h1_name = get_unique_name(sanitize_segment(h1["title"]), h1_name_count)
        h1_dir = output / h1_name
        write_text(h1_dir / "index.md", h1["lines"])
        h1_dir_count += 1

        h2_name_count: dict[str, int] = {}
        for h2 in h1["h2"]:
            h2_name = get_unique_name(sanitize_segment(h2["title"]), h2_name_count)
            write_text(h1_dir / h2_name / "index.md", h2["lines"])
            h2_dir_count += 1

    return h1_dir_count, h2_dir_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--no-clean", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.source
    output = args.output

    if not source.exists():
        raise FileNotFoundError(f"源文件不存在: {source}")
    if source.resolve() == output.resolve():
        raise ValueError("输出目录不能与源文件相同")

    h1_count, h2_count = split_markdown(source, output, clean_output=not args.no_clean)
    print(f"完成拆分：# 级目录 {h1_count} 个，## 级目录 {h2_count} 个，输出目录：{output}")


if __name__ == "__main__":
    main()
