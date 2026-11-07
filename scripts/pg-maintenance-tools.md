# PostgreSQL 手冊維護工具

這組工具處理靜態掃描、精確連結改寫與公開驗收，不提交、不推送，也不自動更改 GitBook 設定。版本及資料根目錄先用 `python scripts/pg_project.py` 確認；語意審查與新的手冊相容性試跑仍依專案 skill。

## 掃描一致性

```powershell
python scripts/final_site_audit.py --out outputs/pg-audit/run1
```

`scan.json` 的 `scan_valid` 才表示這次輸入一致：HEAD、實際讀取的檔案雜湊、來源清單、審查存檔與連結目標均需保持一致。掃描使用保存的輸入內容；執行期間異動會保留報告、標記無效並以結束碼 2 返回。這不等同於 lint 全零或公開畫面通過。

`site_pages` 包含 SUMMARY 指向但尚未加入 Git 的新頁；`tracked_site_pages` 只計 Git 已追蹤者，另列 `untracked_summary_pages`。工具不為掃描自動執行 `git add`。

## 預覽及套用精確連結改寫

規格範例（檔案與 ID 請換成當次已確認目標）：

```json
{
  "files": ["chapter/parent.md", "chapter/README.md"],
  "targets": [
    {"from": {"page": "chapter/parent.md", "fragment": "OLD"},
     "to": {"page": "chapter/parent/item.md", "fragment": "item"}}
  ],
  "expected_changes": {"chapter/parent.md": 1, "chapter/README.md": 1}
}
```

```powershell
python scripts/pg_link_rewrite.py plan --spec outputs/pg-repair/spec.json --out outputs/pg-repair/plan.json
python scripts/pg_link_rewrite.py apply --plan outputs/pg-repair/plan.json --report outputs/pg-repair/applied.json
```

先閱讀計畫的逐項 URL 變更、檔案範圍與數量。沒有 `expected_changes` 時可以產生預覽，但不能套用；數量不符也不能套用。一般原位改寫只變動精確「目的檔案＋片段」，不整理無關同頁連結。引用定義改一次，並保留其使用位置、標題、BOM 與換行。碼框、行內碼、HTML `pre`／`code` 及註解不改。

`rewrite_links(text, source, destination, targets)` 可供小節拆分工具使用：當內容移往不同檔案時，會重算相對引用；它只回傳新文字及編輯清單，不自行寫檔。完整小節、原碼、表格、目錄與目的 ID 的保護仍需在批次驗證，不是此連結工具的語意判斷。

套用前驗證全部候選檔案雜湊，並重新計算計畫，才開始寫入。失敗時只撤回仍等於本工具生成版本的已寫檔案；若發現後續其他修改則保留它，記錄 `rollback_conflicts`。`outputs/pg-maintenance/rewrite.lock` 阻止同一工具競爭；殘留鎖需先確認沒有執行者，工具不自行搶鎖。

## 共用公開驗收

每批提供一份 bundle，使用共用程式，無須再複製瀏覽器腳本或 `common.py`。以下是設定格式範例，不代表已驗證該版本的正式網站：

```json
{
  "origin": "https://manual.example.org",
  "major": 19,
  "source_commit": "REPLACE_WITH_REVIEWED_COMMIT",
  "cases": [
    {"name": "root", "path": "/19/chapter/item", "narrow": false,
     "batchTargets": [{"anchor": "item", "kind": "heading"}],
     "expected": {"allCodeTexts": ["SELECT 1;"], "tableRows": []}},
    {"name": "table-reference", "path": "/19/chapter/parent", "narrow": true,
     "travel": {"path": "/19/chapter/item", "anchor": "item", "kind": "table"}}
  ]
}
```

```powershell
node scripts/pg_public_probe.mjs --bundle outputs/pg-audit/bundle.json --out outputs/pg-audit/run1 --all
node scripts/pg_public_probe.mjs --bundle outputs/pg-audit/bundle.json --out outputs/pg-audit/run2 --cases root,table-reference
python scripts/pg_public_audit.py --bundle outputs/pg-audit/bundle.json --results outputs/pg-audit/run1/browser-checks.json --out outputs/pg-audit/run1/verification.json
```

工具使用隔離的本機 Chrome；可用 `PG_CHROME_PATH` 或 bundle 的 `chromePath` 指定位置，不使用使用者的瀏覽器設定檔。每次執行採新的輸出目錄，既有結果不覆蓋；不自動重新載入失敗案例。若要依 skill 進行有界重驗，保留首讀報告並在另一目錄明確指定案例。

點擊種類為 `heading`、`body`、`table`、`compatibility`（後者另提供 `paragraphPrefix`）。`any` 及既有 `batchAnchors`／`allowHeadingLink` 是舊案例遷移相容模式，新案例應明確選取用途。輸出記錄實際連結是否位於標題、表格或指定段落，避免標題自連結冒充正文引用。

`expected` 支援 `allCodeTexts`、`tableRows`、`listBlocks`、`headingIds`、`rootParagraphs`、`outsideCodeParagraphs`、`link_counts`。正文比較只合併空白並忽略空段；只有明確設定 `ignore_last_updated: true` 才排除已知時間格式，不任意丟棄其他文字。碼框按完整內容及順序比較，不合併其空白。驗收報告列出每案宣告的內容欄位，沒有宣告的檢查不代表已通過。

完整小節搬移前，可在修前案例加入 `sectionRanges`，例如 `[{"name":"part","start":"section-id","end":"next-section-id"}]`；最後一節可改用 `endParagraphPrefix` 指定唯一來源段落。兩種結束條件只能擇一，工具不推測邊界。結果的 `sections` 保存各節的內容及其在全頁陣列中的索引，能區分不同小節中重複出現的段落；缺少、重複或反向邊界會標記 `valid: false`，準備器必須拒絕採用。此資料只提供 DOM 歸屬，不自動決定該搬移哪個小節，也不代表新頁已公開驗收。

`pg_public_audit.expected_links()` 使用 Markdown 解析器辨識角括號網址與引用式連結，再加入每頁明確提供的 `interface_links`；不從父頁剩餘連結猜測子頁介面。`public_url()` 要求提供實測或明確計畫的路徑映射，不把檔案位置當公開路徑。批次準備程式負責提供正文歸屬、已知導覽及內容預期；共用工具不硬編碼某批表格數量、頁名或 `zhu-yi`。

比對器要求結果為 `complete`，且 bundle 雜湊、來源提交、版本與來源網域均符合；缺案、重複案、尚在執行或失敗的程序不能算通過。多個 shard 可共同驗收，但案例不可重複。重驗與首讀應分別比對及保存各案判定，不能把重複輸出直接當成不同案例相加。

## 進度檔與驗證

Python 使用 `pg_maintenance.atomic_json/read_json`，Node 使用 `pg_public_probe_helpers.mjs` 的 `atomicJson/readJson`。以同目錄暫存檔、flush／sync、原子替換寫入；公平的程序內排隊及共用 `.io.lock` 協調讀寫。Windows 短暫分享鎖有次數上限，超過就報錯並保留舊檔，不重試網路工作或吞掉 JSON 損毀。程序異常留下的鎖不會自動刪除，先核對執行者再處理。

```powershell
python -m unittest discover -s scripts -p test_pg_maintenance.py -v
python -m unittest discover -s scripts -p test_final_site_audit.py -v
python -m unittest discover -s scripts -p test_pg_public_audit.py -v
node --test scripts/test_pg_public_probe.mjs
```

Node 測試只在本機 HTTP 測試頁與隔離 Chrome 操作，不操作正式文件站。沒有 Chrome 時會明確跳過瀏覽器案例；跳過不代表公開驗收通過。
