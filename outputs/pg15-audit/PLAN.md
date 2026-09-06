# PostgreSQL 15 正體中文手冊：盤點與更新計劃

盤點日期：2026-09-06。分支：`15`。基準提交：`9e1029c`（2023-08-20）。開始盤點時工作目錄乾淨。官方基準：[PostgreSQL 15.19 手冊](https://www.postgresql.org/docs/15/index.html)，不是 `/docs/current/`。本次僅新增盤點成果與翻譯 skill，未修改手冊正文及 SUMMARY。

## 結論與範圍

目前已建置 I–VIII 部分、1–76 章及 A–O 附錄的入口，但入口完整不等於內容完整。最優先工作是修正仍描述舊版行為的正文，其次補齊缺漏子節、空白頁與指令參考，最後分批完成英文內容與用語一致性。

本次掃描全部 SUMMARY 入口和其檔案，下載官方首頁及其 110 個目錄連結頁，進行章級與直接子節比對，並抽查已翻譯及版本敏感的正文。沒有逐句審校所有頁面，也沒有把所有更深層小節、表格與函式簽章做全文差異比對。因此以下是可執行的工作清單，不宣稱全書翻譯完成率或所有技術差異均已找出。

## 本地內容盤點

| 類別 | 頁數 | 解讀 |
| --- | ---: | --- |
| SUMMARY 對應頁面 | 859 | 路徑不重複，全部存在 |
| 僅有標題的末端頁面 | 61 | 無正文，需要補充 |
| 僅有標題、但有子頁的容器 | 11 | 不直接判定為缺譯，另核對官方章介紹 |
| 正文未偵測到中文字 | 422 | 優先進入待翻譯檢查；可能含純程式碼或英文連結 |
| 有中文，且有長英文區塊 | 128 | 混合內容候選，需逐段確認 |
| 有中文，未觸發上述英文規則 | 237 | 仍須審校，不代表完成或與 15 一致 |

分類去除標題、程式碼區塊、行內程式碼與 URL 後，以中文字和英文區塊判斷；連結文字、API 表格仍可能影響結果。長英文區塊定義為至少 20 個英文字且無中文的段落。數字僅供排程，不能直接換算翻譯進度。

| 部分 | 頁數 | 空白末端 | 英文候選 | 混合候選 | 中文待審 | 空白容器 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| I 新手教學 | 24 | 0 | 0 | 0 | 23 | 1 |
| II SQL 查詢語言 | 138 | 0 | 51 | 25 | 61 | 1 |
| III 系統管理 | 130 | 0 | 65 | 24 | 41 | 0 |
| IV 用戶端介面 | 110 | 53 | 47 | 6 | 4 | 0 |
| V 資料庫程式設計 | 83 | 0 | 64 | 2 | 16 | 1 |
| VI 參考資訊 | 143 | 0 | 54 | 41 | 48 | 0 |
| VII 資料庫進階 | 134 | 8 | 84 | 14 | 21 | 7 |
| VIII 附錄 | 89 | 0 | 56 | 16 | 16 | 1 |

另有簡介、前言及其子頁共 7 頁，以及參考書目 1 頁。

全部逐頁分類見 [inventory.csv](inventory.csv)，逐章統計見 [chapter-inventory.csv](chapter-inventory.csv)。

## 第一批：P0 版本內容及結構修復

| 範圍 | 已確認的本地證據 | 工作與驗收 |
| --- | --- | --- |
| 5.9 Schemas | `the-sql-language/ddl/schemas.md` 仍敘述所有使用者預設具備 public 的 CREATE、USAGE | 按 15 的新資料庫預設與升級保留既有權限兩種情況改寫，核對該節完整敘述 |
| 11.6 唯一值索引；連動 5.4、CREATE TABLE、CREATE INDEX | `the-sql-language/index/unique-indexes.md` 語法與正文沒有 NULLS NOT DISTINCT | 補充 15 的選項與 NULL 行為；其他三處逐一比對，不假定都缺漏 |
| 26.3 PITR；連動 9.27、pg_basebackup | `server-administration/backup-and-restore/continuous-archiving-and-point-in-time-recovery-pitr.md` 還教 pg_start_backup／pg_stop_backup 與 exclusive backup | 重對官方整節，移除不適用流程，核對新 API、回傳內容及步驟；不可只取代函式名稱 |
| 20.9、28.2 統計資訊 | `server-administration/server-configuration/run-time-statistics.md` 仍有 stats_temp_directory，28.2 標題仍為統計資訊收集器 | 對齊 cumulative statistics 架構、參數及讀取一致性；確認全部欄位與範例 |
| SUMMARY 及頁面標題 | 34 章子節多寫成 33.x；36 章多為 35.x；68/69/71/73/75 章亦留舊編號 | 依官方主題對應重編，不能固定整批加一；同時檢查正文標題與交叉連結 |
| 37 Information Schema | attributes、character_sets 同標 37.7；domain_constraints、domain_udt_usage 亦有重號 | 以物件名稱比對官方再修編號，補缺頁 |
| 53／54 Catalogs 與 Views | 7 個可按名稱對上的 view 頁仍列在 53 章 | 將目錄歸位到 54 章；檔案路徑是否搬移可另行決定，保留可用連結 |
| 官方版本連結 | 含 /10/ 的頁面 91、/11/ 9、/12/ 77、/13/ 82、/14/ 4、/current/ 86、/devel/ 2 | 區分原文對照與刻意引用的歷史資訊；前者改為 /15/ 並驗證實際章節及 anchor，後者保留用途。各類有重疊，不能相加當頁面總數 |

上述技術變更依據：[15 版發布說明](https://www.postgresql.org/docs/15/release-15.html)。實作時還需讀取各對應章的完整 15.19 正文；本表不是資料庫操作建議。

`tutorial/getting-started/architectural-fundamentals.md` 的 frontmatter 尚標「版本：11」。應在完成版本審校後更新來源記錄，不能只把版本號改成 15 便當作內容已同步。

有 4 個已追蹤的 Markdown 未列入 SUMMARY：`internals/system-catalogs/` 下的 `pg_replication_slots.md`、`pg_roles.md`、`pg_settings.md`、`pg_shmem_allocations.md`。54 章已有同名對應頁，應先比對內容與入站連結，確認重複或遷移殘留後再處理，不能直接新增第二份入口或刪除。

## 第二批：P1 補齊主要缺口

| 章節／群組 | 需要補充或更新的範圍 |
| --- | --- |
| 34 libpq | 缺 34.5 Pipeline Mode 的目錄入口；12 個既有子頁僅標題。先補原文／翻譯正文，再對齊 34.1–34.22；既有 Row-by-Row 是不同主題，不能當 Pipeline Mode |
| 35 Large Objects | 5 個子頁全部僅標題；補 35.1–35.5 |
| 36 ECPG | 15 個子頁僅標題，另缺 Oracle Compatibility Mode；依官方 36.1–36.17 配置，不沿用舊 35.x |
| 37 Information Schema | 21 個子頁僅標題；另缺 routine_routine_usage、routine_sequence_usage、routine_table_usage 的入口 |
| 40 Event Triggers | 補 40.5 Table Rewrite Event Trigger Example；先核對有無嵌在其他頁的範例 |
| 49 Logical Decoding | 補 49.9 Streaming of Large Transactions、49.10 Two-phase Commit Support |
| VI SQL Commands | 目前官方 183 個指令入口中，有 68 個未按名稱映射到本地；優先 BEGIN、COMMIT、ROLLBACK、SAVEPOINT、CALL、交易與游標指令，其次 ALTER／CREATE／DROP 群組。完整名單見候選清單 |
| VI 用戶端工具 | 缺 clusterdb、ecpg、pg_amcheck、pg_config、reindexdb 的目錄入口 |
| VI 伺服器工具 | 缺 pg_checksums、pg_controldata、pg_resetwal、pg_rewind、pg_waldump、postmaster 的目錄入口 |
| 附錄 E | 既有 15、15.1、15.2；補 15.3–15.19 共 17 份發布說明，再重編 E.x。minor release 編號會隨上游新增而移動 |

此處「缺入口」不等於主題在全書從未提及。例如交易教學已有 BEGIN／COMMIT，仍不能取代完整指令參考頁。

31 章的 Row Filters、Column Lists 已有本地頁面，應歸入待翻譯／更新，而非新增缺頁。MERGE 已有中文內容，51 Archive Modules 與 66 Custom WAL Resource Managers 也已有正文；需要審校與完成翻譯，不應重建。

來源：[libpq](https://www.postgresql.org/docs/15/libpq.html)、[ECPG](https://www.postgresql.org/docs/15/ecpg.html)、[Information Schema](https://www.postgresql.org/docs/15/information-schema.html)、[SQL Commands](https://www.postgresql.org/docs/15/sql-commands.html)、[版本資訊](https://www.postgresql.org/docs/15/release.html)。

## 第三批：P2 全書翻譯與深層內容

| 範圍 | 建議批次 |
| --- | --- |
| 1–3 教學 | 以已譯文為風格參考，核對版本、連結、範例與術語；不需重新全譯 |
| 4–15 SQL | 先完成 5.3、9 章函式與運算子、11.9、13.5 等混合／英文內容，再審校其餘各節；9 章應分函式類別交付並逐項比對表格與簽章 |
| 16–33 管理 | 先 19–21 設定認證、25–28 維護備份監控、30–31 WAL／複寫；再安裝、角色、本地化、JIT 與 regression tests。核對 JSON 日誌、備份壓縮、角色清單等 15 版內容是否完整 |
| 38–51 程式設計 | 優先 PL/pgSQL、觸發器、邏輯解碼；44 PL/Tcl 現在只有一句介紹，45 PL/Perl、47 SPI 也僅章介紹層級，需補官方子節；其餘 Extending SQL、Rule System、PL/Python、Background Workers、Archive Modules 分章翻譯 |
| 52–66 內部機制 | 53 Catalogs 有 40 個直接子節未映射；54 Views 扣除移錯位置的 7 頁後仍有 16 個未映射。55 Protocol 有 7 個空白末端。60、61、64 只有章頁入口的支援函式/API 子節需補；其餘依英文／混合清單完成 |
| 67–76 索引與儲存 | 72 Hash Indexes 整頁僅標題，補 72.1–72.2；73.7 HOT 缺入口；74 的 6 個子節及 76 的 3 個子節需補，先確認是否散落在父頁，再依 GitBook 閱讀結構拆分；67–71、75 完成翻譯與編號校正 |
| 附錄 A–D、G–O | 保留完整錯誤碼、SQL 關鍵字及相容性表格；逐項對 15 審查。O 的 5 個更名／移除功能子節須補入口與內容；其餘依逐頁分類翻譯 |

附錄 F 共有 50 個官方模組入口，本地有 23 個。缺少的 27 個如下，依主題分批處理，名稱及正確 F.x 編號見候選清單：

- 備份封存：basebackup_to_shell、basic_archive。
- 型別、搜尋與索引：btree_gist、citext、cube、dict_int、dict_xsyn、fuzzystrmatch、intagg、intarray、isn、lo、ltree、seg、unaccent。
- 觀測與維護：old_snapshot、pageinspect、pg_freespacemap、pg_prewarm、pgrowlocks、pg_surgery、pg_walinspect。
- 其他模組：pgcrypto、spi、sslinfo、tcn、xml2。

來源：[官方附錄 F](https://www.postgresql.org/docs/15/contrib.html)、[System Catalogs](https://www.postgresql.org/docs/15/catalogs.html)、[System Views](https://www.postgresql.org/docs/15/views.html)、[Physical Storage](https://www.postgresql.org/docs/15/storage.html)。

## 排程及交付標準

1. 第一個批次交付 P0 的版本差異修復，以及章號／來源 URL 對應表。先處理 public 權限、備份 API、統計系統與唯一值索引。
2. 接著以「34 libpq」、「交易指令參考」、「工具參考」、「15.x release notes」各自成批。每批完成正文、目錄、引用與審校，避免只建立空檔。
3. 大型章節如第 9、37、53、54 章，按官方子節分批；其他章以一章為單位。P2 可依社群貢獻者專長認領，不先虛估工時。
4. 每批需記錄：官方 URL／版本／日期、對應本地檔案、待譯段落、技術審校結果、連結與 GitBook 格式檢查。只在正文、表格、範例、限制及交叉引用都核對後標為完成。
5. 維護術語決議清單，區分「已觀察慣例」與「新建議」。不要把全文潤飾、技術更正與搬移路徑混成難審查的單一變更。

## 盤點檔案與重現

- [official-toc.json](official-toc.json)：本次取得的官方目錄快照，保留英文標題及來源路徑。
- [section-comparison.csv](section-comparison.csv)：直接子節／指令對應，含本地路徑與官方 URL。
- [unmapped-sections.md](unmapped-sections.md)：未映射候選完整名單。
- [inventory.csv](inventory.csv)、[chapter-inventory.csv](chapter-inventory.csv)：逐頁及逐章現況。
- [翻譯 skill](postgresql-tw-translation/SKILL.md)及[風格依據](postgresql-tw-translation/references/style.md)。

`section-comparison.csv` 的 title/path 僅表示標題或檔名映射，不能證明正文相同；number-only-review 只按編號推定；other-chapter-review 表示找到同名物件但章節位置不同；unmapped-review 仍須人工排除合併頁或譯名差異。已知 7.8 的 Querys 拼字，以及 22.5 的 Default Roles 舊名稱都會造成未映射，實際已有頁面，應更新而非新建。不得把候選總數宣稱為缺譯頁數。

在專案根目錄執行：

```powershell
python outputs/pg15-audit/audit.py
python outputs/pg15-audit/compare.py
```

重新取得官方目錄時，第一行加上 `--fetch`。這會覆蓋目錄快照；需記錄新的版本日期並重新審查本計劃的數字。程式只讀手冊，輸出在本目錄。本次未連線資料庫、未執行 SQL，也未做 GitBook 發布驗證。
