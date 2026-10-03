<a id="SQL-CREATEVIEW"></a><a id="id-1.9.3.97.1"></a>

## CREATE VIEW

CREATE VIEW — 定義新的檢視表

<a id="id-1.9.3.97.4"></a>

## 語法

```

CREATE [ OR REPLACE ] [ TEMP | TEMPORARY ] [ RECURSIVE ] VIEW name [ ( column_name [, ...] ) ]
    [ WITH ( view_option_name [= view_option_value] [, ... ] ) ]
    AS query
    [ WITH [ CASCADED | LOCAL ] CHECK OPTION ]
```

<a id="id-1.9.3.97.5"></a>

## 說明

`CREATE VIEW` 會定義一個查詢的檢視表。檢視表並不會實體具體化；而是在每次查詢中參照該檢視表時執行其查詢。

`CREATE OR REPLACE VIEW` 與此類似，但若已存在同名的檢視表，則會將其取代。新的查詢必須產生與現有檢視表查詢所產生的相同欄位（也就是相同的欄位名稱、相同的順序以及相同的資料型別），但可以在清單的結尾加入額外的欄位。產生輸出欄位的計算方式則可以完全不同。

若指定了綱要名稱（例如 `CREATE VIEW
myschema.myview ...`），檢視表就會建立在指定的綱要中；否則會建立在目前的綱要中。暫存檢視表存在於一個特殊的綱要中，因此建立暫存檢視表時不能指定綱要名稱。檢視表的名稱必須與同一綱要中任何其他關聯（資料表、序列、索引、檢視表、具體化檢視表或外部資料表）的名稱不同。

<a id="id-1.9.3.97.6"></a>

## 參數

`TEMPORARY` 或 `TEMP`
:   若有指定，檢視表會建立為暫存檢視表。暫存檢視表會在目前工作階段結束時自動移除。當暫存檢視表存在時，目前工作階段將看不到同名的現有永久關聯，除非以綱要限定的名稱參照它們。

    若檢視表所參照的任何資料表是暫存的，則該檢視表會建立為暫存檢視表（無論是否指定了 `TEMPORARY`）。

`RECURSIVE` <a id="id-1.9.3.97.6.2.2.1.2"></a>
:   建立遞迴檢視表。語法

    ```

    CREATE RECURSIVE VIEW [ schema . ] view_name (column_names) AS SELECT ...;
    ```

    等同於

    ```

    CREATE VIEW [ schema . ] view_name AS WITH RECURSIVE view_name (column_names) AS (SELECT ...) SELECT column_names FROM view_name;
    ```

    遞迴檢視表必須指定檢視表欄位名稱清單。

*`name`*
:   要建立的檢視表名稱（可選擇以綱要限定）。

*`column_name`*
:   選用的名稱清單，用作檢視表的欄位名稱。若未指定，欄位名稱會從查詢中推導而來。

`WITH ( view_option_name [= view_option_value] [, ... ] )`
:   此子句為檢視表指定選用參數；支援下列參數：

    `check_option` (`enum`)
    :   此參數可以是 `local` 或 `cascaded`，等同於指定 `WITH [ CASCADED | LOCAL ] CHECK OPTION`（見下文）。

    `security_barrier` (`boolean`)
    :   若檢視表是用來提供資料列層級安全性，就應該使用此參數。完整細節請參閱[第 39.5 節](../../server-programming/rules/rules-privileges.md)。

    `security_invoker` (`boolean`)
    :   此選項會讓底層的基礎關聯依據檢視表使用者的權限進行檢查，而不是依據檢視表擁有者的權限。完整細節請參閱下方的注意事項。

    以上所有選項都可以使用 [`ALTER VIEW`](sql-alterview.md) 在現有的檢視表上變更。

*`query`*
:   提供檢視表欄位與資料列的 [`SELECT`](sql-select.md) 或 [`VALUES`](sql-values.md) 命令。

`WITH [ CASCADED | LOCAL ] CHECK OPTION` <a id="id-1.9.3.97.6.2.7.1.2"></a> <a id="id-1.9.3.97.6.2.7.1.3"></a>
:   此選項控制可自動更新之檢視表的行為。指定此選項時，會檢查對該檢視表執行的 `INSERT`、`UPDATE` 與 `MERGE` 命令，以確保新的資料列滿足檢視表的定義條件（也就是檢查新的資料列，確保它們可以透過該檢視表看見）。若不滿足，該更新就會被拒絕。若未指定 `CHECK OPTION`，則允許對該檢視表執行的 `INSERT`、`UPDATE` 與 `MERGE` 命令建立無法透過該檢視表看見的資料列。支援下列檢查選項：

    `LOCAL`
    :   新的資料列只會依據直接定義在該檢視表本身的條件進行檢查。定義在底層基礎檢視表上的任何條件都不會被檢查（除非它們也指定了 `CHECK OPTION`）。

    `CASCADED`
    :   新的資料列會依據該檢視表以及所有底層基礎檢視表的條件進行檢查。若指定了 `CHECK OPTION`，且既未指定 `LOCAL`，也未指定 `CASCADED`，則假定為 `CASCADED`。

    `CHECK OPTION` 不可以用於 `RECURSIVE` 檢視表。

    請注意，`CHECK OPTION` 只支援可自動更新、且沒有 `INSTEAD OF` 觸發程序或 `INSTEAD` 規則的檢視表。若可自動更新的檢視表是定義在具有 `INSTEAD OF` 觸發程序的基礎檢視表之上，則可以使用 `LOCAL CHECK OPTION` 檢查該可自動更新檢視表上的條件，但具有 `INSTEAD OF` 觸發程序之基礎檢視表上的條件將不會被檢查（串聯（cascaded）檢查選項不會向下串聯到可經由觸發程序更新的檢視表，而直接定義在可經由觸發程序更新之檢視表上的任何檢查選項都會被忽略）。若該檢視表或其任何基礎關聯具有會使 `INSERT` 或 `UPDATE` 命令被重寫的 `INSTEAD` 規則，則在重寫後的查詢中會忽略所有檢查選項，包括來自定義在該具有 `INSTEAD` 規則之關聯之上的可自動更新檢視表的任何檢查。若該檢視表或其任何基礎關聯具有規則，則不支援 `MERGE`。

<a id="id-1.9.3.97.7"></a>

## 注意事項

請使用 [`DROP VIEW`](sql-dropview.md) 陳述式移除檢視表。

請留意檢視表欄位的名稱與型別是否會依你想要的方式指定。例如：

```

CREATE VIEW vista AS SELECT 'Hello World';
```

是不好的寫法，因為欄位名稱預設為 `?column?`；此外，欄位資料型別預設為 `text`，這可能不是你想要的。在檢視表結果中使用字串常數時，較好的寫法類似這樣：

```

CREATE VIEW vista AS SELECT text 'Hello World' AS hello;
```

預設情況下，對檢視表中所參照之底層基礎關聯的存取，是由檢視表擁有者的權限決定。在某些情況下，這可以用來提供對底層資料表安全但受限的存取。不過，並非所有檢視表都能防止竄改；詳細資訊請參閱[第 39.5 節](../../server-programming/rules/rules-privileges.md)。

若檢視表的 `security_invoker` 屬性設為 `true`，則對底層基礎關聯的存取是由執行查詢之使用者的權限決定，而不是由檢視表擁有者的權限決定。因此，security invoker 檢視表的使用者必須擁有該檢視表及其底層基礎關聯的相關權限。

若任何底層基礎關聯是 security invoker 檢視表，它會被視為直接從原始查詢存取一樣來處理。因此，security invoker 檢視表一律會使用目前使用者的權限檢查其底層基礎關聯，即使它是從沒有 `security_invoker` 屬性的檢視表存取的也是如此。

若任何底層基礎關聯啟用了[資料列層級安全性](../../the-sql-language/ddl/ddl-rowsecurity.md)，則預設會套用檢視表擁有者的資料列層級安全性政策，而對這些政策所參照之任何其他關聯的存取，則由檢視表擁有者的權限決定。不過，若檢視表的 `security_invoker` 設為 `true`，則會改用呼叫者的政策與權限，如同基礎關聯是直接從使用該檢視表的查詢中參照一樣。

在檢視表中呼叫的函式，其處理方式與從使用該檢視表的查詢中直接呼叫相同。因此，檢視表的使用者必須擁有呼叫該檢視表所用之所有函式的權限。檢視表中的函式會以執行查詢之使用者或函式擁有者的權限執行，取決於函式是定義為 `SECURITY INVOKER` 還是 `SECURITY DEFINER`。因此，舉例來說，在檢視表中直接呼叫 `CURRENT_USER` 一律會傳回呼叫者，而不是檢視表擁有者。這不受檢視表的 `security_invoker` 設定影響，因此 `security_invoker` 設為 `false` 的檢視表*並不*等同於 `SECURITY DEFINER` 函式，這兩個概念不應混淆。

建立或取代檢視表的使用者必須擁有檢視表查詢中所參照之任何綱要的 `USAGE` 權限，才能在這些綱要中查找所參照的物件。不過請注意，這項查找只會在建立或取代檢視表時進行。因此，檢視表的使用者只需要擁有包含該檢視表之綱要的 `USAGE` 權限，而不需要擁有檢視表查詢中所參照之綱要的 USAGE 權限，即使是 security invoker 檢視表也是如此。

在現有檢視表上使用 `CREATE OR REPLACE VIEW` 時，只會變更檢視表定義用的 SELECT 規則，以及任何 `WITH ( ... )` 參數與其 `CHECK OPTION`。其他檢視表屬性，包括擁有權、權限以及非 SELECT 規則，都維持不變。你必須擁有該檢視表才能取代它（這包括身為擁有該檢視表之角色的成員）。

<a id="SQL-CREATEVIEW-UPDATABLE-VIEWS"></a>

### 可更新的檢視表

<a id="id-1.9.3.97.7.11.2"></a>

簡單的檢視表可自動更新：系統允許對該檢視表使用 `INSERT`、`UPDATE`、`DELETE` 與 `MERGE` 陳述式，方式與一般資料表相同。若檢視表滿足下列所有條件，即可自動更新：

* 檢視表的 `FROM` 清單中必須恰好只有一個項目，且該項目必須是資料表或另一個可更新的檢視表。
* 檢視表定義的最上層不得包含 `WITH`、`DISTINCT`、`GROUP BY`、`HAVING`、`LIMIT` 或 `OFFSET` 子句。
* 檢視表定義的最上層不得包含集合運算（`UNION`、`INTERSECT` 或 `EXCEPT`）。
* 檢視表的選取清單不得包含任何彙總函式、視窗函式或傳回集合的函式。

可自動更新的檢視表可以混合包含可更新與不可更新的欄位。若某個欄位是對底層基礎關聯中可更新欄位的簡單參照，則該欄位是可更新的；否則該欄位為唯讀，若 `INSERT`、`UPDATE` 或 `MERGE` 陳述式嘗試為其指定值，就會引發錯誤。

若檢視表可自動更新，系統會將對該檢視表執行的任何 `INSERT`、`UPDATE`、`DELETE` 或 `MERGE` 陳述式，轉換為對底層基礎關聯執行的對應陳述式。具有 `ON
CONFLICT UPDATE` 子句的 `INSERT` 陳述式也完全支援。

若可自動更新的檢視表包含 `WHERE` 條件，該條件會限制基礎關聯中有哪些資料列可以被對該檢視表執行的 `UPDATE`、`DELETE` 與 `MERGE` 陳述式修改。不過，`UPDATE` 或 `MERGE` 被允許將資料列變更為不再滿足 `WHERE` 條件，因而不再能透過該檢視表看見。同樣地，`INSERT` 或 `MERGE` 命令可能插入不滿足 `WHERE` 條件、因而無法透過該檢視表看見的基礎關聯資料列（`ON CONFLICT UPDATE` 也可能以類似方式影響無法透過該檢視表看見的現有資料列）。可以使用 `CHECK OPTION` 防止 `INSERT`、`UPDATE` 與 `MERGE` 命令建立這類無法透過該檢視表看見的資料列。

若可自動更新的檢視表標記了 `security_barrier` 屬性，則該檢視表所有的 `WHERE` 條件（以及任何使用標記為 `LEAKPROOF` 之運算子的條件）一律會在檢視表使用者所加入的任何條件之前進行求值。完整細節請參閱[第 39.5 節](../../server-programming/rules/rules-privileges.md)。請注意，因此，最終不會被傳回的資料列（因為它們未通過使用者的 `WHERE` 條件）仍可能被鎖定。可以使用 `EXPLAIN` 查看哪些條件是在關聯層級套用（因此不會鎖定資料列），哪些不是。

不滿足所有這些條件的較複雜檢視表預設為唯讀：系統不允許對該檢視表執行 `INSERT`、`UPDATE`、`DELETE` 或 `MERGE`。你可以在該檢視表上建立 `INSTEAD OF` 觸發程序來達到可更新檢視表的效果，這些觸發程序必須將對該檢視表嘗試進行的插入等操作，轉換為對其他資料表的適當動作。更多資訊請參閱 [CREATE TRIGGER](sql-createtrigger.md)。另一種可能的做法是建立規則（請參閱 [CREATE RULE](sql-createrule.md)），但實務上觸發程序更容易理解，也更容易正確使用。另請注意，具有規則的關聯不支援 `MERGE`。

請注意，對檢視表執行插入、更新或刪除的使用者，必須擁有該檢視表對應的插入、更新或刪除權限。此外，預設情況下，檢視表的擁有者必須擁有底層基礎關聯的相關權限，而執行更新的使用者則不需要擁有底層基礎關聯的任何權限（請參閱[第 39.5 節](../../server-programming/rules/rules-privileges.md)）。不過，若檢視表的 `security_invoker` 設為 `true`，則必須擁有底層基礎關聯相關權限的是執行更新的使用者，而不是檢視表擁有者。

<a id="id-1.9.3.97.8"></a>

## 範例

建立一個由所有喜劇電影組成的檢視表：

```

CREATE VIEW comedies AS
    SELECT *
    FROM films
    WHERE kind = 'Comedy';
```

這會建立一個檢視表，其中包含建立檢視表當時 films 資料表中的欄位（原文此處誤植為 `film`，依範例 SQL 更正）。雖然建立檢視表時使用了 `*`，但之後加入該資料表的欄位不會成為檢視表的一部分。

建立具有 `LOCAL CHECK OPTION` 的檢視表：

```

CREATE VIEW universal_comedies AS
    SELECT *
    FROM comedies
    WHERE classification = 'U'
    WITH LOCAL CHECK OPTION;
```

這會建立一個以 `comedies` 檢視表為基礎的檢視表，只顯示 `kind = 'Comedy'` 且 `classification = 'U'` 的電影。若新的資料列沒有 `classification = 'U'`，則任何在此檢視表中 `INSERT` 或 `UPDATE` 資料列的嘗試都會被拒絕，但電影的 `kind` 不會被檢查。

建立具有 `CASCADED CHECK OPTION` 的檢視表：

```

CREATE VIEW pg_comedies AS
    SELECT *
    FROM comedies
    WHERE classification = 'PG'
    WITH CASCADED CHECK OPTION;
```

這會建立一個會同時檢查新資料列之 `kind` 與 `classification` 的檢視表。

建立混合包含可更新與不可更新欄位的檢視表：

```

CREATE VIEW comedies AS
    SELECT f.*,
           country_code_to_name(f.country_code) AS country,
           (SELECT avg(r.rating)
            FROM user_ratings r
            WHERE r.film_id = f.id) AS avg_rating
    FROM films f
    WHERE f.kind = 'Comedy';
```

此檢視表將支援 `INSERT`、`UPDATE` 與 `DELETE`。來自 `films` 資料表的所有欄位都將是可更新的，而計算出來的欄位 `country` 與 `avg_rating` 則是唯讀的。

建立一個由 1 到 100 的數字組成的遞迴檢視表：

```

CREATE RECURSIVE VIEW public.nums_1_100 (n) AS
    VALUES (1)
UNION ALL
    SELECT n+1 FROM nums_1_100 WHERE n < 100;
```

請注意，雖然在這個 `CREATE` 中遞迴檢視表的名稱是以綱要限定的，但其內部的自我參照並未以綱要限定。這是因為隱含建立之 CTE 的名稱不能以綱要限定。

<a id="id-1.9.3.97.9"></a>

## 相容性

`CREATE OR REPLACE VIEW` 是 PostgreSQL 的語言擴充功能。暫存檢視表的概念也是如此。`WITH ( ... )` 子句同樣是擴充功能，security barrier 檢視表與 security invoker 檢視表也是。

<a id="id-1.9.3.97.10"></a>

## 另請參閱

[ALTER VIEW](sql-alterview.md), [DROP VIEW](sql-dropview.md), [CREATE MATERIALIZED VIEW](sql-creatematerializedview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createview.html)（原文版本：18.6；核對日期：2026-10-03）
