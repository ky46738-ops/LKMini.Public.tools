from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT_NAME = "🗄️歷史錯誤紀錄｜HistoricalErrorRecords"
FORMAL_KEY_PATTERN = re.compile(
    r"^[^\w\s\u3400-\u9fff](?=[^｜\n]*[\u3400-\u9fff])"
    r"[^｜\n]+｜[A-Z][A-Za-z0-9]*$"
)


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
                self.assertIn(data.get("🚦狀態｜Status"), {"完成", "錯誤"})
                self.assertEqual(data.get("🧩唯一根｜Root"), "🧩LKMINI")
                self.assertEqual(data.get("🔑正式根協議｜RootProtocol"), "LKMINI://")

    def test_json_templates_are_valid_and_return_to_root(self) -> None:
        for name in ("LocatorTemplate.json", "ManifestTemplate.json"):
            path = ROOT / "PhantomCapsule" / name
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["🧩唯一根｜Root"], "🧩LKMINI")
            self.assertEqual(data["🔑正式根協議｜RootProtocol"], "LKMINI://")
            self.assertEqual(data["🔙回指｜ReturnTo"], "🧩LKMINI")
            self.assertEqual(data["🏷️物件分類｜ObjectClassification"], "範例定義")
            self.assertEqual(data["🚦狀態｜Status"], "完成")

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

    def test_verified_iphone_binding_is_not_reclassified_as_unverified(self) -> None:
        path = ROOT / "🧭裝置座標卡｜DeviceCoordinateCard.yaml"
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        iphone = data["📱iPhone裝置｜IPhone"]
        self.assertEqual(iphone["🔗裝置綁定狀態｜DeviceBindingStatus"], "完成")
        self.assertEqual(
            iphone["🧾裝置回執回讀狀態｜DeviceReceiptReadbackStatus"],
            "完成",
        )
        self.assertIn(
            "沒有捷徑安裝或即時執行回讀工具",
            iphone["🔐捷徑安裝邊界｜ShortcutInstallationBoundary"],
        )
        self.assertEqual(iphone["🔙回指｜ReturnTo"], "🧩LKMINI")
        self.assertEqual(len(iphone["🧾證據｜Evidence"]), 2)
        self.assertEqual(iphone["📦定位器壓縮檔｜LocatorZIP"]["📦位元組｜Bytes"], 1505)
        self.assertEqual(
            iphone["📦定位器壓縮檔｜LocatorZIP"]["🔐SHA256雜湊｜SHA256"],
            "3be6b2bd27e4e090a1fc2d693e9aa52a20a8918b5a44a5e747cbfebc05c172f4",
        )
        self.assertEqual(
            iphone["📦自動綁定套件｜AutoBindingPackage"]["📦位元組｜Bytes"],
            4985,
        )
        self.assertEqual(
            iphone["📦自動綁定套件｜AutoBindingPackage"]["🔐SHA256雜湊｜SHA256"],
            "977071bfb4c905cdccd07aecc95eb16742b8250d92aa190be0abfc8e70c368e5",
        )

    def test_container_projections_close_the_same_reversible_identity(self) -> None:
        path = ROOT / "🌐容器共存｜極限世界｜ExtremeContainerWorld.yaml"
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        self.assertEqual(data["🚦狀態｜Status"], "完成")
        self.assertEqual(data["♾️可逆閉環驗證狀態｜ReversibleClosureStatus"], "完成")
        self.assertEqual(
            data["🔐內容雜湊｜ContentSHA256"],
            "13d5392d542a11c0232b3d8abca09e7f786e9b76d31cdcb0c0f9cd08efcc9e4a",
        )
        verification = data["🧪實際位元組驗證｜ByteVerification"]
        self.assertEqual(
            verification["🌐網頁封存容器｜WebArchive"]["🚦狀態｜Status"],
            "完成",
        )
        self.assertEqual(
            verification["🌐網頁封存容器｜WebArchive"]["🔐SHA256雜湊｜SHA256"],
            "cbf46a50d299278c36b794f771998bf26c14913b97347042ca5104529267644a",
        )
        self.assertEqual(verification["🗜️WACZ容器｜WACZ"]["🚦狀態｜Status"], "完成")
        self.assertEqual(verification["📄PDF容器｜PDF"]["🚦狀態｜Status"], "完成")
        interaction = data["🖱️互動能力｜InteractionCapabilities"]
        self.assertEqual(
            interaction["🔍實作驗證狀態｜ImplementationVerificationStatus"],
            "完成",
        )
        self.assertEqual(
            interaction["🧪測試程式｜TestProgram"]["📋結果｜Result"],
            "完成",
        )
        package = data["📦交付包｜Package"]
        self.assertEqual(package["🚦狀態｜Status"], "完成")
        self.assertEqual(package["📦位元組｜Bytes"], 2320969)
        self.assertEqual(
            package["🔐SHA256雜湊｜SHA256"],
            "d3391e6b66f20b7be3b387f90feb977965da26b29b33165b1e16dacbab1b8122",
        )

    def test_access_boundaries_are_not_duplicated_as_current_errors(self) -> None:
        path = ROOT / "🧭接線總控清單｜SystemWiringLedger.yaml"
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        current_error_names = {
            item["🧩物件｜Object"] for item in data["🔐現行錯誤｜CurrentErrors"]
        }
        self.assertEqual(current_error_names, set())
        boundaries = data["🚧存取邊界｜AccessBoundaries"]
        self.assertEqual(
            set(boundaries),
            {
                "🌐Sites存取邊界｜Sites",
                "🧾ChatGPT個人化設定｜ChatGPTPersonalization",
                "📱裝置存取邊界｜Devices",
            },
        )
        self.assertIn(
            "🗄️GitHub封存儲存庫｜GitHubArchivedRepo",
            data["🗄️歷史封存證據｜HistoricalArchiveEvidence"],
        )

    def test_boundary_cards_are_complete_without_claiming_external_action(self) -> None:
        cards = (
            "🧭裝置座標卡｜DeviceCoordinateCard.yaml",
            "🔗iPhone捷徑接線卡｜iPhoneShortcutWireCard.yaml",
            "🪟WindowsWSL接線卡｜WindowsWSLWireCard.yaml",
            "🧾個人化指令驗證回執｜PersonalInstructionValidationReceipt.yaml",
        )
        for name in cards:
            with self.subTest(path=name):
                data = yaml.load(
                    (ROOT / name).read_text(encoding="utf-8"),
                    Loader=UniqueKeyLoader,
                )
                self.assertEqual(data["🚦狀態｜Status"], "完成")
                self.assertEqual(
                    data["🔐存取邊界記錄狀態｜AccessBoundaryRecordingStatus"],
                    "完成",
                )
                self.assertTrue(data["🚧存取邊界｜AccessBoundary"])

    def test_sites_card_matches_current_management_readback(self) -> None:
        path = ROOT / "🌐Sites公開只讀出口｜SitesPublicReadOnlyOutlet.yaml"
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        readback = data["🧾工具回讀｜ToolReadback"]
        self.assertEqual(readback["🚦專案狀態｜ProjectStatus"], "active")
        self.assertEqual(readback["🔐存取模式｜AccessMode"], "public")
        self.assertEqual(readback["👥允許使用者｜AllowedUsers"], 1)
        self.assertEqual(readback["💾最新儲存版本｜LatestSavedVersion"], 22)
        self.assertEqual(
            readback["🔐最新版本封存雜湊｜LatestVersionArchiveSHA256"],
            "26d54d9935efa35125c162c31eaaad096d5ba5b4332249a192b08e7d050b4876",
        )
        self.assertEqual(readback["🚦部署狀態｜DeploymentStatus"], "succeeded")
        self.assertEqual(readback["🛡️匿名寫入｜AnonymousWrite"], "HTTP 405")
        self.assertEqual(readback["🔢寫入前修訂｜RevisionBefore"], 13)
        self.assertEqual(readback["🔢寫入後修訂｜RevisionAfter"], 13)

    def test_all_current_yaml_and_json_keys_use_formal_names(self) -> None:
        def walk_keys(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    yield key
                    yield from walk_keys(child)
            elif isinstance(value, list):
                for child in value:
                    yield from walk_keys(child)

        paths = sorted(ROOT.glob("*.yaml"))
        paths.extend(sorted((ROOT / "PhantomCapsule").glob("*.json")))
        for path in paths:
            with self.subTest(path=path.name):
                if path.suffix == ".json":
                    data = json.loads(path.read_text(encoding="utf-8"))
                else:
                    data = yaml.load(
                        path.read_text(encoding="utf-8"),
                        Loader=UniqueKeyLoader,
                    )
                violations = [
                    key
                    for key in walk_keys(data)
                    if not isinstance(key, str) or not FORMAL_KEY_PATTERN.fullmatch(key)
                ]
                self.assertEqual(violations, [])

    def test_repair_ledger_statistics_match_item_statuses(self) -> None:
        path = ROOT / "🧾既有錯誤修復帳｜ExistingErrorRepairLedger.yaml"
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        items = data["🧾真正修復清單｜ActualRepairList"]
        completed = [
            item["🔢編號｜Number"]
            for item in items
            if item["🚦最終狀態｜FinalStatus"] == "完成"
        ]
        errors = [
            item["🔢編號｜Number"]
            for item in items
            if item["🚦最終狀態｜FinalStatus"] == "錯誤"
        ]
        stats = data["📊統計｜Statistics"]
        self.assertEqual(
            stats["🔎發現既有錯誤類別｜DiscoveredExistingErrorCategories"],
            len(items),
        )
        self.assertEqual(
            stats["🛠️現行內容真正修復｜CurrentContentActualRepair"],
            len(completed),
        )
        self.assertEqual(stats["✅完成狀態項目｜CompletedStatusItems"], len(completed))
        self.assertEqual(stats["🚨錯誤狀態項目｜ErrorStatusItems"], len(errors))
        self.assertEqual(stats["🚨錯誤項目｜ErrorItems"], errors)
        self.assertEqual(errors, [])

    def test_animation_projection_is_current_and_fully_checksummed(self) -> None:
        directory = ROOT / "automation" / "GitHubRepositoryAnimationSprite"
        required = {path.name for path in directory.iterdir() if path.is_file()}
        manifest = json.loads((directory / "MANIFEST.json").read_text(encoding="utf-8"))
        self.assertIsNone(manifest["version"])
        self.assertEqual(manifest["edition"], "正版")
        self.assertEqual(manifest["status"], "完成")
        self.assertFalse(
            manifest["official_release_policy"]["canonical_name_has_version_number"]
        )
        self.assertEqual(set(manifest["required"]), required)

        for name in (
            "AICORE.json",
            "CORRECTION.json",
            "EXECUTION_RECEIPT.json",
            "GITHUB_READBACK.json",
            "LOCATOR.json",
            "MANIFEST.json",
            "SNAPSHOT.json",
            "animation-data.json",
            "🪞幻影膠囊",
        ):
            data = json.loads((directory / name).read_text(encoding="utf-8"))
            self.assertIsNone(data["version"], name)
            self.assertEqual(data["edition"], "正版", name)
            self.assertEqual(data["status"], "完成", name)

        current_surface = (
            "README.md",
            "index.html",
            "animation.js",
            "animation.svg",
            "STORYBOARD.md",
            "SUBTITLES.vtt",
            "VOICEOVER.md",
        )
        version_pattern = re.compile(r"\\bv\\d+(?:\\.\\d+)*\\b")
        for name in current_surface:
            text = (directory / name).read_text(encoding="utf-8")
            self.assertIsNone(version_pattern.search(text), name)
        animation_data = json.loads(
            (directory / "animation-data.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            animation_data["current"]["writeback"],
            "🥃老K系統／🧩LKMINI／🪞幻影膠囊",
        )
        self.assertEqual(animation_data["metrics"]["repositories"], 23)
        self.assertEqual(animation_data["metrics"]["branches"], 107)

        seen = set()
        for line in (directory / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
            expected, name = line.split("  ", 1)
            self.assertNotIn(name, seen)
            seen.add(name)
            target = directory / name
            self.assertTrue(target.is_file(), name)
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), expected, name)
        self.assertEqual(seen, required - {"SHA256SUMS.txt"})


if __name__ == "__main__":
    unittest.main()
