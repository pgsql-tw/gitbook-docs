# 正體中文翻譯慣例

這是從既有譯文歸納的專案慣例，不表示每個現有譯法都正確或已獲社群統一採用。來源均相對於專案根目錄，基準為 branch 15、commit 9e1029c。

## 語氣與句型

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

## 尚未統一的詞

- function 同時有「函式」及「函數」：第 9 章目錄兩者並存。修改既有小節時先保持該小節一致；新內容建議採「函式」。這是編輯建議，不是已確認的全專案規定。
- schema 常保留英文；不要逕自全站替換成「綱要」或「結構描述」。以鄰近章節用法為準，必要時保留英文辨識。
- generated column 現有譯文採「自動欄位」，但標題仍為英文。先沿用並保留 generated column 對照，術語變更需獨立列為編輯議題。
- replication 的發布端稱呼有「發佈／發布」，訂閱端有「訂閱者／訂閱戶」。新段落建議統一為「發佈者／訂閱者」，勿把 publication（發佈物件）與 publisher（發佈者）混為一談。
- window function 有「窗函數」及「Window 函式」；foreign key 在教學有「外部索引鍵」。跨章統一前先列出差異，勿因單一來源就推定唯一標準。

## 版本正確性反例

本次抽查發現 5.9 schema 權限、11.6 唯一值索引、26.3 備份 API、20.9 統計參數仍含舊版敘述。因此本 skill 僅重用語言風格，不把這些頁面的技術內容作為正確性基準。`README.md` 的 `/docs/current/` 連結亦不能決定分支版本。
