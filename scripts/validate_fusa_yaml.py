#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "work-products"
FORMATS_CONFIG = ROOT / "docs" / "templates" / "work-products" / "formats.yaml"


def _require(pkg: str) -> None:
    raise RuntimeError(f"缺少依赖：{pkg}。请先安装 requirements.txt（或 pip install {pkg}）。")


try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


RE_VERSION = re.compile(r"^v[0-9]+\.[0-9]+$")
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


REQUIRED_META = [
    "doc_id",
    "title",
    "work_product_type",
    "iso_ref",
    "asil",
    "status",
    "owner",
    "version",
    "last_updated",
]

REQUIRED_BASE_KEYS = [
    "purpose",
    "inputs_references",
    "standard_requirements",
    "project_assumptions",
    "traceability",
    "open_verification_items",
    "review_approval",
    "change_history",
]


def load_yaml(path: Path) -> Dict[str, Any]:
    if yaml is None:
        _require("pyyaml")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_formats_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise RuntimeError(f"缺少工作成果输出格式配置文件: {path}")
    return load_yaml(path)


def discover_yaml(target: Path) -> List[Path]:
    if target.is_file():
        return [target]
    return sorted(target.rglob("*.yaml"))


def validate_one(path: Path) -> List[str]:
    issues: List[str] = []
    doc = load_yaml(path)

    meta = doc.get("meta")
    base = doc.get("base")
    content = doc.get("content")

    if not isinstance(meta, dict):
        return ["缺少 meta（字典）"]
    if not isinstance(base, dict):
        return ["缺少 base（字典）"]
    if not isinstance(content, dict):
        issues.append("缺少 content（字典）")

    for k in REQUIRED_META:
        if k not in meta or str(meta.get(k, "")).strip() == "":
            issues.append(f"meta 缺少必填字段: {k}")

    if "iso_ref" in meta and not isinstance(meta["iso_ref"], list):
        issues.append("meta.iso_ref 必须为列表")

    if "version" in meta and isinstance(meta.get("version"), str) and not RE_VERSION.match(meta["version"]):
        issues.append("meta.version 格式应为 v<主>.<次>，例如 v1.0")

    if "last_updated" in meta and isinstance(meta.get("last_updated"), str) and not RE_DATE.match(meta["last_updated"]):
        issues.append("meta.last_updated 格式应为 YYYY-MM-DD")

    for k in REQUIRED_BASE_KEYS:
        if k not in base:
            issues.append(f"base 缺少关键段: {k}")

    wp_type = meta.get("work_product_type")
    try:
        cfg = load_formats_config(FORMATS_CONFIG)
        wpf = (cfg or {}).get("work_product_formats", {})
        if not isinstance(wpf, dict) or not wpf:
            issues.append("formats.yaml 缺少 work_product_formats 配置")
        elif wp_type not in wpf:
            issues.append(f"work_product_type 未在 formats.yaml 配置: {wp_type}")
    except Exception as e:
        issues.append(f"读取 formats.yaml 失败: {e}")

    if wp_type == "item-definition":
        if not isinstance(content, dict):
            return issues
        required_content = [
            "item_overview",
            "boundary_interfaces",
            "operating_scenarios",
            "dependencies_constraints",
            "known_failures_initial_concerns",
        ]
        for k in required_content:
            if k not in content:
                issues.append(f"content 缺少 item-definition 关键段: {k}")

    if wp_type == "hara":
        if not isinstance(content, dict):
            return issues
        required_content = [
            "analysis_scope",
            "hazards_and_events",
            "risk_assessment",
            "safety_goals",
            "assumptions_limits",
            "downstream_allocation",
        ]
        for k in required_content:
            if k not in content:
                issues.append(f"content 缺少 hara 关键段: {k}")

    return issues


def main() -> int:
    p = argparse.ArgumentParser(description="Validate FuSa YAML single-source documents.")
    p.add_argument("--target", default=str(DEFAULT_DATA_DIR), help="YAML file or directory. Default: data/work-products")
    args = p.parse_args()

    target = Path(args.target).resolve()
    files = discover_yaml(target)
    if not files:
        print(f"[INFO] 未发现 YAML: {target}")
        return 0

    failed = 0
    for f in files:
        issues = validate_one(f)
        if issues:
            failed += 1
            print(f"[FAIL] {f.relative_to(ROOT)}")
            for i in issues:
                print(f"  - {i}")
        else:
            print(f"[PASS] {f.relative_to(ROOT)}")

    if failed:
        print(f"\n校验失败: {failed}/{len(files)}")
        return 1
    print(f"\n全部通过: {len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

