#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "docs" / "templates" / "_base"
WORD_MD = BASE_DIR / "base-template.word.md"
EXCEL_MD = BASE_DIR / "base-template.excel.md"
WORD_YAML = BASE_DIR / "base.word.yaml"
EXCEL_YAML = BASE_DIR / "base.excel.yaml"
RENDER_FILE = ROOT / "scripts" / "render_from_yaml.py"
STATE_FILE = BASE_DIR / ".sync_state.json"

AUTO_BLOCK_START = "# AUTO_SYNC_BASE_START"
AUTO_BLOCK_END = "# AUTO_SYNC_BASE_END"


def _require(pkg: str) -> None:
    raise RuntimeError(f"缺少依赖：{pkg}。请先安装 requirements.txt（或 pip install {pkg}）。")


try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_state() -> Dict[str, str]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: Dict[str, str]) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_word_headings(word_md: str) -> List[str]:
    return [m.group(1).strip() for m in re.finditer(r"^#{1,3}\s+(.+)$", word_md, flags=re.MULTILINE)]


def extract_excel_sheet_titles(excel_md: str) -> List[str]:
    out: List[str] = []
    for m in re.finditer(r"^##\s+Sheet:\s+(.+)$", excel_md, flags=re.MULTILINE):
        out.append(m.group(1).strip())
    return out


def build_base_word_yaml() -> Dict[str, Any]:
    # 与当前 base-template.word.md 对齐的规范（模板驱动；章节编号与 MD 手工模板一致）
    return {
        "template_type": "base-word",
        "version": "v0.1",
        "frontmatter_mapping": {
            "doc_id": "meta.doc_id",
            "title": "meta.title",
            "work_product_type": "meta.work_product_type",
            "iso_ref": "meta.iso_ref",
            "asil": "meta.asil",
            "status": "meta.status",
            "owner": "meta.owner",
            "reviewers": "meta.reviewers",
            "version": "meta.version",
            "baseline": "meta.baseline",
            "last_updated": "meta.last_updated",
        },
        "sections": [
            {
                "heading": "Change History（变更历史）",
                "heading_level": 2,
                "blocks": [
                    {
                        "subheading": "Document Change History（文档履历）",
                        "table": {
                            "columns": ["Version", "Status", "Author", "Date", "Approver", "Approve Date", "Description"],
                            "source": "base.change_history_document",
                            "mapping": {
                                "Version": "version",
                                "Status": "status",
                                "Author": "author",
                                "Date": "date",
                                "Approver": "approver",
                                "Approve Date": "approve_date",
                                "Description": "description",
                            },
                        },
                    },
                    {
                        "subheading": "Template Change History（文档模板履历）",
                        "table": {
                            "columns": ["Version", "Status", "Author", "Date", "Approver", "Approve Date", "Description"],
                            "source": "base.change_history_template",
                            "mapping": {
                                "Version": "version",
                                "Status": "status",
                                "Author": "author",
                                "Date": "date",
                                "Approver": "approver",
                                "Approve Date": "approve_date",
                                "Description": "description",
                            },
                        },
                    },
                ],
            },
            {
                "heading": "General Information（一般信息）",
                "blocks": [
                    {"subheading": "Document Purpose（文档目的）", "source": "base.purpose"},
                    {"subheading": "Document Scope（文档范围）", "source": "base.document_scope"},
                    {
                        "subheading": "Input Document（输入文档）",
                        "table": {
                            "columns": ["Document No.", "File name", "Version"],
                            "source": "base.input_documents",
                            "mapping": {"Document No.": "document_no", "File name": "file_name", "Version": "version"},
                        },
                    },
                    {
                        "subheading": "References（参考文档）",
                        "table": {
                            "columns": ["Document No.", "File name", "Version"],
                            "source": "base.references",
                            "mapping": {"Document No.": "document_no", "File name": "file_name", "Version": "version"},
                        },
                    },
                ],
            },
            {
                "heading": "Terms and Abbreviations（术语与缩略语）",
                "blocks": [
                    {
                        "subheading": "Terms （术语）",
                        "table": {
                            "columns": ["Term", "Definition", "Source"],
                            "source": "base.terms",
                            "mapping": {"Term": "term", "Definition": "definition", "Source": "source"},
                        },
                    },
                    {
                        "subheading": "Abbreviations（缩略语）",
                        "table": {
                            "columns": ["Term", "Definition"],
                            "source": "base.abbreviations",
                            "mapping": {"Term": "term", "Definition": "definition"},
                        },
                    },
                ],
            },
            {"heading": "正文内容（Main Content）", "content_placeholder": True},
        ],
    }


def build_base_excel_yaml() -> Dict[str, Any]:
    # 与当前 base-template.excel.md 对齐的规范（模板驱动）
    #
    # 说明：此函数的 sheet 命名应尽量与 base-template.excel.md 保持一致，
    # 以便模板说明一更新就能在输出中体现。
    return {
        "template_type": "base-excel",
        "version": "v0.1",
        "workbook": {
            "sheets": [
                {
                    "name": "Cover（封面）",
                    "kind": "key_value",
                    "rows": [
                        {"key": "title", "value_path": "meta.title"},
                    ],
                },
                {
                    "name": "Document Change History （文档履历）",
                    "kind": "table",
                    "columns": ["Version", "Status", "Author", "Date", "Approver", "Approve Date", "Description"],
                    "source": "base.change_history_document",
                    "mapping": {
                        "Version": "version",
                        "Status": "status",
                        "Author": "author",
                        "Date": "date",
                        "Approver": "approver",
                        "Approve Date": "approve_date",
                        "Description": "description",
                    },
                },
                {
                    "name": "Template Change History （模板履历）",
                    "kind": "table",
                    "columns": ["Version", "Status", "Author", "Date", "Approver", "Approve Date", "Description"],
                    "source": "base.change_history_template",
                    "mapping": {
                        "Version": "version",
                        "Status": "status",
                        "Author": "author",
                        "Date": "date",
                        "Approver": "approver",
                        "Approve Date": "approve_date",
                        "Description": "description",
                    },
                },
                {
                    "name": "General Information（一般信息）",
                    "kind": "table",
                    "columns": ["Document Purpose（文档目的）", "Document Scope（文档范围）"],
                    "source": "base.general_information",
                    "mapping": {"Document Purpose（文档目的）": "purpose", "Document Scope（文档范围）": "scope"},
                },
                {
                    "name": "Input （输入文档）",
                    "kind": "table",
                    "columns": ["Document No.", "File name", "Version"],
                    "source": "base.input_documents",
                    "mapping": {"Document No.": "document_no", "File name": "file_name", "Version": "version"},
                },
                {
                    "name": "References（参考文档）",
                    "kind": "table",
                    "columns": ["Document No.", "File name", "Version"],
                    "source": "base.references",
                    "mapping": {"Document No.": "document_no", "File name": "file_name", "Version": "version"},
                },
            ]
        },
    }


def dump_yaml(path: Path, data: Dict[str, Any]) -> None:
    if yaml is None:
        _require("pyyaml")
    text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    path.write_text(text, encoding="utf-8")


def update_render_autoblock(word_headings: List[str], excel_sheets: List[str]) -> None:
    text = load_text(RENDER_FILE)
    block = (
        f"{AUTO_BLOCK_START}\n"
        f"SYNC_BASE_WORD_TEMPLATE_MD = \"docs/templates/_base/base-template.word.md\"\n"
        f"SYNC_BASE_EXCEL_TEMPLATE_MD = \"docs/templates/_base/base-template.excel.md\"\n"
        f"SYNC_BASE_WORD_HEADINGS = {word_headings!r}\n"
        f"SYNC_BASE_EXCEL_SHEETS = {excel_sheets!r}\n"
        f"{AUTO_BLOCK_END}"
    )

    if AUTO_BLOCK_START in text and AUTO_BLOCK_END in text:
        text = re.sub(
            re.escape(AUTO_BLOCK_START) + r".*?" + re.escape(AUTO_BLOCK_END),
            block,
            text,
            flags=re.DOTALL,
        )
    else:
        # 插入到导入区域后
        anchor = "ROOT = Path(__file__).resolve().parents[1]"
        idx = text.find(anchor)
        if idx == -1:
            text = block + "\n\n" + text
        else:
            end = text.find("\n", idx)
            text = text[: end + 1] + "\n" + block + "\n" + text[end + 1 :]

    RENDER_FILE.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="自动同步基础模板：检查 base-template.word/excel.md 变更并更新 YAML 与渲染器硬编码元信息。"
    )
    parser.add_argument("--force", action="store_true", help="即使模板未变化也强制执行同步")
    parser.add_argument("--check", action="store_true", help="仅检查是否有变更，不写文件")
    args = parser.parse_args()

    if not WORD_MD.exists() or not EXCEL_MD.exists():
        raise RuntimeError("未找到基础模板说明文件（base-template.word.md / base-template.excel.md）")

    word_text = load_text(WORD_MD)
    excel_text = load_text(EXCEL_MD)

    current = {
        "word_md_sha256": sha256_text(word_text),
        "excel_md_sha256": sha256_text(excel_text),
    }
    last = load_state()
    changed = args.force or current != {k: last.get(k, "") for k in current.keys()}

    if args.check:
        if changed:
            print("[CHANGED] 基础模板说明文件有更新，需要同步。")
            return 1
        print("[OK] 基础模板说明文件无变化。")
        return 0

    if not changed:
        print("[SKIP] 基础模板说明文件无变化，未执行同步。")
        return 0

    # 提取元信息用于同步到硬编码文件
    word_headings = extract_word_headings(word_text)
    excel_sheets = extract_excel_sheet_titles(excel_text)

    # 更新 YAML 规范文件
    dump_yaml(WORD_YAML, build_base_word_yaml())
    dump_yaml(EXCEL_YAML, build_base_excel_yaml())

    # 更新 render_from_yaml.py 自动块（硬编码元信息）
    update_render_autoblock(word_headings, excel_sheets)

    # 记录状态
    save_state(current)
    print("[OK] 已同步 base.word.yaml / base.excel.yaml / render_from_yaml.py")
    print(f"[INFO] word headings: {len(word_headings)}, excel sheets: {len(excel_sheets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

