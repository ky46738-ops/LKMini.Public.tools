#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔑 LKMINI 根協議解析器

所有正式路徑以 LKMINI:// 開始。
解析器只負責辨識根、解析路徑、名稱與虛擬副檔名，並回傳結構化結果。
規則與實際行為由外部系統能力承接。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from pathlib import PurePosixPath
from typing import Any

根協議檔頭 = "LKMINI://"


class 根協議錯誤(ValueError):
    """❌ 根協議解析錯誤。"""


@dataclass(frozen=True)
class 根協議解析結果:
    原始協議: str
    根: str
    上層路徑: str
    名稱: str
    虛擬副檔名: str


class LKMINI根協議解析器:
    """🔑 系統固定使用的根協議解析器。"""

    def 是根協議(self, 文字: str) -> bool:
        return isinstance(文字, str) and 文字.lstrip().startswith(根協議檔頭)

    def 解析(self, 協議文字: str) -> 根協議解析結果:
        if not isinstance(協議文字, str):
            raise 根協議錯誤("❌ 協議內容必須是文字")

        原始協議 = 協議文字.strip()
        if not 原始協議.startswith(根協議檔頭):
            raise 根協議錯誤(f"❌ 缺少根協議檔頭：{根協議檔頭}")

        主體 = 原始協議[len(根協議檔頭):].strip()
        if not 主體:
            raise 根協議錯誤("❌ 根協議缺少路徑")
        if "\\" in 主體:
            raise 根協議錯誤("❌ 路徑必須使用正斜線「/」")
        if "?" in 主體 or "#" in 主體:
            raise 根協議錯誤("❌ 根協議不接受查詢字串或 fragment")
        if 主體.startswith("/") or 主體.endswith("/") or "//" in 主體:
            raise 根協議錯誤("❌ 路徑包含無效節點")

        原始路徑部分 = 主體.split("/")
        if any(
            部分 in {"", ".", ".."} or 部分 != 部分.strip()
            for 部分 in 原始路徑部分
        ):
            raise 根協議錯誤("❌ 路徑包含無效節點")

        路徑 = PurePosixPath(*原始路徑部分)
        路徑部分 = 路徑.parts
        if tuple(原始路徑部分) != 路徑部分:
            raise 根協議錯誤("❌ 路徑正規化後不一致")

        最後節點 = 路徑部分[-1]
        if "." not in 最後節點:
            raise 根協議錯誤("❌ 缺少虛擬副檔名")

        名稱, 虛擬副檔名 = (項目.strip() for 項目 in 最後節點.rsplit(".", 1))
        if not 名稱 or not 虛擬副檔名:
            raise 根協議錯誤("❌ 名稱與虛擬副檔名都必須存在")

        return 根協議解析結果(
            原始協議=原始協議,
            根="🧩LKMINI",
            上層路徑="/".join(路徑部分[:-1]),
            名稱=名稱,
            虛擬副檔名=虛擬副檔名,
        )

    def 接管(self, 協議文字: str) -> dict[str, Any]:
        結果 = self.解析(協議文字)
        return {
            "🚦狀態｜Status": "✅ 解析完成",
            "🧩唯一根｜Root": "🧩LKMINI",
            "🔑正式根協議｜RootProtocol": 根協議檔頭,
            "🧾解析結果｜ParseResult": asdict(結果),
        }


def 主程式() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({
            "🚦狀態｜Status": "❌ 缺少協議",
            "📘使用方式｜Usage": "python 解析器.py LKMINI://路徑/名稱.虛擬副檔名",
        }, ensure_ascii=False, indent=2))
        return 1

    try:
        結果 = LKMINI根協議解析器().接管(sys.argv[1])
        print(json.dumps(結果, ensure_ascii=False, indent=2))
        return 0
    except 根協議錯誤 as 錯誤:
        print(json.dumps({
            "🚦狀態｜Status": "❌ 解析錯誤",
            "📝錯誤｜Error": str(錯誤),
        }, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(主程式())
