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

### 參數

_`name`_

要建立的規則名稱。這必須與同一個資料表的其他規則名稱不同。同一個資料表和相同事件類型的多個規會按字母順序套用。

_`event`_

此事件是 SELECT，INSERT，UPDATE 或 DELETE 之一。請注意，包含 ON CONFLICT 子句的 INSERT 不能用於具有 INSERT 或 UPDATE 規則的資料表。請考慮使用可更新檢視表。

_`table_name`_

規則適用的資料表或檢視表名稱（可加上綱要名稱）。

_`condition`_

任何 SQL 條件表示式（回傳布林值）。條件表示式不能引用除 NEW 和 OLD 之外的任何資料表，也不能包含彙總函數。

`INSTEAD`

INSTEAD 表示應該執行此指令而不是原始指令。

`ALSO`

ALSO 表示除原始指令外還應該執行此命令。

如果既未指定 ALSO 也未指定 INSTEAD，則 ALSO 是預設行為。

_`command`_

組成規則操作的指令。有效指令是 SELECT，INSERT，UPDATE，DELETE 或 NOTIFY。

在條件和指令中，特殊資料表名稱 NEW 和 OLD 可用於引用資料表中的值。NEW 在 ON INSERT 和 ON UPDATE 規則中有效，用於引用要插入或更新的新資料列。OLD 在 ON UPDATE 和 ON DELETE 規則中有效，以引用正在更新或刪除的現有資料列。

### 注意

您必須是資料表的擁有者才能為其建立或變更規則。

在檢視表中的 INSERT，UPDATE 或 DELETE 規則中，您可以加入一個發出檢視表欄位的 RETURNING 子句。如果規則分別由 INSERT RETURNING，UPDATE RETURNING 或 DELETE RETURNING 指令觸發，則此子句將用於計算輸出。當規則由沒有 RETURNING 的指令觸發時，將忽略規則的 RETURNING 子句。目前實作上只允許無條件的 INSTEAD 規則包含 RETURNING；此外，同一事件的所有規則中最多只能有一個 RETURNING 子句。（這可確保只有一個候選 RETURNING 子句用於計算結果。）如果任何可用規則中沒有 RETURNING 子句，則將拒絕對檢視表的 RETURNING 查詢。

注意避免循環規則非常重要。例如，雖然 PostgreSQL 接受以下兩個規則定義中，但由於規則的遞迴擴展，SELECT 指令會導致 PostgreSQL 回報錯誤：

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

目前，如果規則操作包含 NOTIFY 指令的話，NOTIFY 指令將無條件執行。也就是即使沒有規則應該套用的任何資料，也會發出 NOTIFY。例如，在：

```text
CREATE RULE notify_me AS ON UPDATE TO mytable DO ALSO NOTIFY mytable;

UPDATE mytable SET name = 'foo' WHERE id = 42;
```

在 UPDATE 期間將發送一個 NOTIFY 事件，無論是否存在與條件 id = 42 相符的資料列。這是可能在未來版本中修補的實作限制。

### 相容性

CREATE RULE 是一個 PostgreSQL 延伸語法，整個查詢語句重寫系統也是。

### 參閱

[ALTER RULE](alter-rule.md), [DROP RULE](drop-rule.md)

