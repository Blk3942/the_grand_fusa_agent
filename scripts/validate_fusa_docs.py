#!/usr/bin/env python3
"""Validate FuSa markdown documents against project structure rules."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
# 与 render_from_yaml.py 默认输出根目录一致（生成物 MD/DOCX 的唯一约定出口）
DEFAULT_DOCS_DIR = ROOT / "out"
RULES_PATH = ROOT / "docs" / "templates" / "schemas" / "document-structure-rules.json"


def load_rules(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    if not content.startswith("---\n"):
        return {}, content
    end = content.find("\n---\n", 4)
    if end == -1:
        return {}, content

    frontmatter_text = content[4:end]
    body = content[end + len("\n---\n") :]
    data: Dict[str, str] = {}
    current_key = None
    list_mode = False

    for raw_line in frontmatter_text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if list_mode and line.lstrip().startswith("- "):
            if current_key:
                data[current_key] = (data.get(current_key, "") + "\n" + line.lstrip()[2:]).strip()
            continue
        list_mode = False
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                data[key] = ""
                current_key = key
                list_mode = True
            else:
                data[key] = value
                current_key = key
    return data, body


def collect_h1_titles(body: str) -> List[str]:
    return [m.group(1).strip() for m in re.finditer(r"^#\s+(.+)$", body, flags=re.MULTILINE)]


def normalize_title(title: str) -> str:
    # Remove section index prefix like "1. ", "10.1 ", "A. ", but DO NOT
    # strip ordinary words (e.g. "Change History") which would break matching.
    normalized = re.sub(r"^\s*(?:\d+(?:\.\d+)*|[A-Z])[.)]?\s+", "", title.strip())
    return normalized.strip()


def has_keyword(body: str, keyword: str) -> bool:
    return keyword in body


def validate_file(path: Path, rules: Dict) -> List[str]:
    issues: List[str] = []
    content = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    if not frontmatter:
        issues.append("缺少 YAML front matter（--- 包裹）")
        return issues

    for key in rules["required_frontmatter_keys"]:
        if key not in frontmatter or not str(frontmatter[key]).strip():
            issues.append(f"front matter 缺少必填字段: {key}")

    h1_titles = collect_h1_titles(body)
    normalized_h1 = {normalize_title(t) for t in h1_titles}
    for required_h1 in rules["required_h1_sections_global"]:
        if required_h1 not in normalized_h1:
            issues.append(f"缺少基础章节 H1: {required_h1}")

    wp_type = frontmatter.get("work_product_type", "").strip()
    expected_keywords = rules.get("work_product_specific_keywords", {}).get(wp_type, [])
    for keyword in expected_keywords:
        if not has_keyword(body, keyword):
            issues.append(f"缺少工作成果专属内容关键词: {keyword}")

    return issues


def discover_docs(target: Path) -> List[Path]:
    if target.is_file():
        return [target]
    return sorted(target.rglob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate FuSa markdown docs structure.")
    parser.add_argument(
        "--target",
        default=str(DEFAULT_DOCS_DIR),
        help="Markdown file or directory to validate. Default: out/（与渲染输出根目录一致）",
    )
    parser.add_argument(
        "--rules",
        default=str(RULES_PATH),
        help="Rules JSON path. Default: docs/templates/schemas/document-structure-rules.json",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    rules_path = Path(args.rules).resolve()
    rules = load_rules(rules_path)

    docs = discover_docs(target)
    if not docs:
        print(f"[INFO] 未发现 Markdown 文档: {target}")
        return 0

    failed = 0
    for doc in docs:
        issues = validate_file(doc, rules)
        if issues:
            failed += 1
            print(f"[FAIL] {doc.relative_to(ROOT)}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"[PASS] {doc.relative_to(ROOT)}")

    if failed:
        print(f"\n校验失败: {failed}/{len(docs)}")
        return 1

    print(f"\n全部通过: {len(docs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
