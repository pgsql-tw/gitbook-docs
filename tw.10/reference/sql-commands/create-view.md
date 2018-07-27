---
description: 版本：10
---

# CREATE VIEW

CREATE VIEW — 定義一個新的檢視表

### 語法

```text
CREATE [ OR REPLACE ] [ TEMP | TEMPORARY ] [ RECURSIVE ] VIEW name [ ( column_name [, ...] ) ]
    [ WITH ( view_option_name [= view_option_value] [, ... ] ) ]
    AS query
    [ WITH [ CASCADED | LOCAL ] CHECK OPTION ]
```

### 說明

CREATE VIEW 定義某個查詢的檢視表。此檢視表並不會實體上存在。相反地，每次在查詢中引用檢視表時才進行查詢。

CREATE OR REPLACE VIEW 類似，只是如果已經存在同名的檢視表，則替換它。新的查詢必須産生與現有檢視表查詢所産生相同的欄位（即，相同順序且具有相同資料型別的相同欄位名稱），但它可以會在列表末尾增加其他欄位。產生輸出欄位的計算可能完全不同。

如果加上了綱要名稱（例如，CREATE VIEW myschema.myview ...），則會在指定的綱要中建立檢視表。否則，它將在目前綱要中建立。臨時檢視表存在於特殊綱要中，因此在建立臨時檢視圖時不能加上綱要名稱。檢視表的名稱必須與同一綱要中的任何其他檢視表、資料表、序列、索引或外部資料表的名稱不同。

### 參數

`TEMPORARY` or `TEMP`

如果指定此選項，則檢視表將建立為臨時檢視表。臨時檢視表會在目前連線結束時自動刪除。當臨時檢視表存在時，目前連線不會顯示具有相同名稱的現有永久關連，除非它們以綱要名稱引用。

如果檢視表引用的任何資料表是臨時的，則檢視表將建立為臨時檢視表（無論是否指定了 TEMPORARY）。

`RECURSIVE`

建立遞迴檢視表。語法：

```text
CREATE RECURSIVE VIEW [ schema . ] view_name (column_names) AS SELECT ...;
```

同等於

```text
CREATE VIEW [ schema . ] view_name AS WITH RECURSIVE view_name (column_names) AS (SELECT ...) SELECT column_names FROM view_name;
```

必須為遞迴檢視表指定檢視表欄位名稱列表。

_`name`_

要建立的檢視表名稱（選擇性加入綱要名稱）。

_`column_name`_

用於檢視表欄位的選擇性名稱列表。如果沒有，則從查詢中推導出欄位名稱。

`WITH (` _`view_option_name`_ \[= _`view_option_value`_\] \[, ... \] \)

此子句指定檢視表的選擇性參數；支援以下參數：

`check_option` \(`string`\)

此參數可能是 local 或 cascaded，等同於指定 WITH \[CASCADED \| LOCAL\] CHECK OPTION（見下文）。可以使用 ALTER VIEW 在現有檢視表上變更此選項。

`security_barrier` \(`boolean`\)

如果檢視表旨在提供資料列級安全性，則應使用此方法。有關詳細訊息，請參閱[第 40.5 節](../../server-programming/the-rule-system/rules-and-privileges.md)。

_`query`_

[SELECT](select.md) 或 [VALUES](values.md) 指令，它將提供檢視表的欄位和資料列。

`WITH [ CASCADED | LOCAL ] CHECK OPTION`

此選項控制自動可更新檢視表的行為。指定此選項時，將檢查檢視表上的 INSERT 和 UPDATE 指令，以確保新資料列滿足檢視表定義條件（即，檢查新資料列以確保它們在檢視表中可見）。如果不是，則將拒絕更新。如果未指定 CHECK OPTION，則允許檢視表上的 INSERT 和 UPDATE 指令建立檢視表不可見的資料列。支援以下檢查選項：

`LOCAL`

僅根據檢視表本身中直接定義的條件檢查新資料列。不檢查在其基礎的檢視表上定義的任何條件（除非它們也指定了 CHECK OPTION）。

`CASCADED`

根據檢視圖條件和所有其基礎的檢視表檢查新資料列。如果指定了 CHECK OPTION，而既未指定 LOCAL 也未指定 CASCADED，則假定為 CASCADED。

CHECK OPTION 可能不適用於 RECURSIVE 檢視表。

請注意，CHECK OPTION 僅在可自動更新的檢視表上受到支援，並且沒有 INSTEAD OF 觸發器或 INSTEAD 規則。如果在具有 INSTEAD OF 觸發器的基本檢視表之上定義了可自動更新的檢視表，則 LOCAL CHECK OPTION 可用於檢查自動更新檢視表上的條件。但是具有 INSTEAD OF 觸發器的基本檢視表上的條件將不會檢查（CASCADED 選項不會延伸影響到觸發器可更新檢視表，並且將忽略直接在觸發器可更新檢視表上定義的任何檢查選項）。如果檢視表或其任何基本關連具有導致 INSERT 或 UPDATE 指令被重寫的 INSTEAD 規則，則在重寫的查詢中將忽略所有檢查選項，包括在與關連之上定義的自動可更新檢視表的任何檢查與 INSTEAD 規則。

### Notes

Use the [DROP VIEW](https://www.postgresql.org/docs/10/static/sql-dropview.html) statement to drop views.

Be careful that the names and types of the view's columns will be assigned the way you want. For example:

```text
CREATE VIEW vista AS SELECT 'Hello World';
```

is bad form because the column name defaults to `?column?`; also, the column data type defaults to `text`, which might not be what you wanted. Better style for a string literal in a view's result is something like:

```text
CREATE VIEW vista AS SELECT text 'Hello World' AS hello;
```

Access to tables referenced in the view is determined by permissions of the view owner. In some cases, this can be used to provide secure but restricted access to the underlying tables. However, not all views are secure against tampering; see [Section 40.5](https://www.postgresql.org/docs/10/static/rules-privileges.html) for details. Functions called in the view are treated the same as if they had been called directly from the query using the view. Therefore the user of a view must have permissions to call all functions used by the view.

When `CREATE OR REPLACE VIEW` is used on an existing view, only the view's defining SELECT rule is changed. Other view properties, including ownership, permissions, and non-SELECT rules, remain unchanged. You must own the view to replace it \(this includes being a member of the owning role\).

#### Updatable Views

Simple views are automatically updatable: the system will allow `INSERT`, `UPDATE` and `DELETE` statements to be used on the view in the same way as on a regular table. A view is automatically updatable if it satisfies all of the following conditions:

* The view must have exactly one entry in its `FROM` list, which must be a table or another updatable view.
* The view definition must not contain `WITH`, `DISTINCT`, `GROUP BY`, `HAVING`, `LIMIT`, or `OFFSET` clauses at the top level.
* The view definition must not contain set operations \(`UNION`, `INTERSECT` or `EXCEPT`\) at the top level.
* The view's select list must not contain any aggregates, window functions or set-returning functions.

An automatically updatable view may contain a mix of updatable and non-updatable columns. A column is updatable if it is a simple reference to an updatable column of the underlying base relation; otherwise the column is read-only, and an error will be raised if an `INSERT` or `UPDATE` statement attempts to assign a value to it.

If the view is automatically updatable the system will convert any `INSERT`, `UPDATE` or `DELETE` statement on the view into the corresponding statement on the underlying base relation. `INSERT` statements that have an `ON CONFLICT UPDATE` clause are fully supported.

If an automatically updatable view contains a `WHERE` condition, the condition restricts which rows of the base relation are available to be modified by `UPDATE` and `DELETE` statements on the view. However, an `UPDATE` is allowed to change a row so that it no longer satisfies the `WHERE` condition, and thus is no longer visible through the view. Similarly, an `INSERT` command can potentially insert base-relation rows that do not satisfy the `WHERE` condition and thus are not visible through the view \(`ON CONFLICT UPDATE` may similarly affect an existing row not visible through the view\). The `CHECK OPTION` may be used to prevent `INSERT` and `UPDATE` commands from creating such rows that are not visible through the view.

If an automatically updatable view is marked with the `security_barrier` property then all the view's `WHERE` conditions \(and any conditions using operators which are marked as `LEAKPROOF`\) will always be evaluated before any conditions that a user of the view has added. See [Section 40.5](https://www.postgresql.org/docs/10/static/rules-privileges.html) for full details. Note that, due to this, rows which are not ultimately returned \(because they do not pass the user's `WHERE` conditions\) may still end up being locked. `EXPLAIN` can be used to see which conditions are applied at the relation level \(and therefore do not lock rows\) and which are not.

A more complex view that does not satisfy all these conditions is read-only by default: the system will not allow an insert, update, or delete on the view. You can get the effect of an updatable view by creating `INSTEAD OF` triggers on the view, which must convert attempted inserts, etc. on the view into appropriate actions on other tables. For more information see [CREATE TRIGGER](https://www.postgresql.org/docs/10/static/sql-createtrigger.html). Another possibility is to create rules \(see [CREATE RULE](https://www.postgresql.org/docs/10/static/sql-createrule.html)\), but in practice triggers are easier to understand and use correctly.

Note that the user performing the insert, update or delete on the view must have the corresponding insert, update or delete privilege on the view. In addition the view's owner must have the relevant privileges on the underlying base relations, but the user performing the update does not need any permissions on the underlying base relations \(see [Section 40.5](https://www.postgresql.org/docs/10/static/rules-privileges.html)\).

### 範例

建立一個包含所有喜劇電影的檢視表：

```text
CREATE VIEW comedies AS
    SELECT *
    FROM films
    WHERE kind = 'Comedy';
```

這將建立一個檢視表，包含資料表 film 中當下所有欄位。雖然 \* 用於建立檢視表，但稍後附加到資料表中的欄位，將不會成為檢視表的一部分。

使用 LOCAL CHECK OPTION 建立檢視表：

```text
CREATE VIEW universal_comedies AS
    SELECT *
    FROM comedies
    WHERE classification = 'U'
    WITH LOCAL CHECK OPTION;
```

這將建立一個基於喜劇檢視表的檢視表，僅顯示具有 kind = 'Comedy' 和 classification='U' 的電影。如果新的資料列沒有 classification = 'U'，則將拒絕任何在檢視表中插入或更新資料列的嘗試，但不會檢查 film 中的 kind 欄位。

使用 CASCADED CHECK OPTION 建立檢視表：

```text
CREATE VIEW pg_comedies AS
    SELECT *
    FROM comedies
    WHERE classification = 'PG'
    WITH CASCADED CHECK OPTION;
```

這將建立一個檢視表，檢查新資料列的 classification 和 kind。

混合可更新和不可更新欄位建立檢視表：

```text
CREATE VIEW comedies AS
    SELECT f.*,
           country_code_to_name(f.country_code) AS country,
           (SELECT avg(r.rating)
            FROM user_ratings r
            WHERE r.film_id = f.id) AS avg_rating
    FROM films f
    WHERE f.kind = 'Comedy';
```

此檢視表將支援 INSERT，UPDATE 和 DELETE。film 資料表中的所有欄位都是可更新的，而計算欄位 country 和 avg\_rating 將只是唯讀的。

建立一個包含 1 到 100 之間數字的遞迴檢視表：

```text
CREATE RECURSIVE VIEW public.nums_1_100 (n) AS
    VALUES (1)
UNION ALL
    SELECT n+1 FROM nums_1_100 WHERE n < 100;
```

請注意，雖然遞迴檢視表的名稱在此 CREATE 中加上綱要的，但其內部自我引用不能加上綱要。這是因為 CTE 名稱不能包含綱要名稱。

### 相容性

CREATE OR REPLACE VIEW 是 PostgreSQL 語言的延伸功能。臨時檢視表的概念也是如此。WITH（...）子句也是一個延伸功能。

### 參閱

[ALTER VIEW](alter-view.md), [DROP VIEW](drop-view.md), [CREATE MATERIALIZED VIEW](create-materialized-view.md)

