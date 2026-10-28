<a id="SQL-CREATERULE"></a><a id="id-1.9.3.79.1"></a>

## CREATE RULE

CREATE RULE — 定義新的重寫規則

<a id="id-1.9.3.79.4"></a>

## 語法

```

CREATE [ OR REPLACE ] RULE name AS ON event
    TO table_name [ WHERE condition ]
    DO [ ALSO | INSTEAD ] { NOTHING | command | ( command ; command ... ) }

where event can be one of:

    SELECT | INSERT | UPDATE | DELETE
```

<a id="id-1.9.3.79.5"></a>

## 說明

`CREATE RULE` 會定義一條套用於指定資料表或檢視表的新規則。
`CREATE OR REPLACE RULE` 會建立新規則，或取代同一資料表上同名的現有規則。

PostgreSQL 的規則系統讓使用者可以定義在資料庫資料表中進行插入、更新或刪除時要執行的替代動作。粗略地說，規則會使某個資料表上的某個命令被執行時，額外執行其他命令。或者，`INSTEAD`
規則可以用另一個命令取代某個命令，或使某個命令完全不被執行。規則也被用來實作 SQL 檢視表。很重要的是要了解，規則實際上是一種命令轉換機制，或者說命令巨集。轉換發生在命令開始執行之前。若你真正想要的是針對每一筆實體資料列各自獨立觸發的操作，你大概會想使用觸發程序，而不是規則。關於規則系統的更多資訊，請參閱[第 39 章](../../server-programming/rules/README.md)。

目前，`ON SELECT` 規則只能附加到檢視表上。這種規則必須命名為 `"_RETURN"`，
必須是無條件的 `INSTEAD` 規則，且其動作必須只由單一 `SELECT` 命令組成。
這個命令定義了檢視表的可見內容。（檢視表本身基本上是一個沒有儲存空間的虛設資料表。）最好將這種規則視為實作細節。雖然可以透過 `CREATE OR REPLACE RULE "_RETURN" AS
...` 重新定義檢視表，但使用 `CREATE OR REPLACE
VIEW` 是比較好的寫法。

你可以定義 `ON INSERT`、`ON UPDATE` 與
`ON DELETE` 規則（或這些規則中足以滿足你需求的任何子集），以其他資料表上的適當更新來取代檢視表上的更新動作，藉此營造出可更新檢視表的效果。若你想要支援
`INSERT RETURNING` 等功能，請務必在這些規則中各自放入適當的
`RETURNING` 子句。

若你嘗試使用條件式規則來處理複雜的檢視表更新，有一個陷阱：對於你希望在檢視表上允許的每一種動作，都*必須*有一條無條件的
`INSTEAD` 規則。若規則是條件式的，或不是
`INSTEAD` 規則，系統仍會拒絕執行更新動作的嘗試，因為它認為在某些情況下，最後可能會嘗試對檢視表的虛設資料表執行該動作。若你想在條件式規則中處理所有有用的情況，請加上一條無條件的 `DO
INSTEAD NOTHING` 規則，以確保系統了解它永遠不會被要求去更新虛設資料表。
接著將條件式規則設為非 `INSTEAD` 規則；在這些規則被套用的情況下，它們會附加在預設的
`INSTEAD NOTHING` 動作之上。（不過，此方法目前無法用來支援 `RETURNING` 查詢。）

<a id="id-1.9.3.79.5.7"></a>

### 注意

足夠簡單而可自動更新的檢視表（請參閱 [CREATE VIEW](sql-createview.md)）不需要使用者建立的規則就能更新。雖然你仍然可以建立明確的規則，但自動更新轉換的效能通常會優於明確的規則。

另一個值得考慮的替代方案，是使用 `INSTEAD OF`
觸發程序（請參閱 [CREATE TRIGGER](sql-createtrigger.md)）來取代規則。

<a id="id-1.9.3.79.6"></a>

## 參數

*`name`*
:   要建立之規則的名稱。它必須與同一資料表上任何其他規則的名稱不同。同一資料表上、相同事件類型的多條規則會依名稱的字母順序套用。

*`event`*
:   事件是 `SELECT`、
    `INSERT`、`UPDATE` 或
    `DELETE` 其中之一。請注意，含有 `ON
    CONFLICT` 子句的
    `INSERT` 不能用在具有
    `INSERT` 或 `UPDATE`
    規則的資料表上。請考慮改用可更新檢視表。

*`table_name`*
:   規則所套用之資料表或檢視表的名稱（可選擇以綱要限定）。

*`condition`*
:   任何 SQL 條件運算式（回傳
    `boolean`）。條件運算式不能引用 `NEW` 與 `OLD` 以外的任何資料表，也不能包含彙總函式。

`INSTEAD`
:   `INSTEAD` 表示這些命令應該*取代*原始命令來執行。

`ALSO`

`ALSO` 表示這些命令應該在原始命令*之外額外*執行。

若既未指定 `ALSO`，也未指定
`INSTEAD`，則預設為 `ALSO`。

*`command`*
:   構成規則動作的一個或多個命令。有效的命令為 `SELECT`、
    `INSERT`、`UPDATE`、
    `DELETE` 或 `NOTIFY`。

在 *`condition`* 與
*`command`* 中，可以使用特殊資料表名稱 `NEW` 與 `OLD`
來引用所參照資料表中的值。
`NEW` 在 `ON INSERT` 與
`ON UPDATE` 規則中有效，用來引用正在插入或更新的新資料列。`OLD` 在
`ON UPDATE` 與 `ON DELETE` 規則中有效，用來引用正在更新或刪除的現有資料列。

<a id="id-1.9.3.79.7"></a>

## 注意事項

你必須是資料表的擁有者，才能為它建立或變更規則。

在檢視表上針對 `INSERT`、`UPDATE` 或
`DELETE` 的規則中，你可以加上會輸出檢視表欄位的 `RETURNING`
子句。若規則分別由 `INSERT RETURNING`、
`UPDATE RETURNING` 或 `DELETE RETURNING` 命令觸發，此子句會被用來計算輸出。當規則由不含
`RETURNING` 的命令觸發時，規則的 `RETURNING` 子句會被忽略。目前的實作只允許無條件的
`INSTEAD` 規則包含 `RETURNING`；此外，同一事件的所有規則之中，最多只能有一個 `RETURNING` 子句。（這確保只有一個候選的
`RETURNING` 子句可用來計算結果。）
若所有可用的規則中都沒有 `RETURNING` 子句，則檢視表上的 `RETURNING` 查詢會被拒絕。

務必非常小心，避免循環規則。例如，雖然下列兩個規則定義各自都會被 PostgreSQL 接受，但
`SELECT` 命令會因為規則的遞迴展開，而導致
PostgreSQL 回報錯誤：

```

CREATE RULE "_RETURN" AS
    ON SELECT TO t1
    DO INSTEAD
        SELECT * FROM t2;

CREATE RULE "_RETURN" AS
    ON SELECT TO t2
    DO INSTEAD
        SELECT * FROM t1;

SELECT * FROM t1;
```

目前，若規則動作包含 `NOTIFY`
命令，該 `NOTIFY` 命令會無條件執行，也就是說，即使沒有任何規則應套用的資料列，仍會發出 `NOTIFY`。例如，在：

```

CREATE RULE notify_me AS ON UPDATE TO mytable DO ALSO NOTIFY mytable;

UPDATE mytable SET name = 'foo' WHERE id = 42;
```

中，不論是否有任何資料列符合條件 `id = 42`，在
`UPDATE` 期間都會送出一個 `NOTIFY` 事件。這是實作上的限制，可能會在未來的版本中修正。

<a id="id-1.9.3.79.8"></a>

## 相容性

`CREATE RULE` 是
PostgreSQL 的語言擴充，整個查詢重寫系統也是如此。

<a id="id-1.9.3.79.9"></a>

## 另請參閱

[ALTER RULE](sql-alterrule.md), [DROP RULE](sql-droprule.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createrule.html)（原文版本：18.6；核對日期：2026-10-04）
