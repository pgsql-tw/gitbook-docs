<a id="SQL-DECLARE"></a><a id="id-1.9.3.99.1"></a><a id="id-1.9.3.99.2"></a><a id="id-1.9.3.99.3"></a>

## DECLARE

DECLARE — 定義游標

<a id="id-1.9.3.99.6"></a>

## 語法

```

DECLARE name [ BINARY ] [ ASENSITIVE | INSENSITIVE ] [ [ NO ] SCROLL ]
    CURSOR [ { WITH | WITHOUT } HOLD ] FOR query
```

<a id="id-1.9.3.99.7"></a>

## 說明

`DECLARE` 讓使用者建立游標，游標可以用來從一個較大的查詢中，每次擷取少量的資料列。游標建立之後，使用 [`FETCH`](sql-fetch.md) 從中擷取資料列。

### 注意

本頁說明的是在 SQL 命令層級使用游標的方式。如果您要在 PL/pgSQL 函式中使用游標，規則有所不同——請參閱[第 41.7 節](../../server-programming/plpgsql/plpgsql-cursors.md)。

<a id="id-1.9.3.99.8"></a>

## 參數

*`name`*
:   要建立之游標的名稱。此名稱必須與工作階段中任何其他作用中游標的名稱不同。

`BINARY`
:   使游標以二進位格式而非文字格式傳回資料。

`ASENSITIVE`<br>`INSENSITIVE`
:   游標敏感度決定了：在游標宣告之後、於同一交易中對游標底層資料所做的變更，在該游標中是否可見。`INSENSITIVE` 表示這些變更不可見，`ASENSITIVE` 表示此行為取決於實作。第三種行為 `SENSITIVE`（表示這類變更在游標中可見）在 PostgreSQL 中無法使用。在 PostgreSQL 中，所有游標都是不敏感的（insensitive）；因此這些關鍵字沒有作用，只是為了與 SQL 標準相容而被接受。

    同時指定 `INSENSITIVE` 與 `FOR UPDATE` 或 `FOR SHARE` 是錯誤的。

`SCROLL`<br>`NO SCROLL`
:   `SCROLL` 指定游標可以用非循序的方式（例如向後）擷取資料列。視查詢執行計畫的複雜度而定，指定 `SCROLL` 可能會對查詢的執行時間造成效能損失。`NO SCROLL` 指定游標不能用非循序的方式擷取資料列。預設是在某些情況下允許捲動；這與指定 `SCROLL` 並不相同。詳細資訊請參閱下方的[注意事項](sql-declare.md#SQL-DECLARE-NOTES)。

`WITH HOLD`<br>`WITHOUT HOLD`
:   `WITH HOLD` 指定在建立游標的交易成功提交之後，該游標仍可以繼續使用。`WITHOUT HOLD` 指定游標不能在建立它的交易之外使用。若既未指定 `WITHOUT HOLD`，也未指定 `WITH HOLD`，則預設為 `WITHOUT HOLD`。

*`query`*
:   一個 [`SELECT`](sql-select.md) 或 [`VALUES`](sql-values.md) 命令，用來提供游標所要傳回的資料列。

關鍵字 `ASENSITIVE`、`BINARY`、`INSENSITIVE` 與 `SCROLL` 可以任意順序出現。

<a id="SQL-DECLARE-NOTES"></a>

## 注意事項

一般游標以文字格式傳回資料，與 `SELECT` 所產生的相同。`BINARY` 選項指定游標應該以二進位格式傳回資料。這可以減少伺服器與用戶端雙方的轉換工作，代價是程式設計師需要花更多心力處理與平台相依的二進位資料格式。舉例來說，若查詢從整數欄位傳回一個為 1 的值，使用預設游標時您會得到字串 `1`，而使用二進位游標時，您會得到一個 4 位元組的欄位，內含該值的內部表示法（採用 big-endian 位元組順序）。

二進位游標應謹慎使用。許多應用程式（包括 psql）並未準備好處理二進位游標，而是預期資料以文字格式傳回。

### 注意

當用戶端應用程式使用「延伸查詢」協定發出 `FETCH` 命令時，Bind 協定訊息會指定以文字或二進位格式擷取資料。這項選擇會覆寫游標原本的定義方式。因此，在使用延伸查詢協定時，二進位游標這個概念本身已經過時——任何游標都可以被視為文字或二進位格式。

除非指定了 `WITH HOLD`，否則此命令所建立的游標只能在目前交易內使用。因此，沒有 `WITH HOLD` 的 `DECLARE` 在交易區塊之外是沒有用的：游標只會存續到該陳述式完成為止。所以，若在交易區塊之外使用這樣的命令，PostgreSQL 會回報錯誤。請使用 [`BEGIN`](sql-begin.md) 與 [`COMMIT`](sql-commit.md)（或 [`ROLLBACK`](sql-rollback.md)）來定義交易區塊。

若指定了 `WITH HOLD`，且建立游標的交易成功提交，則同一工作階段中後續的交易仍可以繼續存取該游標。（但若建立游標的交易被中止，游標就會被移除。）以 `WITH HOLD` 建立的游標，會在對它發出明確的 `CLOSE` 命令時，或在工作階段結束時關閉。在目前的實作中，保留游標（held cursor）所代表的資料列會被複製到暫存檔案或記憶體區域中，使其在後續交易中仍然可用。

當查詢包含 `FOR UPDATE` 或 `FOR SHARE` 時，不可指定 `WITH HOLD`。

定義將用於向後擷取的游標時，應該指定 `SCROLL` 選項。這是 SQL 標準所要求的。然而，為了與較早的版本相容，若游標的查詢計畫夠簡單、不需要額外的負擔就能支援向後擷取，PostgreSQL 會允許在沒有 `SCROLL` 的情況下向後擷取。不過，建議應用程式開發者不要依賴從未以 `SCROLL` 建立的游標向後擷取。若指定了 `NO SCROLL`，則在任何情況下都不允許向後擷取。

當查詢包含 `FOR UPDATE` 或 `FOR SHARE` 時，同樣不允許向後擷取；因此在這種情況下不可指定 `SCROLL`。

### 小心

可捲動的游標若呼叫任何揮發性函式（請參閱[第 36.7 節](../../server-programming/extend/xfunc-volatility.md)），可能會產生非預期的結果。當先前擷取過的資料列被重新擷取時，這些函式可能會被重新執行，或許會導致與第一次不同的結果。對於涉及揮發性函式的查詢，最好指定 `NO SCROLL`。若這樣做並不實際，一種變通方法是將游標宣告為 `SCROLL WITH HOLD`，並在從中讀取任何資料列之前提交交易。這會強制將游標的完整輸出實體化到暫存儲存空間中，使揮發性函式對每個資料列都恰好只執行一次。

若游標的查詢包含 `FOR UPDATE` 或 `FOR SHARE`，則傳回的資料列會在第一次被擷取時鎖定，方式與帶有這些選項的一般 [`SELECT`](sql-select.md) 命令相同。此外，傳回的資料列會是最新的版本。

### 小心

若游標打算與 `UPDATE ... WHERE CURRENT OF` 或 `DELETE ... WHERE CURRENT OF` 搭配使用，一般建議使用 `FOR UPDATE`。使用 `FOR UPDATE` 可以防止其他工作階段在資料列被擷取之後、被更新之前變更這些資料列。若沒有 `FOR UPDATE`，當資料列在游標建立之後已被變更時，後續的 `WHERE CURRENT OF` 命令將不會有任何作用。

使用 `FOR UPDATE` 的另一個理由是：若沒有它，當游標查詢不符合 SQL 標準對「可簡單更新」（simply updatable）的規則時（特別是，游標必須只參照一個資料表，且不使用分組或 `ORDER BY`），後續的 `WHERE CURRENT OF` 可能會失敗。不是可簡單更新的游標可能可以運作，也可能無法運作，取決於計畫選擇的細節；因此在最糟的情況下，應用程式可能在測試時正常運作，到了正式環境卻失敗。若指定了 `FOR UPDATE`，就能保證游標是可更新的。

不將 `FOR UPDATE` 與 `WHERE CURRENT OF` 搭配使用的主要理由，是您需要游標可以捲動，或需要游標與並行更新隔離（也就是持續顯示舊資料）的情況。若這是必要條件，請特別留意上述的注意事項。

SQL 標準只在嵌入式 SQL 中為游標做了規定。PostgreSQL 伺服器並未實作游標的 `OPEN` 陳述式；游標在宣告時即被視為已開啟。不過，ECPG（PostgreSQL 的嵌入式 SQL 前置處理器）支援標準 SQL 的游標慣例，包括涉及 `DECLARE` 與 `OPEN` 陳述式的慣例。

開啟中游標底層的伺服器資料結構稱為 *portal*。portal 名稱會在用戶端協定中公開：用戶端若知道 portal 名稱，就可以直接從開啟中的 portal 擷取資料列。使用 `DECLARE` 建立游標時，portal 名稱與游標名稱相同。

您可以查詢 [`pg_cursors`](../../internals/views/view-pg-cursors.md) 系統檢視表，查看所有可用的游標。

<a id="id-1.9.3.99.10"></a>

## 範例

宣告一個游標：

```

DECLARE liahona CURSOR FOR SELECT * FROM films;
```

更多游標使用範例，請參閱 [FETCH](sql-fetch.md)。

<a id="id-1.9.3.99.11"></a>

## 相容性

SQL 標準只允許在嵌入式 SQL 與模組中使用游標。PostgreSQL 允許以互動方式使用游標。

依據 SQL 標準，`UPDATE ... WHERE CURRENT OF` 與 `DELETE ... WHERE CURRENT OF` 陳述式對不敏感游標所做的變更，在同一個游標中是可見的。PostgreSQL 對這些陳述式的處理方式與其他所有資料變更陳述式相同，也就是這些變更在不敏感游標中不可見。

二進位游標是 PostgreSQL 擴充功能。

<a id="id-1.9.3.99.12"></a>

## 另請參閱

[CLOSE](sql-close.md), [FETCH](sql-fetch.md), [MOVE](sql-move.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-declare.html)（原文版本：18.6；核對日期：2026-10-03）
