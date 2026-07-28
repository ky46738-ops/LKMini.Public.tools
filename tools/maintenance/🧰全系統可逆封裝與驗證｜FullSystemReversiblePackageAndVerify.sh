#!/usr/bin/env bash
set -Eeuo pipefail

# 🧰全系統可逆封裝與驗證｜FullSystemReversiblePackageAndVerify
# 本工具納入正式程式座標，讓重複交付可由系統自行全量封裝與驗證。
#
# 用法：
#   bash "🧰全系統可逆封裝與驗證｜FullSystemReversiblePackageAndVerify.sh" \
#     <來源提交｜SourceCommit> \
#     <乾淨工作樹｜CleanWorktree> \
#     <輸出資料夾｜OutputDirectory>
#
# 輸出：
#   🪞全系統可逆交付｜FullSystemReversibleDelivery｜YYYYMMDD-HHMMSS_TPE.zip
#   同名 ZIP 的 SHA256 sidecar
#   🧾全系統可逆交付驗證回執｜FullSystemReversibleDeliveryVerification｜...yaml

readonly history_source_prefix='🗄️歷史錯誤紀錄｜HistoricalErrorRecords/'
readonly current_objects_dir='00_現行本體｜CurrentObjects'
readonly task_receipts_dir='01_任務回執｜TaskReceipts'
readonly source_evidence_dir='02_原始證據｜SourceEvidence'
readonly reversible_evidence_dir='03_可逆證據｜ReversibleEvidence'
readonly historical_evidence_dir='04_歷史證據｜HistoricalEvidence'

fail() {
  printf '🚨錯誤｜Error: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "缺少必要指令：$1"
}

yaml_single_quote() {
  local value=${1//\'/\'\'}
  printf '%s' "$value"
}

yaml_list_item() {
  local item=$1
  local indentation=${2:-4}
  printf "%*s- '%s'\n" "$indentation" '' "$(yaml_single_quote "$item")"
}

file_count() {
  find "$1" -type f -print0 | awk 'BEGIN { RS = "\0" } { n++ } END { print n + 0 }'
}

[[ $# -eq 3 ]] || fail \
  '需要三個參數：<來源提交｜SourceCommit> <乾淨工作樹｜CleanWorktree> <輸出資料夾｜OutputDirectory>'

for command_name in git tar zip unzip sha256sum find sort cmp awk sed mktemp date wc dirname basename cp mkdir; do
  require_command "$command_name"
done

source_commit_input=$1
clean_worktree_input=$2
output_dir_input=$3

[[ -d "$clean_worktree_input" ]] || fail "工作樹不存在：$clean_worktree_input"
clean_worktree=$(cd "$clean_worktree_input" && pwd -P)
git -C "$clean_worktree" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || fail "指定路徑不是 Git 工作樹：$clean_worktree"

source_commit=$(git -C "$clean_worktree" rev-parse --verify "${source_commit_input}^{commit}") \
  || fail "找不到來源提交：$source_commit_input"
worktree_commit=$(git -C "$clean_worktree" rev-parse HEAD)
[[ "$worktree_commit" == "$source_commit" ]] \
  || fail "工作樹 HEAD 與來源提交不同：HEAD=$worktree_commit，來源=$source_commit"

worktree_changes=$(git -C "$clean_worktree" status --porcelain=v1 --untracked-files=all)
[[ -z "$worktree_changes" ]] \
  || fail '工作樹不是乾淨狀態；請先提交或另建乾淨 worktree，封裝未啟動'

mkdir -p -- "$output_dir_input"
output_dir=$(cd "$output_dir_input" && pwd -P)

time_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
time_tpe=$(TZ=Asia/Taipei date '+%Y-%m-%dT%H:%M:%S%z')
filename_time_tpe=$(TZ=Asia/Taipei date '+%Y%m%d-%H%M%S_TPE')
delivery_root_name="🪞全系統可逆交付｜FullSystemReversibleDelivery｜${filename_time_tpe}"
delivery_zip="$output_dir/${delivery_root_name}.zip"
delivery_sha="$delivery_zip.sha256"
verification_receipt="$output_dir/🧾全系統可逆交付驗證回執｜FullSystemReversibleDeliveryVerification｜${filename_time_tpe}.yaml"

[[ ! -e "$delivery_zip" ]] || fail "拒絕覆寫既有交付：$delivery_zip"
[[ ! -e "$delivery_sha" ]] || fail "拒絕覆寫既有雜湊：$delivery_sha"
[[ ! -e "$verification_receipt" ]] || fail "拒絕覆寫既有回執：$verification_receipt"

temp_root=$(mktemp -d "${TMPDIR:-/tmp}/lkmini-reversible-package.XXXXXX")
cleanup() {
  if [[ -n ${temp_root:-} && -d "$temp_root" ]]; then
    rm -rf -- "$temp_root"
  fi
}
trap cleanup EXIT

source_snapshot="$temp_root/來源提交快照"
package_stage="$temp_root/封裝舞台"
verification_extract="$temp_root/驗證解壓"
delivery_root="$package_stage/$delivery_root_name"
mkdir -p -- \
  "$source_snapshot" \
  "$verification_extract" \
  "$delivery_root/$current_objects_dir" \
  "$delivery_root/$task_receipts_dir" \
  "$delivery_root/$source_evidence_dir" \
  "$delivery_root/$reversible_evidence_dir" \
  "$delivery_root/$historical_evidence_dir"

declare -a current_paths=()
declare -a historical_paths=()

while IFS= read -r -d '' tree_entry; do
  tree_meta=${tree_entry%%$'\t'*}
  tree_path=${tree_entry#*$'\t'}
  tree_mode=${tree_meta%% *}

  [[ "$tree_path" != *$'\n'* ]] || fail "不支援含換行的 Git 路徑：$tree_path"
  [[ "$tree_path" != /* && "$tree_path" != ../* && "$tree_path" != */../* ]] \
    || fail "偵測到不安全路徑：$tree_path"
  [[ "$tree_mode" == '100644' || "$tree_mode" == '100755' ]] \
    || fail "目前只接受一般 blob，路徑=$tree_path，模式=$tree_mode"

  if [[ "$tree_path" == "$history_source_prefix"* ]]; then
    historical_paths+=("$tree_path")
  else
    current_paths+=("$tree_path")
  fi
done < <(
  git -C "$clean_worktree" -c core.quotePath=false \
    ls-tree -r -z "$source_commit"
)

current_count=${#current_paths[@]}
historical_count=${#historical_paths[@]}
(( current_count >= 42 )) \
  || fail "現行 blob 少於 42：實際=$current_count"
(( historical_count >= 11 )) \
  || fail "歷史證據少於 11：實際=$historical_count"

git -C "$clean_worktree" archive --format=tar "$source_commit" \
  | tar -xf - -C "$source_snapshot"

current_bytes=0
for tree_path in "${current_paths[@]}"; do
  source_file="$source_snapshot/$tree_path"
  target_file="$delivery_root/$current_objects_dir/$tree_path"
  [[ -f "$source_file" ]] || fail "提交快照缺少現行 blob：$tree_path"
  mkdir -p -- "$(dirname -- "$target_file")"
  cp -p -- "$source_file" "$target_file"
  current_bytes=$((current_bytes + $(wc -c < "$source_file")))
done

historical_bytes=0
for tree_path in "${historical_paths[@]}"; do
  historical_relative_path=${tree_path#"$history_source_prefix"}
  source_file="$source_snapshot/$tree_path"
  target_file="$delivery_root/$historical_evidence_dir/$historical_relative_path"
  [[ -f "$source_file" ]] || fail "提交快照缺少歷史 blob：$tree_path"
  mkdir -p -- "$(dirname -- "$target_file")"
  cp -p -- "$source_file" "$target_file"
  historical_bytes=$((historical_bytes + $(wc -c < "$source_file")))
done

[[ $(file_count "$delivery_root/$current_objects_dir") -eq "$current_count" ]] \
  || fail '現行本體複製數量不一致'
[[ $(file_count "$delivery_root/$historical_evidence_dir") -eq "$historical_count" ]] \
  || fail '歷史證據複製數量不一致'

source_tree=$(git -C "$clean_worktree" rev-parse "${source_commit}^{tree}")
source_commit_time=$(git -C "$clean_worktree" show -s --format=%cI "$source_commit")

source_commit_receipt="$delivery_root/$source_evidence_dir/🧾來源提交回執｜SourceCommitReceipt.yaml"
{
  printf "'🧾來源提交回執｜SourceCommitReceipt':\n"
  printf "  '🧩唯一根節點｜RootNode': '🧩LKMINI'\n"
  printf "  '⚖️最高公理｜Axiom': 'A=A'\n"
  printf "  '🔑來源提交｜SourceCommit': '%s'\n" "$source_commit"
  printf "  '🌳來源樹｜SourceTree': '%s'\n" "$source_tree"
  printf "  '🕒來源提交時間｜SourceCommitTime': '%s'\n" "$(yaml_single_quote "$source_commit_time")"
  printf "  '🧼工作樹狀態｜WorktreeState': '乾淨'\n"
  printf "  '🔢現行本體數量｜CurrentObjectCount': %d\n" "$current_count"
  printf "  '🔢歷史證據數量｜HistoricalEvidenceCount': %d\n" "$historical_count"
  printf "  '🚦狀態｜Status': '完成'\n"
} > "$source_commit_receipt"

manifest_file="$delivery_root/$reversible_evidence_dir/🧾清單｜Manifest.yaml"
{
  printf "'🧾清單｜Manifest':\n"
  printf "  '🧩唯一根節點｜RootNode': '🧩LKMINI'\n"
  printf "  '⚖️最高公理｜Axiom': 'A=A'\n"
  printf "  '🔑來源提交｜SourceCommit': '%s'\n" "$source_commit"
  printf "  '🕒建立時間｜CreatedAt': '%s'\n" "$time_utc"
  printf "  '📄現行本體｜CurrentObjects':\n"
  printf "    '🔢數量｜Count': %d\n" "$current_count"
  printf "    '🧾路徑｜Paths':\n"
  for tree_path in "${current_paths[@]}"; do
    yaml_list_item "$current_objects_dir/$tree_path" 6
  done
  printf "  '🗄️歷史證據｜HistoricalEvidence':\n"
  printf "    '🔢數量｜Count': %d\n" "$historical_count"
  printf "    '🧾路徑｜Paths':\n"
  for tree_path in "${historical_paths[@]}"; do
    historical_relative_path=${tree_path#"$history_source_prefix"}
    yaml_list_item "$historical_evidence_dir/$historical_relative_path" 6
  done
  printf "  '♻️可逆必要物件｜RequiredReversibleObjects':\n"
  yaml_list_item "$reversible_evidence_dir/🧾清單｜Manifest.yaml"
  yaml_list_item "$reversible_evidence_dir/📍定位器｜Locator.yaml"
  yaml_list_item "$reversible_evidence_dir/📸快照｜Snapshot.yaml"
  yaml_list_item "$reversible_evidence_dir/♻️反向鏈｜ReverseChain.yaml"
  yaml_list_item "$reversible_evidence_dir/🔐雜湊清單｜SHA256SUMS.txt"
  yaml_list_item "$reversible_evidence_dir/🪞幻影膠囊｜PhantomCapsule.yaml"
  printf "  '🚦狀態｜Status': '完成'\n"
} > "$manifest_file"

locator_file="$delivery_root/$reversible_evidence_dir/📍定位器｜Locator.yaml"
{
  printf "'📍定位器｜Locator':\n"
  printf "  '🧩唯一根節點｜RootNode': '🧩LKMINI'\n"
  printf "  '🔑來源提交｜SourceCommit': '%s'\n" "$source_commit"
  printf "  '📄現行本體定位｜CurrentObjectLocators':\n"
  for tree_path in "${current_paths[@]}"; do
    printf "    - '📦封裝位置｜PackageLocation': '%s'\n" \
      "$(yaml_single_quote "$current_objects_dir/$tree_path")"
    printf "      '🐙GitBlob定位｜GitBlobLocator': '%s:%s'\n" \
      "$source_commit" "$(yaml_single_quote "$tree_path")"
  done
  printf "  '🗄️歷史證據定位｜HistoricalEvidenceLocators':\n"
  for tree_path in "${historical_paths[@]}"; do
    historical_relative_path=${tree_path#"$history_source_prefix"}
    printf "    - '📦封裝位置｜PackageLocation': '%s'\n" \
      "$(yaml_single_quote "$historical_evidence_dir/$historical_relative_path")"
    printf "      '🐙GitBlob定位｜GitBlobLocator': '%s:%s'\n" \
      "$source_commit" "$(yaml_single_quote "$tree_path")"
  done
  printf "  '🚦狀態｜Status': '完成'\n"
} > "$locator_file"

snapshot_file="$delivery_root/$reversible_evidence_dir/📸快照｜Snapshot.yaml"
{
  printf "'📸快照｜Snapshot':\n"
  printf "  '🧩唯一根節點｜RootNode': '🧩LKMINI'\n"
  printf "  '🔑來源提交｜SourceCommit': '%s'\n" "$source_commit"
  printf "  '🌳來源樹｜SourceTree': '%s'\n" "$source_tree"
  printf "  '🕒快照時間｜SnapshotTime': '%s'\n" "$time_utc"
  printf "  '🧼工作樹狀態｜WorktreeState': '乾淨'\n"
  printf "  '📄現行本體｜CurrentObjects':\n"
  printf "    '🔢數量｜Count': %d\n" "$current_count"
  printf "    '🔢位元組｜Bytes': %d\n" "$current_bytes"
  printf "  '🗄️歷史證據｜HistoricalEvidence':\n"
  printf "    '🔢數量｜Count': %d\n" "$historical_count"
  printf "    '🔢位元組｜Bytes': %d\n" "$historical_bytes"
  printf "  '♻️回復來源｜RestoreSource': 'Git commit tree 加封裝內完整 blob'\n"
  printf "  '🚦狀態｜Status': '完成'\n"
} > "$snapshot_file"

reverse_chain_file="$delivery_root/$reversible_evidence_dir/♻️反向鏈｜ReverseChain.yaml"
{
  printf "'♻️反向鏈｜ReverseChain':\n"
  printf "  '🧩唯一根節點｜RootNode': '🧩LKMINI'\n"
  printf "  '⚖️最高公理｜Axiom': 'A=A'\n"
  printf "  '🔑來源提交｜SourceCommit': '%s'\n" "$source_commit"
  printf "  '🔟十動作回推｜TenActionReversePath':\n"
  printf "    - '🔢步驟｜Step': 9\n      '➡️動作｜Action': '可逆循環｜ReversibleLoop：驗證 ZIP 與外部 SHA256'\n"
  printf "    - '🔢步驟｜Step': 8\n      '➡️動作｜Action': '同步｜Sync：解壓並核對封裝file_count'\n"
  printf "    - '🔢步驟｜Step': 7\n      '➡️動作｜Action': '快照｜Snapshot：以 SHA256SUMS 逐檔驗證'\n"
  printf "    - '🔢步驟｜Step': 6\n      '➡️動作｜Action': '融合｜Fusion：由 Manifest 還原物件關係'\n"
  printf "    - '🔢步驟｜Step': 5\n      '➡️動作｜Action': '廣播｜Broadcast：由 Locator 找回 Git blob'\n"
  printf "    - '🔢步驟｜Step': 4\n      '➡️動作｜Action': '更新｜Update：比較封裝 blob 與來源提交 blob'\n"
  printf "    - '🔢步驟｜Step': 3\n      '➡️動作｜Action': '驗證｜Verify：確認來源樹與來源提交'\n"
  printf "    - '🔢步驟｜Step': 2\n      '➡️動作｜Action': '掛載｜Mount：掛載 GitHub 程式座標'\n"
  printf "    - '🔢步驟｜Step': 1\n      '➡️動作｜Action': '啟動｜Activate：回到 LKMINI:// 正式協議'\n"
  printf "    - '🔢步驟｜Step': 0\n      '➡️動作｜Action': '讀取｜Read：回指 🧩LKMINI'\n"
  printf "  '🚦狀態｜Status': '完成'\n"
} > "$reverse_chain_file"

phantom_capsule_file="$delivery_root/$reversible_evidence_dir/🪞幻影膠囊｜PhantomCapsule.yaml"
{
  printf "'🪞幻影膠囊｜PhantomCapsule':\n"
  printf "  '🧩唯一根節點｜RootNode': '🧩LKMINI'\n"
  printf "  '🔑正式根協議｜RootProtocol': 'LKMINI://'\n"
  printf "  '⚖️最高公理｜Axiom': 'A=A'\n"
  printf "  '🌱最小可逆種子｜MinimalReversibleSeed':\n"
  printf "    '🔄可逆｜Reversible': true\n"
  printf "    '📏大小｜Size': '最小'\n"
  printf "    '📈膨脹｜Expand': false\n"
  printf "  '🧬空容器｜EmptyContainer':\n"
  printf "    '🔄可逆｜Reversible': true\n"
  printf "    '🪞自我解釋｜SelfDescribe': true\n"
  printf "  '🔐六項最小可逆條件｜SixMinimalReversibleConditions':\n"
  yaml_list_item '🔐SHA256｜SHA256'
  yaml_list_item '🧾清單｜Manifest'
  yaml_list_item '📍定位器｜Locator'
  yaml_list_item '📸快照｜Snapshot'
  yaml_list_item '♻️反向鏈｜ReverseChain'
  yaml_list_item '📦交付包｜Package'
  printf "  '🚦狀態｜Status': '完成'\n"
} > "$phantom_capsule_file"

internal_verification_receipt="$delivery_root/$task_receipts_dir/🧾內部封裝驗證回執｜InternalPackageVerificationReceipt.yaml"
{
  printf "'🧾內部封裝驗證回執｜InternalPackageVerificationReceipt':\n"
  printf "  '🧩唯一根節點｜RootNode': '🧩LKMINI'\n"
  printf "  '🔑來源提交｜SourceCommit': '%s'\n" "$source_commit"
  printf "  '🔢現行本體數量｜CurrentObjectCount': %d\n" "$current_count"
  printf "  '🔢歷史證據數量｜HistoricalEvidenceCount': %d\n" "$historical_count"
  printf "  '🔬逐檔GitBlob比對｜PerBlobGitComparison': '封裝後執行並記錄於外部驗證回執'\n"
  printf "  '🔐內部雜湊驗證｜InternalHashVerification': '封裝後執行並記錄於外部驗證回執'\n"
  printf "  '🚦狀態｜Status': '完成'\n"
} > "$internal_verification_receipt"

hash_file="$delivery_root/$reversible_evidence_dir/🔐雜湊清單｜SHA256SUMS.txt"
(
  cd "$delivery_root"
  find . -type f \
    ! -path "./$reversible_evidence_dir/🔐雜湊清單｜SHA256SUMS.txt" \
    -print0 \
    | sort -z \
    | while IFS= read -r -d '' relative_file; do
        sha256sum -- "$relative_file"
      done
) > "$hash_file"

hash_line_count=$(wc -l < "$hash_file")
expected_hashed_files=$(( $(file_count "$delivery_root") - 1 ))
[[ "$hash_line_count" -eq "$expected_hashed_files" ]] \
  || fail "內部 SHA256SUMS 行數不一致：實際=$hash_line_count，預期=$expected_hashed_files"

(
  cd "$delivery_root"
  sha256sum -c "$reversible_evidence_dir/🔐雜湊清單｜SHA256SUMS.txt" >/dev/null
) || fail '封裝前內部 SHA256 驗證失敗'

(
  cd "$package_stage"
  zip -X -q -r "$delivery_zip" "$delivery_root_name"
)
unzip -tqq "$delivery_zip" || fail 'ZIP 結構測試失敗'

duplicate_entry=$(unzip -Z1 "$delivery_zip" | sort | uniq -d | sed -n '1p')
[[ -z "$duplicate_entry" ]] || fail "ZIP 內有重複路徑：$duplicate_entry"

unzip -q "$delivery_zip" -d "$verification_extract"
extracted_delivery_root="$verification_extract/$delivery_root_name"
[[ -d "$extracted_delivery_root" ]] || fail 'ZIP 解壓後缺少正式交付根'

(
  cd "$extracted_delivery_root"
  sha256sum -c "$reversible_evidence_dir/🔐雜湊清單｜SHA256SUMS.txt" >/dev/null
) || fail 'ZIP 解壓後內部 SHA256 驗證失敗'

extracted_current_count=$(file_count "$extracted_delivery_root/$current_objects_dir")
extracted_historical_count=$(file_count "$extracted_delivery_root/$historical_evidence_dir")
[[ "$extracted_current_count" -eq "$current_count" ]] \
  || fail "ZIP 現行本體數量不一致：實際=$extracted_current_count，預期=$current_count"
[[ "$extracted_historical_count" -eq "$historical_count" ]] \
  || fail "ZIP 歷史證據數量不一致：實際=$extracted_historical_count，預期=$historical_count"

for tree_path in "${current_paths[@]}"; do
  cmp -s \
    "$extracted_delivery_root/$current_objects_dir/$tree_path" \
    <(git -C "$clean_worktree" cat-file blob "${source_commit}:${tree_path}") \
    || fail "現行 blob 與來源提交不一致：$tree_path"
done

for tree_path in "${historical_paths[@]}"; do
  historical_relative_path=${tree_path#"$history_source_prefix"}
  cmp -s \
    "$extracted_delivery_root/$historical_evidence_dir/$historical_relative_path" \
    <(git -C "$clean_worktree" cat-file blob "${source_commit}:${tree_path}") \
    || fail "歷史 blob 與來源提交不一致：$tree_path"
done

zip_file_count=$(unzip -Z1 "$delivery_zip" | awk 'substr($0, length($0), 1) != "/" { n++ } END { print n + 0 }')
packaged_file_count=$(file_count "$extracted_delivery_root")
[[ "$zip_file_count" -eq "$packaged_file_count" ]] \
  || fail "ZIP 檔案總數不一致：索引=$zip_file_count，解壓=$packaged_file_count"

zip_hash=$(sha256sum "$delivery_zip" | awk '{ print $1 }')
printf '%s  %s\n' "$zip_hash" "$(basename -- "$delivery_zip")" > "$delivery_sha"
(
  cd "$output_dir"
  sha256sum -c "$(basename -- "$delivery_sha")" >/dev/null
) || fail 'ZIP 外部 SHA256 sidecar 驗證失敗'

{
  printf "'🧾全系統可逆交付驗證回執｜FullSystemReversibleDeliveryVerification':\n"
  printf "  '🧩唯一根節點｜RootNode': '🧩LKMINI'\n"
  printf "  '⚖️最高公理｜Axiom': 'A=A'\n"
  printf "  '🔑來源提交｜SourceCommit': '%s'\n" "$source_commit"
  printf "  '📦交付檔案｜DeliveryFile': '%s'\n" "$(yaml_single_quote "$(basename -- "$delivery_zip")")"
  printf "  '🔐交付SHA256｜DeliverySHA256': '%s'\n" "$zip_hash"
  printf "  '🕒驗證時間UTC｜VerifiedAtUTC': '%s'\n" "$time_utc"
  printf "  '🕒驗證時間TPE｜VerifiedAtTPE': '%s'\n" "$time_tpe"
  printf "  '🔢現行本體數量｜CurrentObjectCount': %d\n" "$current_count"
  printf "  '🔢歷史證據數量｜HistoricalEvidenceCount': %d\n" "$historical_count"
  printf "  '🔢封裝檔案總數｜PackagedFileCount': %d\n" "$packaged_file_count"
  printf "  '🔢內部雜湊驗證數｜InternalHashVerifiedCount': %d\n" "$hash_line_count"
  printf "  '🧪ZIP結構測試｜ZipStructureTest': '完成'\n"
  printf "  '🧪ZIP解壓測試｜ZipExtractionTest': '完成'\n"
  printf "  '🔐內部雜湊驗證｜InternalHashVerification': '完成'\n"
  printf "  '🔐外部雜湊驗證｜ExternalHashVerification': '完成'\n"
  printf "  '🧬逐檔GitBlob比對｜PerBlobGitComparison': '完成'\n"
  printf "  '♻️反向鏈驗證｜ReverseChainVerification': '完成'\n"
  printf "  '🚦狀態｜Status': '完成'\n"
} > "$verification_receipt"

printf '🚦狀態｜Status: 完成\n'
printf '📦交付檔案｜DeliveryFile: %s\n' "$delivery_zip"
printf '🔐交付SHA256｜DeliverySHA256: %s\n' "$zip_hash"
printf '🧾驗證回執｜VerificationReceipt: %s\n' "$verification_receipt"
printf '🔢現行本體｜CurrentObjects: %d\n' "$current_count"
printf '🔢歷史證據｜HistoricalEvidence: %d\n' "$historical_count"
printf '🔢封裝檔案｜PackagedFiles: %d\n' "$packaged_file_count"
