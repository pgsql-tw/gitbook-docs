<a id="id-1.9.3.155.1"></a>

## LOCK

LOCK — 鎖定一個資料表

<a id="id-1.9.3.155.2"></a>

## 語法

```

LOCK [ TABLE ] [ ONLY ] name [ * ] [, ...] [ IN lockmode MODE ] [ NOWAIT ]

where lockmode is one of:

    ACCESS SHARE | ROW SHARE | ROW EXCLUSIVE | SHARE UPDATE EXCLUSIVE
    | SHARE | SHARE ROW EXCLUSIVE | EXCLUSIVE | ACCESS EXCLUSIVE
```

<a id="id-1.9.3.155.5"></a>

## 說明

`LOCK TABLE` 會取得資料表層級的鎖定，必要時會等待任何互相衝突的鎖定被釋放。若指定了 `NOWAIT`，`LOCK TABLE` 就不會等待取得所要的鎖定：若無法立即取得，指令會中止並發出錯誤。鎖定一旦取得，就會在目前交易剩餘的時間內持續保持。（沒有 `UNLOCK TABLE` 指令；鎖定一律會在交易結束時釋放。）

鎖定檢視表時，出現在該檢視表定義查詢中的所有關聯（relation）也會以相同的鎖定模式遞迴地一併鎖定。

當 PostgreSQL 為參照資料表的指令自動取得鎖定時，一律會使用可能範圍內限制最少的鎖定模式。`LOCK TABLE` 則是為了因應你可能需要更嚴格鎖定的情況而提供的。舉例來說，假設某個應用程式以 `READ COMMITTED` 隔離等級執行交易，並且需要確保資料表中的資料在整個交易期間維持穩定。為達成此目的，你可以在查詢之前先取得該資料表的 `SHARE` 鎖定模式。這樣可以防止並行的資料變更，並確保後續對該資料表的讀取都能看到一份穩定的已提交資料檢視，因為 `SHARE` 鎖定模式會與寫入者所取得的 `ROW EXCLUSIVE` 鎖定衝突，你的 `LOCK TABLE name IN SHARE MODE` 陳述式會一直等到任何並行持有 `ROW EXCLUSIVE` 模式鎖定的交易提交或回復為止。因此，一旦你取得該鎖定，就不會有尚未完成的未提交寫入；此外，在你釋放該鎖定之前，也不會有新的寫入能夠開始。

若要在以 `REPEATABLE READ` 或 `SERIALIZABLE` 隔離等級執行交易時達到類似的效果，你必須在執行任何 `SELECT` 或資料修改陳述式之前，先執行 `LOCK TABLE` 陳述式。`REPEATABLE READ` 或 `SERIALIZABLE` 交易對資料的檢視，會在其第一個 `SELECT` 或資料修改陳述式開始時被凍結。在交易稍後才執行的 `LOCK TABLE`，仍然可以防止並行寫入——但無法確保該交易所讀到的內容對應到最新已提交的值。

若這類交易將要變更資料表中的資料，就應該使用 `SHARE ROW EXCLUSIVE` 鎖定模式，而非 `SHARE` 模式。這可確保同一時間只會有一個這類交易在執行。若不這麼做，就有可能發生死結：兩個交易可能都先取得了 `SHARE` 模式，之後卻都無法再取得 `ROW EXCLUSIVE` 模式來實際執行更新。（請注意，交易自身的鎖定永遠不會互相衝突，因此某交易在持有 `SHARE` 模式時可以取得 `ROW EXCLUSIVE` 模式——但若有其他人持有 `SHARE` 模式，則無法取得。）為避免死結，請確保所有交易都以相同的順序在相同的物件上取得鎖定；若同一物件牽涉多種鎖定模式，交易應一律先取得限制最嚴格的模式。

關於鎖定模式與鎖定策略的更多資訊，請參閱[第 13.3 節](../../the-sql-language/mvcc/explicit-locking.md)。

<a id="id-1.9.3.155.6"></a>

## 參數

*`name`*
:   要鎖定的既有資料表名稱（可加上綱要限定）。若在資料表名稱前指定了 `ONLY`，就只會鎖定該資料表本身。若未指定 `ONLY`，則該資料表及其所有子資料表（如果有的話）都會被鎖定。你也可以選擇在資料表名稱後加上 `*`，明確表示要包含子資料表。

    指令 `LOCK TABLE a, b;` 等同於 `LOCK TABLE a; LOCK TABLE b;`。這些資料表會依照 `LOCK TABLE` 指令中所指定的順序逐一鎖定。

*`lockmode`*
:   鎖定模式指定此鎖定會與哪些鎖定衝突。鎖定模式的說明請參閱[第 13.3 節](../../the-sql-language/mvcc/explicit-locking.md)。

    若未指定鎖定模式，則會使用限制最嚴格的模式 `ACCESS EXCLUSIVE`。

`NOWAIT`
:   指定 `LOCK TABLE` 不應等待任何互相衝突的鎖定被釋放：若無法在不等待的情況下立即取得指定的鎖定，該交易即會中止。

<a id="id-1.9.3.155.7"></a>

## 注意事項

若要鎖定一個資料表，使用者必須具備所指定 *`lockmode`* 所需的適當權限。若使用者對該資料表擁有 `MAINTAIN`、`UPDATE`、`DELETE` 或 `TRUNCATE` 權限，即可使用任何 *`lockmode`*。若使用者對該資料表擁有 `INSERT` 權限，則可使用 `ROW EXCLUSIVE MODE`（或[第 13.3 節](../../the-sql-language/mvcc/explicit-locking.md)所述、衝突性較低的模式）。若使用者對該資料表擁有 `SELECT` 權限，則可使用 `ACCESS SHARE MODE`。

對檢視表執行鎖定的使用者，必須對該檢視表擁有相應的權限。此外，依預設，該檢視表的擁有者必須對其底層的基礎關聯擁有相關權限，而執行鎖定的使用者則不需要對底層的基礎關聯擁有任何權限。不過，若該檢視表已將 `security_invoker` 設為 `true`（請參閱 [`CREATE VIEW`](sql-createview.md)），則執行鎖定的使用者本身（而非檢視表擁有者）必須對底層的基礎關聯擁有相關權限。

`LOCK TABLE` 在交易區塊之外沒有任何用處：鎖定只會保持到該陳述式完成為止。因此，若在交易區塊之外使用 `LOCK`，PostgreSQL 會回報錯誤。請使用 [`BEGIN`](sql-begin.md) 與 [`COMMIT`](sql-commit.md)（或 [`ROLLBACK`](sql-rollback.md)）來定義交易區塊。

`LOCK TABLE` 只處理資料表層級的鎖定，因此所有含有 `ROW` 字樣的模式名稱其實都是用詞不當。這些模式名稱一般應理解為表示使用者打算在已鎖定的資料表內取得資料列層級鎖定的意圖。此外，`ROW EXCLUSIVE` 模式是一種可共用的資料表鎖定。請記住，就 `LOCK TABLE` 而言，所有鎖定模式的語義都相同，差異僅在於哪些模式會與哪些模式互相衝突的規則。關於如何取得實際的資料列層級鎖定，請參閱[第 13.3.2 節](../../the-sql-language/mvcc/explicit-locking.md#LOCKING-ROWS)，以及 [SELECT](sql-select.md) 文件中的[鎖定子句](sql-select.md#SQL-FOR-UPDATE-SHARE)。

<a id="id-1.9.3.155.8"></a>

## 範例

在即將對外鍵資料表執行插入操作之前，對主鍵資料表取得 `SHARE` 鎖定：

```

BEGIN WORK;
LOCK TABLE films IN SHARE MODE;
SELECT id FROM films
    WHERE name = 'Star Wars: Episode I - The Phantom Menace';
-- Do ROLLBACK if record was not returned
INSERT INTO films_user_comments VALUES
    (_id_, 'GREAT! I was waiting for it for so long!');
COMMIT WORK;
```

即將執行刪除操作時，對主鍵資料表取得 `SHARE ROW EXCLUSIVE` 鎖定：

```

BEGIN WORK;
LOCK TABLE films IN SHARE ROW EXCLUSIVE MODE;
DELETE FROM films_user_comments WHERE id IN
    (SELECT id FROM films WHERE rating < 5);
DELETE FROM films WHERE rating < 5;
COMMIT WORK;
```

<a id="id-1.9.3.155.9"></a>

## 相容性

SQL 標準中沒有 `LOCK TABLE`，而是改用 `SET TRANSACTION` 來指定交易的並行等級。PostgreSQL 也支援這種方式；詳情請參閱 [SET TRANSACTION](sql-set-transaction.md)。

除了 `ACCESS SHARE`、`ACCESS EXCLUSIVE` 與 `SHARE UPDATE EXCLUSIVE` 鎖定模式之外，PostgreSQL 的鎖定模式與 `LOCK TABLE` 語法，都與 Oracle 中所提供的相容。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-lock.html)（原文版本：18.6；核對日期：2026-09-28）
