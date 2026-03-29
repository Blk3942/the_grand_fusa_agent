#!/usr/bin/env python3
"""Render .mmd (Mermaid) to .png.

优先级：
1) `npx @mermaid-js/mermaid-cli`（需本机 Node.js / npm）
2) 全局命令 `mmdc`（若已 npm install -g @mermaid-js/mermaid-cli）
3) HTTPS Kroki（需网络；部分环境可能被拦截）
4) `--offline-demo`：不解析 Mermaid，用 matplotlib 生成固定布局示意 PNG（需 pip install matplotlib）

示例：
  python scripts/render_mermaid.py -i path/to/diagram.mmd -o path/to/diagram.png
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_KROKI = "https://kroki.io/mermaid/png"


def _try_mermaid_cli(src: Path, dst: Path) -> bool:
    """Return True if PNG was written. Try npx mermaid-cli, then global mmdc."""
    src_s, dst_s = str(src), str(dst)
    candidates: list[tuple[list[str], Path | None]] = []

    npx = shutil.which("npx")
    if npx:
        candidates.append(
            (
                [
                    npx,
                    "--yes",
                    "@mermaid-js/mermaid-cli",
                    "-i",
                    src_s,
                    "-o",
                    dst_s,
                    "-b",
                    "transparent",
                ],
                ROOT,
            )
        )

    mmdc = shutil.which("mmdc")
    if mmdc:
        candidates.append(([mmdc, "-i", src_s, "-o", dst_s, "-b", "transparent"], None))

    for cmd, cwd in candidates:
        try:
            kw: dict = dict(check=True, capture_output=True, text=True, timeout=180)
            if cwd is not None:
                kw["cwd"] = str(cwd)
            subprocess.run(cmd, **kw)
            if dst.is_file() and dst.stat().st_size > 0:
                return True
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            continue
    return False


def _try_kroki(src: Path, dst: Path, kroki_url: str) -> bool:
    text = src.read_text(encoding="utf-8")
    req = Request(
        kroki_url,
        data=text.encode("utf-8"),
        headers={
            "Content-Type": "text/plain; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (compatible; FuSa-agent-render/1.0)",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=60) as resp:
            data = resp.read()
    except HTTPError:
        return False
    except URLError:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    return dst.is_file() and len(data) > 0


def render_mmd_to_png(src_mmd: Path, dst_png: Path, kroki_url: str = DEFAULT_KROKI) -> bool:
    """将 Mermaid 源文件渲染为 PNG。依次尝试本地 CLI 与 Kroki。成功返回 True。"""
    dst_png.parent.mkdir(parents=True, exist_ok=True)
    if _try_mermaid_cli(src_mmd, dst_png):
        return True
    if _try_kroki(src_mmd, dst_png, kroki_url):
        return True
    return False


def render_no_demo_offline_png(out: Path) -> None:
    """离线生成与 noa-architecture.mmd 意图一致的演示 PNG（matplotlib）。"""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    except ImportError as e:
        raise RuntimeError("离线演示需要 matplotlib：pip install matplotlib") from e

    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    def box(x, y, w, h, title, color="#E8F4FD"):
        p = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.15",
            linewidth=1.2,
            edgecolor="#333333",
            facecolor=color,
        )
        ax.add_patch(p)
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=9, wrap=True)

    # 布局：左→右 感知 / 地图 / NOA / 输出
    box(0.3, 6.5, 2.2, 2.8, "感知与融合\n摄像头 / 雷达\n→ 融合", "#E3F2FD")
    box(0.3, 2.0, 2.2, 2.8, "地图与导航\n定位 / 路线拓扑", "#E8F5E9")
    box(3.2, 4.0, 2.8, 3.5, "NOA 核心\nODD · 状态机\n运动规划", "#FFF3E0")
    box(6.8, 5.5, 2.6, 2.5, "HMI\n提示 / 接管", "#FCE4EC")
    box(6.8, 2.0, 2.6, 2.5, "域控 / 执行\n横纵向请求", "#F3E5F5")
    box(3.5, 0.4, 2.4, 1.2, "外部环境\n道路 / 交通", "#EEEEEE")

    arr = FancyArrowPatch((2.5, 7.8), (3.2, 6.5), arrowstyle="->", mutation_scale=12, color="#444")
    ax.add_patch(arr)
    arr2 = FancyArrowPatch((2.5, 3.5), (3.2, 4.8), arrowstyle="->", mutation_scale=12, color="#444")
    ax.add_patch(arr2)
    arr3 = FancyArrowPatch((6.0, 5.8), (6.8, 6.2), arrowstyle="->", mutation_scale=12, color="#444")
    ax.add_patch(arr3)
    arr4 = FancyArrowPatch((6.0, 5.2), (6.8, 3.8), arrowstyle="->", mutation_scale=12, color="#444")
    ax.add_patch(arr4)
    arr5 = FancyArrowPatch((4.5, 4.0), (4.5, 1.6), arrowstyle="->", mutation_scale=12, color="#888")
    ax.add_patch(arr5)

    ax.text(5, 9.5, "L2 NOA 逻辑架构示意图（离线演示）", ha="center", fontsize=12, fontweight="bold")

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> int:
    p = argparse.ArgumentParser(description="Render Mermaid .mmd to PNG.")
    p.add_argument("--input", "-i", required=True, type=Path, help="Input .mmd file")
    p.add_argument("--output", "-o", type=Path, help="Output .png path (default: next to input)")
    p.add_argument("--kroki-url", default=DEFAULT_KROKI, help="Kroki POST URL")
    p.add_argument(
        "--offline-demo",
        action="store_true",
        help="用 matplotlib 生成固定布局示意 PNG（不解析 Mermaid；需 matplotlib）",
    )
    args = p.parse_args()
    src = args.input.resolve()
    if not src.is_file():
        print(f"[ERROR] 找不到: {src}", file=sys.stderr)
        return 1
    out = args.output.resolve() if args.output else src.with_suffix(".png")

    if args.offline_demo:
        try:
            render_no_demo_offline_png(out)
            print(f"[OK] offline-demo -> {out}")
            return 0
        except RuntimeError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1

    if _try_mermaid_cli(src, out):
        print(f"[OK] mermaid-cli -> {out}")
        return 0
    if _try_kroki(src, out, args.kroki_url):
        print(f"[OK] kroki -> {out}")
        return 0

    print(
        "[WARN] mermaid-cli 与 Kroki 均不可用或失败。\n"
        f"       可手动: npx @mermaid-js/mermaid-cli -i \"{src}\" -o \"{out}\"\n"
        f"       或离线示意图: python scripts/render_mermaid.py -i \"{src}\" --offline-demo -o \"{out}\"",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
