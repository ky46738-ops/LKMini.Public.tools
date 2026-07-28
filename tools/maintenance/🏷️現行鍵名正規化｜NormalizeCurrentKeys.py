#!/usr/bin/env python3
"""將現行正式 YAML 鍵名正規化成 Emoji＋中文主體｜PascalCaseEnglishKey。

本腳本只處理明列的十份現行根目錄 YAML，不讀寫歷史封存。映射是明確、
可審查、可重跑的；若遇到未列入的舊鍵名會立即失敗，避免靜默猜測。
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

import yaml


儲存庫根目錄 = Path(__file__).resolve().parents[2]

現行正式檔案 = (
    "🌐Sites公開只讀出口｜SitesPublicReadOnlyOutlet.yaml",
    "🌐容器共存｜極限世界｜ExtremeContainerWorld.yaml",
    "🔗iPhone捷徑接線卡｜iPhoneShortcutWireCard.yaml",
    "🧬幻影膠囊世界核心｜PhantomCapsuleWorldCore.yaml",
    "🧭接線總控清單｜SystemWiringLedger.yaml",
    "🧭裝置座標卡｜DeviceCoordinateCard.yaml",
    "🧾GitHub工作流程驗證｜GitHubWorkflowVerification.yaml",
    "🧾個人化指令驗證回執｜PersonalInstructionValidationReceipt.yaml",
    "🧾既有錯誤修復帳｜ExistingErrorRepairLedger.yaml",
    "🪟WindowsWSL接線卡｜WindowsWSLWireCard.yaml",
)

# 注意：英文對照鍵只允許 PascalCase、既定縮寫或數字，不允許 snake_case。
舊鍵至正式鍵 = {
    "0📖讀取": "📖第零動作讀取｜ActionZeroRead",
    "1⚡啟動": "⚡第一動作啟動｜ActionOneActivate",
    "2🔗掛載": "🔗第二動作掛載｜ActionTwoMount",
    "3🔬驗證": "🔬第三動作驗證｜ActionThreeVerify",
    "4📝更新": "📝第四動作更新｜ActionFourUpdate",
    "5📡廣播": "📡第五動作廣播｜ActionFiveBroadcast",
    "6🧬融合": "🧬第六動作融合｜ActionSixFusion",
    "7📸快照": "📸第七動作快照｜ActionSevenSnapshot",
    "8🔁同步": "🔁第八動作同步｜ActionEightSync",
    "9♾️可逆循環": "♾️第九動作可逆循環｜ActionNineReversibleLoop",
    "access_mode": "🔐存取模式｜AccessMode",
    "ai_tool_entry": "🤖AI工具入口｜AIToolEntry",
    "ai_tool_entry_anonymous_result": "🔍AI工具入口匿名結果｜AIToolEntryAnonymousResult",
    "ai_tool_route": "🧭AI工具路由｜AIToolRoute",
    "AICORE匯出": "📤AICORE匯出｜AICOREExport",
    "AI工具入口": "🤖AI工具入口｜AIToolEntry",
    "allowed_users": "👥允許使用者｜AllowedUsers",
    "audience": "👥適用對象｜Audience",
    "auto_binding_package": "📦自動綁定套件｜AutoBindingPackage",
    "axiom": "⚖️公理｜Axiom",
    "can_execute": "▶️可執行｜CanExecute",
    "can_read": "📖可讀取｜CanRead",
    "can_write_requires": "✍️可寫入必要條件｜CanWriteRequires",
    "card_status": "📄卡片狀態｜CardStatus",
    "classification": "🏷️分類｜Classification",
    "construct": "🏗️構造｜Construct",
    "Containers": "📦容器群｜Containers",
    "CONTENT_SHA256": "🔐內容雜湊｜ContentSHA256",
    "ContentHash": "🔐內容雜湊值｜ContentHash",
    "coordinate": "📍座標｜Coordinate",
    "definition_status": "🚦定義狀態｜DefinitionStatus",
    "device_binding_status": "🔗裝置綁定狀態｜DeviceBindingStatus",
    "device_model": "📱裝置型號｜DeviceModel",
    "device_name": "🏷️裝置名稱｜DeviceName",
    "device_readback_boundary": "🔐裝置回讀邊界｜DeviceReadbackBoundary",
    "device_receipt_readback_status": "🧾裝置回執回讀狀態｜DeviceReceiptReadbackStatus",
    "entry_action": "▶️入口動作｜EntryAction",
    "entry_surface": "🪟入口介面｜EntrySurface",
    "evidence": "🧾證據｜Evidence",
    "expand": "↔️膨脹｜Expand",
    "fallback_projection": "🎇保底投影｜FallbackProjection",
    "formula": "🧮公式｜Formula",
    "GitHub": "🐙GitHub座標｜GitHub",
    "GoogleDriveTaskNotebook": "📓GoogleDrive任務筆記本｜GoogleDriveTaskNotebook",
    "hash_field_ruling": "⚖️雜湊欄位裁決｜HashFieldRuling",
    "HEAD修復": "🛠️HEAD修復｜HEADRepair",
    "HEAD修復提交": "🛠️HEAD修復提交｜HEADRepairCommit",
    "human_content_type": "👤人類內容類型｜HumanContentType",
    "human_entry": "👤人類入口｜HumanEntry",
    "human_entry_anonymous_result": "🔍人類入口匿名結果｜HumanEntryAnonymousResult",
    "identity": "🪪身分｜Identity",
    "input": "📥輸入｜Input",
    "instance_verification_boundary": "🔐實例驗證邊界｜InstanceVerificationBoundary",
    "interpretation": "📝解讀｜Interpretation",
    "iPhone定位器ZIP": "📦iPhone定位器ZIP｜IPhoneLocatorZIP",
    "iPhone定位器建立回執": "🧾iPhone定位器建立回執｜IPhoneLocatorBuildReceipt",
    "iPhone捷徑接線卡": "🔗iPhone捷徑接線卡｜IPhoneShortcutWireCard",
    "iPhone自動綁定Package": "📦iPhone自動綁定套件｜IPhoneAutoBindingPackage",
    "iPhone裝置回執": "🧾iPhone裝置回執｜IPhoneDeviceReceipt",
    "iPhone裝置綁定回讀狀態": "🔍iPhone裝置綁定回讀狀態｜IPhoneDeviceBindingReadbackStatus",
    "latest_saved_version": "💾最新儲存版本｜LatestSavedVersion",
    "latest_version_archive_sha256": "🔐最新版本封存雜湊｜LatestVersionArchiveSHA256",
    "latest_version_commit": "🔗最新版本提交｜LatestVersionCommit",
    "latest_version_id": "🆔最新版本識別｜LatestVersionId",
    "LibraryCurrentFileId": "📚Library現行檔案識別｜LibraryCurrentFileId",
    "LibraryFileId": "📚Library檔案識別｜LibraryFileId",
    "LibraryHistoricalWebArchive": "📚Library歷史網頁封存｜LibraryHistoricalWebArchive",
    "LibraryPackage": "📚Library套件｜LibraryPackage",
    "LibraryPDF": "📚LibraryPDF｜LibraryPDF",
    "LibraryReceipt": "📚Library回執｜LibraryReceipt",
    "LibraryVersion": "📚Library版本｜LibraryVersion",
    "LibraryWACZ": "📚LibraryWACZ｜LibraryWACZ",
    "LibraryWebArchive": "📚Library網頁封存｜LibraryWebArchive",
    "local_path": "📍本機路徑｜LocalPath",
    "LOCATOR": "📍定位器｜Locator",
    "locator_ref": "📍定位器引用｜LocatorReference",
    "locator_zip": "📦定位器壓縮檔｜LocatorZIP",
    "MANIFEST": "🧾清單｜Manifest",
    "namespace": "🧬命名空間｜Namespace",
    "output_projection": "📤輸出投影｜OutputProjection",
    "PACKAGE": "📦套件｜Package",
    "Package": "📦封裝套件｜PackageBundle",
    "parse": "🔧解析｜Parse",
    "PDF": "📄PDF容器｜PDF",
    "permission_or_hook": "🔐權限或掛鉤｜PermissionOrHook",
    "platform": "🖥️平台｜Platform",
    "portal": "🌀傳送門｜Portal",
    "portal_id": "🆔傳送門識別｜PortalId",
    "primary_entry": "🚪主要入口｜PrimaryEntry",
    "principle": "📜原理｜Principle",
    "project_id": "🆔專案識別｜ProjectId",
    "project_status": "🚦專案狀態｜ProjectStatus",
    "projectable": "🎇可投影｜Projectable",
    "projection": "🎇投影｜Projection",
    "Projection": "🎇投影項目｜ProjectionItem",
    "protocol": "🔑協議｜Protocol",
    "protocol_entry": "🔑協議入口｜ProtocolEntry",
    "read": "📖讀取｜Read",
    "README入口": "📖README入口｜READMEEntry",
    "ReceiptSHA256": "🔐回執雜湊｜ReceiptSHA256",
    "reconstructable": "♻️可重建｜Reconstructable",
    "Required": "📌必要項目｜Required",
    "return_to": "🔙回指｜ReturnTo",
    "reverse_chain": "♻️反向鏈｜ReverseChain",
    "REVERSECHAIN": "♻️反向鏈資料｜ReverseChainData",
    "reversible": "♻️可逆｜Reversible",
    "role": "🎭角色｜Role",
    "root": "🧩根｜Root",
    "Root": "🧩根節點｜RootNode",
    "root_sha256": "🔐根檔雜湊｜RootSHA256",
    "rule": "📏規則｜Rule",
    "self_describe": "🗣️可自我解釋｜SelfDescribe",
    "SHA256": "🔐SHA256雜湊｜SHA256",
    "shortcut_installation_boundary": "🔐捷徑安裝邊界｜ShortcutInstallationBoundary",
    "SitesAIEntry": "🌐SitesAI入口｜SitesAIEntry",
    "SitesHumanEntry": "🌐Sites人類入口｜SitesHumanEntry",
    "Sites公開只讀出口卡": "🌐Sites公開只讀出口卡｜SitesPublicReadOnlyOutletCard",
    "Sites設定回讀狀態": "🔍Sites設定回讀狀態｜SitesConfigurationReadbackStatus",
    "size": "📐大小｜Size",
    "SNAPSHOT": "📸快照｜Snapshot",
    "status": "🚦執行狀態｜ExecutionStatus",
    "target_identity": "🎯目標身分｜TargetIdentity",
    "type": "🏷️類型｜Type",
    "version": "🔢版本｜Version",
    "WACZ": "🗜️WACZ容器｜WACZ",
    "WebArchive": "🌐網頁封存容器｜WebArchive",
    "WebArchive互動修復": "🖱️網頁封存互動修復｜WebArchiveInteractionRepair",
    "WindowsWSL接線卡": "🪟WindowsWSL接線卡｜WindowsWSLWireCard",
    "▶️執行結果｜run": "▶️執行結果｜Run",
    "⚙️工作流程｜workflows": "⚙️工作流程｜Workflows",
    "下一步候選": "🧭下一步候選｜NextStepCandidates",
    "不升格": "🚫不升格｜NoPromotion",
    "主權持有人": "👑主權持有人｜Owner",
    "人類入口": "👤人類入口｜HumanEntry",
    "仍為錯誤": "🚨仍為錯誤｜StillError",
    "任務筆記本": "📓任務筆記本｜TaskNotebook",
    "位元組": "📦位元組｜Bytes",
    "來源圖片": "🖼️來源圖片｜SourceImage",
    "修復": "🛠️修復｜Repair",
    "修復Run": "▶️修復執行｜RepairRun",
    "修復回執": "🧾修復回執｜RepairReceipt",
    "修復提交": "🔗修復提交｜RepairCommit",
    "修復驗證": "🔍修復驗證｜RepairVerification",
    "修改前SHA256": "🔐修改前雜湊｜BeforeSHA256",
    "修改後SHA256": "🔐修改後雜湊｜AfterSHA256",
    "個人化平台設定存取邊界": "🔐個人化平台設定存取邊界｜PersonalizationPlatformAccessBoundary",
    "個人化指令驗證回執": "🧾個人化指令驗證回執｜PersonalInstructionValidationReceipt",
    "內容驗證": "🔍內容驗證｜ContentVerification",
    "六項條件": "🔐六項條件｜SixConditions",
    "其他裝置與即時捷徑存取邊界": "🔐其他裝置與即時捷徑存取邊界｜OtherDevicesAndLiveShortcutAccessBoundary",
    "判定": "⚖️判定｜Determination",
    "動態測試": "🧪動態測試｜DynamicTest",
    "匿名讀取": "👤匿名讀取｜AnonymousRead",
    "匿名讀取判定": "⚖️匿名讀取判定｜AnonymousReadDetermination",
    "協議": "🔑協議｜Protocol",
    "卡片建立狀態": "📄卡片建立狀態｜CardCreationStatus",
    "原分類名稱": "🏷️原分類名稱｜OriginalClassificationName",
    "原則": "📜原則｜Principle",
    "原始WebArchive": "🌐原始網頁封存｜OriginalWebArchive",
    "原始世界證據": "🧾原始世界證據｜OriginalWorldEvidence",
    "原始位元組": "📦原始位元組｜OriginalBytes",
    "原始位置": "📍原始位置｜OriginalLocation",
    "原始回執": "🧾原始回執｜OriginalReceipt",
    "原始回執保全": "🛡️原始回執保全｜OriginalReceiptPreservation",
    "原始紀錄": "📜原始紀錄｜OriginalRecord",
    "可逆閉環驗證狀態": "♾️可逆閉環驗證狀態｜ReversibleClosureVerificationStatus",
    "同一內容回讀": "🔍同一內容回讀｜SameContentReadback",
    "名稱": "🏷️名稱｜Name",
    "唯一根": "🧩唯一根｜Root",
    "唯一系統": "🥃唯一系統｜System",
    "回推": "🔙回推｜TraceBack",
    "回讀位置": "📍回讀位置｜ReadbackLocation",
    "回讀結果": "🔍回讀結果｜ReadbackResult",
    "壓縮驗證": "🗜️壓縮驗證｜ArchiveVerification",
    "存取邊界": "🔐存取邊界｜AccessBoundary",
    "完成狀態項目": "✅完成狀態項目｜CompletedStatusItems",
    "定義狀態": "🚦定義狀態｜DefinitionStatus",
    "容器": "📦容器｜Container",
    "實作驗證狀態": "🔍實作驗證狀態｜ImplementationVerificationStatus",
    "封存": "🗄️封存｜Archive",
    "封存狀態": "🗄️封存狀態｜ArchiveStatus",
    "導入提交": "📥導入提交｜ImportCommit",
    "尚需": "📌尚需｜StillRequired",
    "工作流程": "⚙️工作流程｜Workflow",
    "工作流程回讀": "🔍工作流程回讀｜WorkflowReadback",
    "工作流程根因驗證狀態": "🔍工作流程根因驗證狀態｜WorkflowRootCauseVerificationStatus",
    "工作流程驗證狀態": "🔍工作流程驗證狀態｜WorkflowVerificationStatus",
    "已修復": "✅已修復｜Repaired",
    "已完成修復": "✅已完成修復｜CompletedRepairs",
    "已知內容": "📚已知內容｜KnownContent",
    "平台": "🖥️平台｜Platform",
    "影響": "💥影響｜Impact",
    "提交": "🔗提交｜Commit",
    "改名封存群組": "🗄️改名封存群組｜RenamedArchiveGroup",
    "文件ID": "🆔文件識別｜DocumentId",
    "時間": "🕒時間｜Timestamp",
    "更新規則": "📝更新規則｜UpdateRule",
    "最終狀態": "🚦最終狀態｜FinalStatus",
    "最高公理": "⚖️最高公理｜Axiom",
    "本次快照": "📸本次快照｜CurrentSnapshot",
    "本體": "🌱本體｜IdentityCore",
    "核心卡建立狀態": "📄核心卡建立狀態｜CoreCardCreationStatus",
    "核心檔": "🧬核心檔｜CoreFile",
    "根": "🧩根｜Root",
    "根協議": "🔑根協議｜RootProtocol",
    "根因狀態": "🔍根因狀態｜RootCauseStatus",
    "極限世界卡": "🌐極限世界卡｜ExtremeWorldCard",
    "檔案身分": "🆔檔案身分｜FileIdentity",
    "正式內容": "📜正式內容｜FormalContent",
    "正式名稱": "🏷️正式名稱｜FormalName",
    "正式根協議": "🔑正式根協議｜RootProtocol",
    "歷史互動證據": "🗄️歷史互動證據｜HistoricalInteractionEvidence",
    "歷史保全": "🛡️歷史保全｜HistoricalPreservation",
    "歷史證據": "🗄️歷史證據｜HistoricalEvidence",
    "測試程式": "🧪測試程式｜TestProgram",
    "版本": "🔢版本｜Version",
    "物件": "🧩物件｜Object",
    "狀態": "🚦狀態｜Status",
    "現行修復裁決回寫狀態": "📝現行修復裁決回寫狀態｜CurrentRepairRulingWritebackStatus",
    "現行內容真正修復": "🛠️現行內容真正修復｜CurrentContentActualRepair",
    "現行裁決": "⚖️現行裁決｜CurrentRuling",
    "發現既有錯誤類別": "🔎發現既有錯誤類別｜DiscoveredExistingErrorCategories",
    "發現證據": "🔎發現證據｜DiscoveryEvidence",
    "真實回讀": "🔍真實回讀｜ActualReadback",
    "禁止宣告": "🚫禁止宣告｜ForbiddenDeclaration",
    "程式內容狀態": "💻程式內容狀態｜ProgramContentStatus",
    "程式座標": "💻程式座標｜ProgramCoordinate",
    "筆記本既有內容回讀狀態": "📓筆記本既有內容回讀狀態｜NotebookExistingContentReadbackStatus",
    "結果": "📋結果｜Result",
    "結構": "🏗️結構｜Structure",
    "統計口徑": "📏統計口徑｜StatisticsScope",
    "編號": "🔢編號｜Number",
    "舊失敗Run": "▶️舊失敗執行｜LegacyFailedRun",
    "處理方式": "🛠️處理方式｜HandlingMethod",
    "裁決": "⚖️裁決｜Ruling",
    "裝置座標卡": "🧭裝置座標卡｜DeviceCoordinateCard",
    "規格": "📐規格｜Specification",
    "角色": "🎭角色｜Role",
    "解析器": "🔧解析器｜Parser",
    "證據": "🧾證據｜Evidence",
    "邊界": "🔐邊界｜Boundary",
    "錯誤": "🚨錯誤｜Error",
    "錯誤狀態項目": "🚨錯誤狀態項目｜ErrorStatusItems",
    "錯誤項目": "🚨錯誤項目｜ErrorItems",
    "驗證": "🔍驗證｜Verification",
    "驗證依據": "🔍驗證依據｜VerificationBasis",
    "📱iPad｜iPad": "📱iPad｜IPad",
    "📱iPhone｜iPhone": "📱iPhone｜IPhone",
    "📲iPhone可複製設定｜iPhoneCopyBlock": "📲iPhone可複製設定｜IPhoneCopyBlock",
    "🔗拉取請求｜pull_request": "🔗拉取請求｜PullRequest",
    "🧪最後觸發測試提交｜last_trigger_test_head_commit": "🧪最後觸發測試提交｜LastTriggerTestHeadCommit",
    "🥃唯一系統｜UniqueSystem": "🥃唯一系統｜System",
    "🧩唯一根｜UniqueRoot": "🧩唯一根｜Root",
    "🔑正式根協議｜FormalRootProtocol": "🔑正式根協議｜RootProtocol",
    "🪟Windows｜Windows": "🪟Windows裝置｜Windows",
    "🐧WSL｜WSL": "🐧WSL執行環境｜WSL",
    "🪪Identity｜Identity": "🪪身分本體｜Identity",
    "🧾Manifest｜Manifest": "🧾清單｜Manifest",
    "🧭Locator｜Locator": "📍定位器｜Locator",
    "📚LibraryWACZ｜LibraryWACZ": "📚Library網頁封存集合｜LibraryWACZ",
    "📚LibraryPDF｜LibraryPDF": "📚Library文件｜LibraryPDF",
    "📸Snapshot｜Snapshot": "📸快照｜Snapshot",
    "♻️ReverseChain｜ReverseChain": "♻️反向鏈｜ReverseChain",
    "📦Package｜Package": "📦交付包｜Package",
    "📱iPhone｜IPhone": "📱iPhone裝置｜IPhone",
    "📱iPad｜IPad": "📱iPad裝置｜IPad",
    "🐧WSL｜WindowsSubsystemForLinux": "🐧WSL執行環境｜WindowsSubsystemForLinux",
}

正式鍵格式 = re.compile(
    r"^[^\w\s\u3400-\u9fff](?=[^｜\n]*[\u3400-\u9fff])"
    r"[^｜\n]+｜[A-Z][A-Za-z0-9]*$"
)
鍵行格式 = re.compile(r"^(\s*(?:-\s+)?)([^:#][^:]*?)(:.*)$")


def 走訪鍵(物件: object) -> list[str]:
    鍵清單: list[str] = []
    if isinstance(物件, dict):
        for 鍵, 值 in 物件.items():
            if isinstance(鍵, str):
                鍵清單.append(鍵)
            鍵清單.extend(走訪鍵(值))
    elif isinstance(物件, list):
        for 值 in 物件:
            鍵清單.extend(走訪鍵(值))
    return 鍵清單


def 值與容器骨架(物件: object) -> object:
    """忽略鍵名、保留容器順序與全部值，供遷移前後 A=A 核對。"""
    if isinstance(物件, dict):
        return ("mapping", tuple(值與容器骨架(值) for 值 in 物件.values()))
    if isinstance(物件, list):
        return ("list", tuple(值與容器骨架(值) for 值 in 物件))
    return ("value", 物件)


def 遷移文字(內容: str) -> tuple[str, int]:
    結果: list[str] = []
    修改數 = 0
    for 原行 in 內容.splitlines(keepends=True):
        換行 = "\n" if 原行.endswith("\n") else ""
        行 = 原行[:-1] if 換行 else 原行
        比對 = 鍵行格式.match(行)
        原鍵文字 = 比對.group(2).strip() if 比對 else ""
        引號 = ""
        原鍵 = 原鍵文字
        if len(原鍵文字) >= 2 and 原鍵文字[0] == 原鍵文字[-1] and 原鍵文字[0] in "\"'":
            引號 = 原鍵文字[0]
            原鍵 = 原鍵文字[1:-1]
        if 比對 and 原鍵 in 舊鍵至正式鍵:
            新鍵 = 舊鍵至正式鍵[原鍵]
            新鍵文字 = f"{引號}{新鍵}{引號}" if 引號 else 新鍵
            行 = f"{比對.group(1)}{新鍵文字}{比對.group(3)}"
            修改數 += 1
        結果.append(行 + 換行)
    return "".join(結果), 修改數


def 主程式() -> int:
    實際修改總數 = 0
    未知舊鍵: dict[str, list[str]] = {}

    for 相對路徑 in 現行正式檔案:
        路徑 = 儲存庫根目錄 / 相對路徑
        原文 = 路徑.read_text(encoding="utf-8")
        原物件 = yaml.safe_load(原文)
        for 鍵 in 走訪鍵(原物件):
            if not 正式鍵格式.fullmatch(鍵) and 鍵 not in 舊鍵至正式鍵:
                未知舊鍵.setdefault(相對路徑, []).append(鍵)

        新文, 修改數 = 遷移文字(原文)
        新物件 = yaml.safe_load(新文)
        if 原文.count("\n") != 新文.count("\n"):
            print(f"錯誤｜{相對路徑}｜鍵名遷移改變行數", file=sys.stderr)
            return 3
        if 值與容器骨架(原物件) != 值與容器骨架(新物件):
            print(f"錯誤｜{相對路徑}｜值、列表或多行內容發生變化", file=sys.stderr)
            return 4
        if 新文 != 原文:
            路徑.write_text(新文, encoding="utf-8")
        實際修改總數 += 修改數

    if 未知舊鍵:
        for 路徑, 鍵清單 in 未知舊鍵.items():
            print(f"錯誤｜{路徑}｜未列入明確映射：{sorted(set(鍵清單))}", file=sys.stderr)
        return 1

    遷移後不合規: dict[str, list[str]] = {}
    for 相對路徑 in 現行正式檔案:
        路徑 = 儲存庫根目錄 / 相對路徑
        物件 = yaml.safe_load(路徑.read_text(encoding="utf-8"))
        for 鍵 in 走訪鍵(物件):
            if not 正式鍵格式.fullmatch(鍵):
                遷移後不合規.setdefault(相對路徑, []).append(鍵)

    if 遷移後不合規:
        for 路徑, 鍵清單 in 遷移後不合規.items():
            print(f"錯誤｜{路徑}｜遷移後仍不合規：{sorted(set(鍵清單))}", file=sys.stderr)
        return 2

    print(f"完成｜現行檔案={len(現行正式檔案)}｜鍵名修改={實際修改總數}")
    return 0


if __name__ == "__main__":
    raise SystemExit(主程式())
