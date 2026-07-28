from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT_NAME = "🗄️歷史錯誤紀錄｜HistoricalErrorRecords"


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise AssertionError(f"Duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping,
)


class CurrentRecordTests(unittest.TestCase):
    def test_current_yaml_is_parseable_and_uses_formal_root(self) -> None:
        current_files = [
            path
            for path in ROOT.glob("*.yaml")
            if ARCHIVE_ROOT_NAME not in path.parts
        ]
        self.assertGreaterEqual(len(current_files), 8)
        for path in current_files:
            with self.subTest(path=path.name):
                data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
                self.assertIn(data.get("狀態"), {"完成", "錯誤"})
                self.assertEqual(data.get("唯一根"), "🧩LKMINI")
                self.assertEqual(data.get("正式根協議"), "LKMINI://")

    def test_json_templates_are_valid_and_return_to_root(self) -> None:
        for name in ("LocatorTemplate.json", "ManifestTemplate.json"):
            path = ROOT / "PhantomCapsule" / name
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["🧩唯一根｜Root"], "🧩LKMINI")
            self.assertEqual(data["🔑正式根協議｜RootProtocol"], "LKMINI://")
            self.assertEqual(data["🔙回指｜ReturnTo"], "🧩LKMINI")

    def test_phantom_capsule_hashes_match_current_bytes(self) -> None:
        directory = ROOT / "PhantomCapsule"
        sums = directory / "SHA256SUMS.txt"
        for line in sums.read_text(encoding="utf-8").splitlines():
            expected, name = line.split("  ", 1)
            path = directory / name
            self.assertTrue(path.is_file(), name)
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(actual, expected, name)

    def test_current_phantom_capsule_does_not_reactivate_old_routes(self) -> None:
        excluded = {"CorrectionNotice.md", "PublicSpec.md"}
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "PhantomCapsule").iterdir()
            if path.is_file() and path.name not in excluded
        )
        self.assertNotIn("LOCATOR://", text)
        self.assertNotIn("06｜唯一出口", text)
        self.assertNotIn("Google Drive：唯一正本", text)

    def test_writing_app_is_offline_and_uses_safe_dom(self) -> None:
        text = (ROOT / "tools" / "writing-class" / "app.html").read_text(
            encoding="utf-8"
        )
        forbidden = (
            "innerHTML",
            "sendToMini",
            "@LKMINIBOT",
            "api.telegram.org",
            "fetch(",
            "XMLHttpRequest",
            "WebSocket",
            "sendBeacon",
        )
        for token in forbidden:
            self.assertNotIn(token, text)
        self.assertIn("Content-Security-Policy", text)
        self.assertIn("connect-src 'none'", text)
        self.assertIn("textContent", text)

    def test_root_index_targets_existing_files(self) -> None:
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        hrefs = re.findall(r'href="(\./[^"]+)"', text)
        self.assertGreaterEqual(len(hrefs), 2)
        for href in hrefs:
            target = ROOT / href.removeprefix("./")
            if href.endswith("/"):
                target = target / "index.html"
            self.assertTrue(target.is_file(), href)


if __name__ == "__main__":
    unittest.main()
