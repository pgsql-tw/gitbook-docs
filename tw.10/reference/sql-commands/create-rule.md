---
description: 版本：10
---

# CREATE RULE

CREATE RULE — 定義新的重寫規則

### 語法

```text
CREATE [ OR REPLACE ] RULE name AS ON event
    TO table_name [ WHERE condition ]
    DO [ ALSO | INSTEAD ] { NOTHING | command | ( command ; command ... ) }

where event can be one of:

    SELECT | INSERT | UPDATE | DELETE
```

### 說明

CREATE RULE 定義了套用於指定資料表或檢視表的新規則。CREATE OR REPLACE RULE 將建立新規則，或替換同一個資料表的同名現有規則。

PostgreSQL 規則系統允許人們定義要對資料庫資料表中的插入，更新或刪除的執行替代操作。粗略地說，當使用者給予資料表上的特定指令時，規則會使其執行其他指令。或者，INSTEAD 規則可以用另一個指令替換特定的指令，或者根本不執行指令。規則也用於實作 SQL 檢視表。重要的是要意識到規則實際上是命令轉換機制或巨集。轉換在指令執行開始之前發生。如果您確實希望為每個實體資料列獨立觸發操作，則可能需要使用觸發器，而不是規則。有關規則系統的更多訊息，請參閱[第 40 章](../../server-programming/the-rule-system/)。

目前，ON SELECT 規則必須是無條件的 INSTEAD 規則，並且必須具有由單個SELECT 指令組成的操作。因此，ON SELECT 規則有效地將資料表轉換為檢視表，其可見內容是由規則的 SELECT 指令回傳的資料列，而不是資料表中儲存的任何內容（如果有的話）。撰寫 CREATE VIEW 指令比建立實際資料表並為其定義 ON SELECT 規則被認為是更好的方式。

您可以透過定義 ON INSERT，ON UPDATE 和 ON DELETE 規則（或任何足以滿足目的的子集）來建立可更新檢視表的錯覺，以使用其他資料表上的適當更新替換檢視表上的更新操作。如果要支援 INSERT RETURNING 等，請務必在每個規則中加上適當的 RETURNING 子句。

如果您嘗試對複雜的檢視表更新使用條件規則，則會有一個問題：對於您希望在檢視表上允許的每個操作，必須有一個無條件的 INSTEAD 規則。 如果規則是有條件的，或者不是 INSTEAD，那麼系統仍將拒絕執行更新操作的嘗試，因為它認為在某些情況下它可能最終會嘗試在檢視表的虛擬資料表上執行操作。如果要處理條件規則中的所有有用情況，請加上無條件 DO INSTEAD NOTHING 規則以確保系統知道它永遠不會被呼叫去更新虛擬資料表。然後使條件規則非 INSTEAD；在套用它們的情況下，它們會加到預設的 INSTEAD NOTHING 操作。（但是，此方法目前不支援 RETURNING 查詢。）

**注意**  
一個簡單到可自動更新的檢視表（請參閱 [CREATE VIEW](create-view.md#ke-geng-xin-de-biao-updatable-views)）不需要使用者建立的規則便可更新。雖然您仍然可以建立明確的規則，但自動更新轉換通常會優於規則。

值得考慮的另一個選擇是使用 INSTEAD OF 觸發器（請參閱 [CREATE TRIGGER](create-trigger.md)）代替規則。

### Parameters

_`name`_

The name of a rule to create. This must be distinct from the name of any other rule for the same table. Multiple rules on the same table and same event type are applied in alphabetical name order.

_`event`_

The event is one of `SELECT`, `INSERT`, `UPDATE`, or `DELETE`. Note that an `INSERT` containing an `ON CONFLICT` clause cannot be used on tables that have either `INSERT` or `UPDATE` rules. Consider using an updatable view instead.

_`table_name`_

The name \(optionally schema-qualified\) of the table or view the rule applies to.

_`condition`_

Any SQL conditional expression \(returning `boolean`\). The condition expression cannot refer to any tables except `NEW` and `OLD`, and cannot contain aggregate functions.

`INSTEAD`

`INSTEAD` indicates that the commands should be executed _instead of_ the original command.

`ALSO`

`ALSO` indicates that the commands should be executed _in addition to_ the original command.

If neither `ALSO` nor `INSTEAD` is specified, `ALSO` is the default.

_`command`_

The command or commands that make up the rule action. Valid commands are `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `NOTIFY`.

Within _`condition`_ and _`command`_, the special table names `NEW` and `OLD` can be used to refer to values in the referenced table. `NEW` is valid in `ON INSERT` and `ON UPDATE` rules to refer to the new row being inserted or updated. `OLD` is valid in `ON UPDATE` and `ON DELETE` rules to refer to the existing row being updated or deleted.

### Notes

You must be the owner of a table to create or change rules for it.

In a rule for `INSERT`, `UPDATE`, or `DELETE` on a view, you can add a `RETURNING` clause that emits the view's columns. This clause will be used to compute the outputs if the rule is triggered by an `INSERT RETURNING`, `UPDATE RETURNING`, or `DELETE RETURNING` command respectively. When the rule is triggered by a command without `RETURNING`, the rule's `RETURNING` clause will be ignored. The current implementation allows only unconditional `INSTEAD` rules to contain `RETURNING`; furthermore there can be at most one `RETURNING` clause among all the rules for the same event. \(This ensures that there is only one candidate `RETURNING` clause to be used to compute the results.\) `RETURNING` queries on the view will be rejected if there is no `RETURNING`clause in any available rule.

It is very important to take care to avoid circular rules. For example, though each of the following two rule definitions are accepted by PostgreSQL, the `SELECT` command would causePostgreSQL to report an error because of recursive expansion of a rule:

```text
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

Presently, if a rule action contains a `NOTIFY` command, the `NOTIFY` command will be executed unconditionally, that is, the `NOTIFY` will be issued even if there are not any rows that the rule should apply to. For example, in:

```text
CREATE RULE notify_me AS ON UPDATE TO mytable DO ALSO NOTIFY mytable;

UPDATE mytable SET name = 'foo' WHERE id = 42;
```

one `NOTIFY` event will be sent during the `UPDATE`, whether or not there are any rows that match the condition `id = 42`. This is an implementation restriction that might be fixed in future releases.

### 相容性

CREATE RULE 是一個 PostgreSQL 延伸語法，整個查詢語句重寫系統也是。

### 參閱

[ALTER RULE](alter-rule.md), [DROP RULE](drop-rule.md)

