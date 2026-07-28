from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PARSER_PATH = REPOSITORY_ROOT / "🔑LKMINI根協議解析器｜LKMINIRootProtocolParser.py"
SPEC = importlib.util.spec_from_file_location("lkmini_root_protocol_parser", PARSER_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class LKMINIRootProtocolParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = MODULE.LKMINI根協議解析器()

    def test_parses_formal_path(self) -> None:
        result = self.parser.解析(
            "LKMINI://🧭裝置｜Devices/📱iPhone｜iPhone/🔗捷徑接線｜ShortcutWire.card"
        )
        self.assertEqual(result.根, "🧩LKMINI")
        self.assertEqual(
            result.上層路徑,
            "🧭裝置｜Devices/📱iPhone｜iPhone",
        )
        self.assertEqual(result.名稱, "🔗捷徑接線｜ShortcutWire")
        self.assertEqual(result.虛擬副檔名, "card")

    def test_structured_output_uses_formal_keys(self) -> None:
        result = self.parser.接管("LKMINI://🧪測試｜Tests/✅樣本｜Sample.card")
        self.assertEqual(result["🚦狀態｜Status"], "完成")
        self.assertEqual(result["🧩唯一根｜Root"], "🧩LKMINI")
        self.assertEqual(result["🔑正式根協議｜RootProtocol"], "LKMINI://")
        parsed = result["🧾解析結果｜ParseResult"]
        self.assertEqual(
            set(parsed),
            {
                "📝原始協議｜OriginalProtocol",
                "🧩解析根｜ParsedRoot",
                "🧭上層路徑｜ParentPath",
                "🏷️名稱｜Name",
                "📎虛擬副檔名｜VirtualExtension",
            },
        )
        self.assertEqual(
            parsed["📝原始協議｜OriginalProtocol"],
            "LKMINI://🧪測試｜Tests/✅樣本｜Sample.card",
        )
        self.assertEqual(parsed["🧩解析根｜ParsedRoot"], "🧩LKMINI")
        self.assertEqual(parsed["🧭上層路徑｜ParentPath"], "🧪測試｜Tests")
        self.assertEqual(parsed["🏷️名稱｜Name"], "✅樣本｜Sample")
        self.assertEqual(parsed["📎虛擬副檔名｜VirtualExtension"], "card")

    def test_rejects_invalid_paths_before_normalization(self) -> None:
        invalid = (
            "LKMINI://A//B.card",
            "LKMINI://A/./B.card",
            "LKMINI://A/../B.card",
            "LKMINI://A/B.card/",
            "LKMINI:///B.card",
            "LKMINI://A/B.card?x=1",
            "LKMINI://A/B.card#fragment",
            "LKMINI://A\\B.card",
            "LKMINI://A/B",
            "lkmini://A/B.card",
        )
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaises(MODULE.根協議錯誤):
                    self.parser.解析(value)


if __name__ == "__main__":
    unittest.main()
