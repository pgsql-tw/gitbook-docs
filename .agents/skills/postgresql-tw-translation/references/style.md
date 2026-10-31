# 正體中文翻譯慣例

這是從既有譯文歸納的專案慣例，不表示每個現有譯法都正確或已獲社群統一採用。來源均相對於專案根目錄；原有常用詞與版本反例的觀察基準為 branch 15、commit 9e1029c。下方 PostgreSQL 18 觀察及語意檢查提醒另來自 2026-09～10 協作審查紀錄與 Claude 的 2026-10-24 草稿，不是全站用詞普查或逐項使用者裁決。

## 語氣與句型

- 本批已確認採「技術直述」：以簡潔且主詞明確的陳述句傳達技術關係與條件，不加入原文未述的推論。例如，`Because logical replication is based on a similar architecture as physical streaming replication, the monitoring on a publication node is similar to monitoring of a physical replication primary.` 譯為「由於邏輯複寫的架構與實體串流複寫相近，發佈節點的監控方式也類似於實體複寫主要伺服器的監控。」
- 教學以「你」直接向讀者說明，配合「我們」帶入範例。可參考 `tutorial/getting-started/architectural-fundamentals.md` 的「在開始使用之前，你需要瞭解……」，以及 `tutorial/advanced-features/transactions.md` 的銀行交易範例。
- 先解釋概念，再說明條件、執行方式與結果。沿用「舉例來說」、「如果……，那麼……」、「請參閱……」等自然句型，避免逐字搬運英文長句。
- 中文使用全形標點；中文與 PostgreSQL、SQL 等英文名稱間適度留空白。初次介紹概念可採「交易（Transaction）」及「交易儲存點（savepoint）」形式，後續以中文簡稱。
- 不需照抄既有冗詞、錯字或不自然的重複，如「你所所用」、「交易事務」。忠實保留技術語意比模仿字面更重要。

## 有來源的常用詞

| 原文 | 優先沿用 | 來源 |
| --- | --- | --- |
| database / table / row / column | 資料庫／資料表／資料列／欄位 | `tutorial/the-sql-language/creating-a-new-table.md`、`populating-a-table-with-rows.md`；後者同目錄 |
| data type | 資料型別 | `the-sql-language/data-types/README.md` |
| transaction / transaction block / savepoint | 交易／交易區塊／交易儲存點 | `tutorial/advanced-features/transactions.md` |
| client / server | 用戶端／伺服器 | `tutorial/getting-started/architectural-fundamentals.md` |
| view / materialized view | 檢視表／具體化檢視表 | `the-sql-language/ddl/generated-columns.md` |
| index / unique index | 索引／唯一值索引 | `the-sql-language/index/unique-indexes.md` |
| constraint / primary key | 限制條件／主鍵 | `the-sql-language/index/unique-indexes.md` |
| logical replication | 邏輯複寫 | `server-administration/logical-replication/README.md` |
| process（作業系統） | 程序 | 使用者裁決，2026-09-11（PostgreSQL 18）；沿用 `server-programming/plpython/plpython-envar.md`、`server-administration/user-manag/perm-functions.md`。例：server process →「伺服器程序」、fork a new process →「啟動（fork）一個新的程序」 |

- 「程序」同時用於 procedure 與 trigger（如「觸發程序」「Tcl 程序名稱」），這是已知的同形詞；需要區分時可於初次出現加註原文，例如「伺服器程序（server process）」。`appendixes/acronyms/README.md` 的「行程間通訊」「行程識別碼」尚未納入本次裁決，暫不更動。

## 提示標題的使用者裁決

- **Caution →「注意」**（2026-10-31）：以官方來源的提示類型為準；PostgreSQL HTML 可由 `div class="caution"` 確認。不用「小心」作為該類提示的標題，但不替換正文中的一般用詞，也不把 Note、Warning 等其他類型一律當成 Caution。維護既有頁面時保留原正文與原碼；GitBook 呈現與定位保護依 [GitBook 維護規則](gitbook-maintenance.md#render-confirmed-caution-callouts)。裁決來源為專案 `outputs/pg18-translation/agents/PROTOCOL.md`。

## 尚未統一的詞

- function 同時有「函式」及「函數」：第 9 章目錄兩者並存。修改既有小節時先保持該小節一致；新內容建議採「函式」。這是編輯建議，不是已確認的全專案規定。
- schema 常保留英文；不要逕自全站替換成「綱要」或「結構描述」。以鄰近章節用法為準，必要時保留英文辨識。
- generated column 現有譯文採「自動欄位」，但標題仍為英文。先沿用並保留 generated column 對照，術語變更需獨立列為編輯議題。
- replication 的發布端稱呼有「發佈／發布」，訂閱端有「訂閱者／訂閱戶」。新段落建議統一為「發佈者／訂閱者」，勿把 publication（發佈物件）與 publisher（發佈者）混為一談。
- window function 有「窗函數」及「Window 函式」；foreign key 在教學有「外部索引鍵」。跨章統一前先列出差異，勿因單一來源就推定唯一標準。

## 版本正確性反例

本次抽查發現 5.9 schema 權限、11.6 唯一值索引、26.3 備份 API、20.9 統計參數仍含舊版敘述。因此本 skill 僅重用語言風格，不把這些頁面的技術內容作為正確性基準。`README.md` 的 `/docs/current/` 連結亦不能決定分支版本。

## PostgreSQL 18 批次用詞觀察（非強制術語表）

Claude 草稿整理的用詞方向如下，供尋找鄰近已發佈用法與評估新批次風格時參考。不得把「某頁已通過審查」推論為「全專案已裁決」，也不因不同譯法就直接退件或全站替換。上方「尚未統一的詞」保留其歷史觀察性質，不據此否定 PostgreSQL 18 章節的不同用法。

| 原文／情境 | 批次紀錄中的譯法 |
| --- | --- |
| schema | 綱要 |
| function／procedure／routine（SQL 物件） | 函式／程序／常式 |
| value | 值；是否用「數值」須看是否確指數量，不能只靠搜尋取代 |
| join／union（散文） | 連接／聯集 |
| foreign join／outer join | 外部資料表連接／外部連接；兩者語意不可混淆 |
| foreign key／window function | 外鍵／視窗函式 |
| generated column（stored／virtual） | 產生欄位（儲存式／虛擬） |
| publication／publisher／subscriber | 發佈／發佈者／訂閱者；須區分物件、角色與動作 |
| replication／replication slot／replication origin | 複寫／複寫插槽／複寫來源 |
| standby server／flush／wraparound／roll back | 待命伺服器／刷寫／回捲／回復；各依技術情境判讀 |
| tuple／memory context | 元組／記憶體上下文 |
| visibility map／free space map | 可見性對應表／可用空間對應表；storage 目錄兩項已同步，不再記為待修 |
| materialized view／constraint | 具體化檢視表／限制條件 |
| domain／collation／bootstrap | 網域／定序／初始建置 |
| host variable | 主機變數 |
| 目錄欄位的 references | 參照 |
| secret | 草稿偏好「祕密」；檢查器對「秘」的提示不是字形裁決依據 |

其他差異候選包含 information schema、安全標籤／安全性標籤、文字搜尋／文字檢索字典、述詞／謂詞、datum、授與／授予。未逐項確認前，不宣告其中一種已全站統一。交叉參照顯示文字可沿用「第 N 節」「表 N」「第 N 章」「附錄 N」；識別字及正式名稱保留辨識性，連結文字調整不等於任意改動目的地。

## 常見語意檢查提醒

這些是從退件經驗歸納的檢查方向，不是自動替換表或不問上下文的退件規則；個案仍以官方原文與使用者裁決為準。

- **數量與比較：** 確認端點是否包含、次數與數量有無混淆，例如 more than one 不應模糊成包含一個的範圍。
- **真值與否定：** 核對否定對象、作用範圍及雙重否定；涉及 SQL 真值時另查 NULL 語境，不把一般英文條件一律解讀成固定真值表。
- **情態與程度：** 分清 may、can、should、must，以及「難以實行」與「不可能」、「適用性」與「使用頻率」。
- **主詞與修飾：** 明確誰擁有、接收、阻擋、逐出或截斷什麼；不要讓中文語序改變動作對象。
- **條件組合：** 保留且／或、各自對應、附加選項與替代條件，不將逐項可選誤寫成整組互斥。
- **語意範圍：** 注意限制對象及例外，不能把特定物件種類、最後一行除外等條件擴大成所有物件或所有行。
- **增譯與漏譯：** 複核 except、unless、only if 等限制，亦不擅加「一定」「重新」「明確指定」等強度或動作。
- **英文殘留：** 區分一般散文、交叉參照文字與產品名、書名、人名、API／型別識別字、受保護原碼；不能把所有英文提示當成未譯缺陷。
