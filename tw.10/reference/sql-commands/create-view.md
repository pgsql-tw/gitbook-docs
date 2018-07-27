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

### 注意

使用 [DROP VIEW](drop-view.md) 語句移除檢視表。

請注意，檢視表欄位的名稱和型別會按您希望的方式分配。例如：

```text
CREATE VIEW vista AS SELECT 'Hello World';
```

是不好的形式，因為欄位名稱預設為 ?column?；此外，欄位資料型別預設為 text，可能不是您想要的。在檢視表的結果中，字串的更好形式是這樣的：

```text
CREATE VIEW vista AS SELECT text 'Hello World' AS hello;
```

對檢視表中引用的資料表存取權限由檢視表擁有者的權限決定。在某些情況下，這可用於提供對基礎資料表安全但受限制的存取。但是，並非所有檢視表都可以防範篡改；有關詳細訊息，請參閱[第 40.5 節](../../server-programming/the-rule-system/rules-and-privileges.md)。在檢視表中呼叫的函數處理方式與使用檢視表直接從查詢中呼叫的函數相同。因此，檢視表的使用者必須具有呼叫檢視表使用的所有函數權限。

在現有檢視表上使用 CREATE OR REPLACE VIEW 時，僅更改檢視表定義的 SELECT 規則。其他檢視表屬性（包括所有權，權限和非 SELECT 規則）保持不變。您必須擁有檢視表才能替換它（這包括成為擁有角色的成員）。

#### 可更新的檢視表（Updatable Views）

簡單檢視表可自動更新：系統將允許 INSERT，UPDATE 和 DELETE 語句以與一般資料表相同的方式在檢視表上使用。如果檢視表滿足以下所有條件，則檢視表可自動更新：

* 檢視表必須在其 FROM 列表中只有一個項目，該列表必須是資料表或另一個可更新檢視表。
* 檢視表定義不得在最上層有 WITH，DISTINCT，GROUP BY，HAVING，LIMIT 或 OFFSET 子句。
* 檢視表定義不得在最上層有集合的操作（UNION，INTERSECT 或 EXCEPT）。
* 檢視表的選擇列表不得包含任何彙總、窗函數或設定回傳函數。

可自動更新的檢視表可以包含可更新欄位和不可更新欄位的混合。如果欄位是對底層基本關連的可更新欄位簡單引用，則欄位是可更新的；否則該欄位是唯讀的，如果 INSERT 或 UPDATE 語句嘗試為其賦值，則會引發錯誤。

如果檢視表可自動更新，則系統會將檢視表上的任何 INSERT，UPDATE 或 DELETE 語句轉換為基本關連上的相應語句。完全支援具有 ON CONFLICT UPDATE 子句的 INSERT 語句。

如果可自動更新的檢視表包含 WHERE 條件，則條件限制檢視表上的 UPDATE 和 DELETE 語句可以修改基本關連的哪些資料列。但是，允許 UPDATE 更改資料列以使其不再滿足 WHERE 條件，因此不再透過檢視表看見。類似地，INSERT 指令可能會插入不滿足 WHERE 條件的基本關連資料列，因此透過檢視圖就不可見（ON CONFLICT UPDATE 可能類似地影響透過檢視圖不可見的現有資料列）。 CHECK OPTION 可用於防止 INSERT 和 UPDATE 指令建立檢視表不可見的資料列。

如果使用 security\_barrier 屬性標記了可自動更新的檢視表，那麼將始終在檢視表使用者增加的任何條件之前評估所有檢視表的 WHERE 條件（以及使用標記為 LEAKPROOF 的運算子的任何條件）。有關詳細訊息，請參閱[第 40.5 節](../../server-programming/the-rule-system/rules-and-privileges.md)。請注意，由於這個原因，最終未回傳的資料列（因為它們沒有通過使用者的 WHERE 條件）可能仍然會被鎖定。EXPLAIN 可用於查看在關連等級套用哪些條件（因此不鎖定資料列），哪些不是。

預設情況下，不滿足所有這些條件的更複雜檢視表是唯讀的：系統不允許在檢視表上插入，更新或刪除。您可以透過在檢視表上建立 INSTEAD OF 觸發器來獲取可更新檢視表的效果，該觸發器必須將檢視表上的嘗試插入等轉換為對其他資料表的適當操作。有關更多訊息，請參閱 [CREATE TRIGGER](create-trigger.md)。另一種可能性是建立規則（參閱 [CREATE RULE](create-rule.md)），但實際上觸發器更容易理解和正確使用。

請注意，在檢視表上執行插入，更新或刪除的使用者必須在檢視表上具有相對應的插入，更新或刪除權限。此外，檢視表的擁有者必須具有底層基本關連的相關權限，但執行更新的使用者不需要對底層基本關連的任何權限（請參閱[第 40.5 節](../../server-programming/the-rule-system/rules-and-privileges.md)）。

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

