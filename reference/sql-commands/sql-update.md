<a id="id-1.9.3.183.1"></a>

## UPDATE

UPDATE — 更新資料表的資料列

## 語法

```

[ WITH [ RECURSIVE ] with_query [, ...] ]
UPDATE [ ONLY ] table_name [ * ] [ [ AS ] alias ]
    SET { column_name = { expression | DEFAULT } |
          ( column_name [, ...] ) = [ ROW ] ( { expression | DEFAULT } [, ...] ) |
          ( column_name [, ...] ) = ( sub-SELECT )
        } [, ...]
    [ FROM from_item [, ...] ]
    [ WHERE condition | WHERE CURRENT OF cursor_name ]
    [ RETURNING [ WITH ( { OLD | NEW } AS output_alias [, ...] ) ]
                { * | output_expression [ [ AS ] output_name ] } [, ...] ]
```

<a id="id-1.9.3.183.5"></a>

## 說明

`UPDATE` 會變更所有滿足條件的資料列中，指定欄位的值。
只有要修改的欄位需要列在 `SET` 子句中；
未明確修改的欄位會保留其先前的值。

要使用資料庫中其他資料表所包含的資訊來修改一個資料表，
有兩種方式：使用子查詢，或在 `FROM` 子句中指定
額外的資料表。哪一種技巧較為合適，取決於具體情況。

選擇性的 `RETURNING` 子句會讓 `UPDATE`
根據每一筆實際被更新的資料列，計算並傳回值。
可以計算任何使用該資料表欄位，及／或 `FROM`
中提及的其他資料表欄位的運算式。預設情況下，
使用的是資料表欄位更新後的新值，但也可以要求取得
更新前的舊值。`RETURNING` 清單的語法與
`SELECT` 的輸出清單相同。

你必須擁有該資料表的 `UPDATE` 權限，或至少對
列於更新清單中的欄位擁有該權限。對於任何在
*`expressions`* 或 *`condition`*
中被讀取其值的欄位，你也必須擁有 `SELECT` 權限。

<a id="id-1.9.3.183.6"></a>

## 參數

*`with_query`*
:   `WITH` 子句讓你可以指定一個或多個子查詢，
    並在 `UPDATE` 查詢中以名稱參照它們。詳情請參閱
    [Section 7.8](../../the-sql-language/queries/queries-with.md) 與
    [SELECT](sql-select.md)。

*`table_name`*
:   要更新的資料表名稱（可加上結構描述限定）。
    若在資料表名稱前指定了 `ONLY`，則只會更新指定資料表中
    符合條件的資料列。若未指定 `ONLY`，則繼承自該資料表的
    任何資料表中符合條件的資料列也會被更新。也可以選擇在
    資料表名稱後指定 `*`，以明確表示包含子系資料表。

*`alias`*
:   目標資料表的替代名稱。當提供別名時，它會完全隱藏該資料表
    的實際名稱。舉例來說，給定 `UPDATE foo AS f`，
    這個 `UPDATE` 陳述式的其餘部分都必須以
    `f` 而非 `foo` 來參照這個資料表。

*`column_name`*
:   *`table_name`* 所指定資料表中某個欄位的名稱。
    若有需要，欄位名稱可以搭配子欄位名稱或陣列註標來限定。
    請勿在目標欄位的指定中包含資料表名稱——舉例來說，
    `UPDATE table_name SET table_name.col = 1` 是無效的。

*`expression`*
:   要指派給該欄位的運算式。此運算式可以使用該資料表中
    這個欄位及其他欄位的舊值。

`DEFAULT`
:   將欄位設為其預設值（若未替該欄位指定特定的預設運算式，
    則為 NULL）。身分識別欄位會被設為由相關聯序列所產生的新值。
    對於產生欄位而言，指定此項是允許的，但這只是單純指定了
    依其產生運算式計算該欄位的一般行為。

*`sub-SELECT`*
:   一個 `SELECT` 子查詢，其產生的輸出欄位數量，
    須與它前面括號括住的欄位清單中列出的數量相同。
    此子查詢執行時傳回的資料列不得超過一列。若傳回一列，
    其欄位值會被指派給目標欄位；若不傳回任何資料列，
    則會將 NULL 值指派給目標欄位。這個子查詢可以參照
    正在更新之資料表目前資料列的舊值。

*`from_item`*
:   一個資料表運算式，讓其他資料表的欄位得以出現在
    `WHERE` 條件及更新運算式中。這使用的語法
    與 `SELECT` 陳述式的
    [`FROM`](sql-select.md#SQL-FROM) 子句相同；
    舉例來說，可以為資料表名稱指定別名。除非你想進行自我聯結
    （在這種情況下，該表必須以別名出現在
    *`from_item`* 中），否則不要在
    *`from_item`* 中重複列出目標資料表。

*`condition`*
:   傳回 `boolean` 型別值的運算式。只有這個運算式傳回
    `true` 的資料列才會被更新。

*`cursor_name`*
:   在 `WHERE CURRENT OF` 條件中使用的游標名稱。
    要更新的資料列是最近一次從這個游標擷取出的那一列。
    這個游標必須是針對 `UPDATE` 目標資料表的
    非群組查詢。請注意，`WHERE CURRENT OF`
    不能與布林條件一起指定。關於在
    `WHERE CURRENT OF` 中使用游標的更多資訊，
    請參閱 [DECLARE](sql-declare.md)。

*`output_alias`*
:   在 `RETURNING` 清單中，`OLD` 或
    `NEW` 資料列的選擇性替代名稱。

    預設情況下，目標資料表的舊值可以透過寫
    `OLD.column_name` 或 `OLD.*`
    來傳回，新值則可以透過寫
    `NEW.column_name` 或 `NEW.*`
    來傳回。當提供別名時，這些名稱會被隱藏，舊資料列或新資料列
    必須改用該別名來參照。舉例來說：
    `RETURNING WITH (OLD AS o, NEW AS n) o.*, n.*`。

*`output_expression`*
:   每筆資料列更新後，要由 `UPDATE` 指令計算並傳回的
    運算式。此運算式可以使用
    *`table_name`* 所指定資料表，
    或 `FROM` 中列出之資料表的任何欄位名稱。
    寫 `*` 可傳回所有欄位。

    欄位名稱或 `*` 可以用 `OLD` 或
    `NEW`，或是對應
    `OLD`／`NEW` 的
    *`output_alias`* 來限定，
    以傳回舊值或新值。未加限定的欄位名稱、或
    `*`、或以目標資料表名稱或別名限定的欄位名稱或
    `*`，都會傳回新值。

*`output_name`*
:   要用於某個傳回欄位的名稱。

<a id="id-1.9.3.183.7"></a>

## 輸出

成功完成後，`UPDATE` 指令會傳回下列形式的指令標籤

```

UPDATE count
```

*`count`* 是被更新的資料列數，
其中也包含值雖未改變、但確實符合條件的資料列。請注意，
當更新因 `BEFORE UPDATE` 觸發程序而被抑制時，
這個數字可能會少於實際符合
*`condition`* 的資料列數。
若 *`count`* 為 0，
表示查詢未更新任何資料列（這不會被視為錯誤）。

若 `UPDATE` 指令含有 `RETURNING` 子句，
其結果會類似於一個 `SELECT` 陳述式的結果，
包含 `RETURNING` 清單中定義的欄位與值，
並以指令所更新的資料列來計算。

<a id="id-1.9.3.183.8"></a>

## 注意事項

當有 `FROM` 子句時，實際發生的事情本質上是：
目標資料表會與 *`from_item`* 清單中提及的
資料表進行聯結，聯結後的每一列輸出資料列，
就代表對目標資料表的一次更新操作。使用
`FROM` 時，你應該確保聯結對每一筆要修改的資料列，
最多只產生一列輸出。換句話說，目標資料列不應該與
其他資料表中超過一列的資料相聯結。若真的發生這種情況，
就只會用其中一個聯結後的資料列來更新目標資料列，
但究竟會用哪一個是無法輕易預測的。

正因為存在這種不確定性，只在子查詢中參照其他資料表會比較安全，
雖然這麼做通常較難閱讀，速度也較慢，這是與使用聯結相比而言。

對於分割表而言，更新一筆資料列可能導致它不再滿足其所屬
分割區的分割限制條件。在這種情況下，若分割樹中存在其他
分割區、且該資料列滿足其分割限制條件，則該資料列會被移動
到那個分割區。若沒有這樣的分割區，就會發生錯誤。在幕後，
這個資料列搬移動作實際上是一次 `DELETE` 加
`INSERT` 操作。

被搬移的資料列上，若有並行的 `UPDATE` 或
`DELETE`，有可能會得到序列化失敗錯誤。假設工作階段 1
正在對某個分割鍵執行 `UPDATE`，而與此同時，
另一個並行的工作階段 2 對這筆（對它而言仍可見的）資料列
執行了 `UPDATE` 或 `DELETE` 操作。
在這種情況下，工作階段 2 的 `UPDATE` 或
`DELETE` 會偵測到資料列搬移，並引發序列化失敗錯誤
（一律會傳回 SQLSTATE 代碼 '40001'）。若發生此情況，
應用程式或許會想要重試該筆交易。在資料表未分割，
或不涉及資料列搬移的一般情況下，工作階段 2 原本
會找出剛剛更新後的新資料列，並對這個新版本執行
`UPDATE`／`DELETE`。

請注意，雖然資料列可以從本機分割區搬移到外部資料表分割區
（前提是外部資料包裝器支援資料列路由），但無法從
外部資料表分割區搬移到另一個分割區。

若發現有外鍵直接參照來源分割區的某個祖系，而該祖系
與 `UPDATE` 查詢中提及的祖系不同，
則嘗試將資料列從一個分割區搬移到另一個分割區的動作
會失敗。

<a id="id-1.9.3.183.9"></a>

## 範例

將資料表 `films` 的 `kind` 欄位中，
`Drama` 改為 `Dramatic`：

```

UPDATE films SET kind = 'Dramatic' WHERE kind = 'Drama';
```

在 `weather` 資料表的某一列中調整溫度資料，
並將降水量重設為其預設值：

```

UPDATE weather SET temp_lo = temp_lo+1, temp_hi = temp_lo+15, prcp = DEFAULT
  WHERE city = 'San Francisco' AND date = '2003-07-03';
```

執行相同的操作，並傳回更新後的項目，以及舊的降水量值：

```

UPDATE weather SET temp_lo = temp_lo+1, temp_hi = temp_lo+15, prcp = DEFAULT
  WHERE city = 'San Francisco' AND date = '2003-07-03'
  RETURNING temp_lo, temp_hi, prcp, old.prcp AS old_prcp;
```

使用替代的欄位清單語法，執行相同的更新：

```

UPDATE weather SET (temp_lo, temp_hi, prcp) = (temp_lo+1, temp_lo+15, DEFAULT)
  WHERE city = 'San Francisco' AND date = '2003-07-03';
```

使用 `FROM` 子句語法，增加負責 Acme Corporation
帳戶之業務人員的銷售件數：

```

UPDATE employees SET sales_count = sales_count + 1 FROM accounts
  WHERE accounts.name = 'Acme Corporation'
  AND employees.id = accounts.sales_person;
```

執行相同的操作，但改在 `WHERE` 子句中使用子查詢：

```

UPDATE employees SET sales_count = sales_count + 1 WHERE id =
  (SELECT sales_person FROM accounts WHERE name = 'Acme Corporation');
```

更新帳戶資料表中的聯絡人姓名，使其與目前指派的業務人員相符：

```

UPDATE accounts SET (contact_first_name, contact_last_name) =
    (SELECT first_name, last_name FROM employees
     WHERE employees.id = accounts.sales_person);
```

使用聯結也可以達成類似的結果：

```

UPDATE accounts SET contact_first_name = first_name,
                    contact_last_name = last_name
  FROM employees WHERE employees.id = accounts.sales_person;
```

然而，若 `employees`.`id` 不是唯一鍵，
第二個查詢可能會產生非預期的結果，而第一個查詢則保證
在有多個 `id` 相符時引發錯誤。此外，若某筆特定的
`accounts`.`sales_person` 項目找不到相符的資料，
第一個查詢會將對應的姓名欄位設為 NULL，
而第二個查詢則完全不會更新該筆資料列。

更新摘要資料表中的統計資訊，使其與目前的資料相符：

```

UPDATE summary s SET (sum_x, sum_y, avg_x, avg_y) =
    (SELECT sum(x), sum(y), avg(x), avg(y) FROM data d
     WHERE d.group_id = s.group_id);
```

嘗試插入一項新的庫存品項及其庫存數量。若該品項已存在，
則改為更新既有品項的庫存數量。為了不讓整筆交易失敗，
可使用儲存點來完成這件事：

```

BEGIN;
-- other operations
SAVEPOINT sp1;
INSERT INTO wines VALUES('Chateau Lafite 2003', '24');
-- Assume the above fails because of a unique key violation,
-- so now we issue these commands:
ROLLBACK TO sp1;
UPDATE wines SET stock = stock + 24 WHERE winename = 'Chateau Lafite 2003';
-- continue with other operations, and eventually
COMMIT;
```

變更資料表 `films` 中，游標 `c_films`
目前所指向那一列的 `kind` 欄位：

```

UPDATE films SET kind = 'Dramatic' WHERE CURRENT OF c_films;
```

<a id="UPDATE-LIMIT"></a>

影響大量資料列的更新，可能會對系統效能產生負面影響，
例如資料表膨脹、複本延遲增加，以及鎖爭用增加。在這類情況下，
將操作拆成較小的批次執行會是合理的做法，並可視需要在批次之間
對資料表執行一次 `VACUUM` 操作。雖然 `UPDATE`
沒有 `LIMIT` 子句，但仍可透過搭配使用
[共同資料表運算式](../../the-sql-language/queries/queries-with.md)
與自我聯結，達到類似的效果。搭配標準 PostgreSQL
資料表存取方法時，對系統欄位
[ctid](../../the-sql-language/ddl/ddl-system-columns.md#DDL-SYSTEM-COLUMNS-CTID)
進行自我聯結是非常有效率的做法：

```

WITH exceeded_max_retries AS (
  SELECT w.ctid FROM work_item AS w
    WHERE w.status = 'active' AND w.num_retries > 10
    ORDER BY w.retry_timestamp
    FOR UPDATE
    LIMIT 5000
)
UPDATE work_item SET status = 'failed'
  FROM exceeded_max_retries AS emr
  WHERE work_item.ctid = emr.ctid;
```

這個指令需要不斷重複執行，直到沒有剩餘的資料列需要更新為止。
（這裡使用 `ctid` 之所以安全，僅僅是因為這個查詢
會被重複執行，避免了 `ctid` 改變所造成的問題。）
使用 `ORDER BY` 子句可以讓這個指令優先處理
哪些資料列要被更新；它也能在其他更新操作使用相同排序方式時，
協助避免死結。若鎖爭用是個問題，可以在 CTE 中加入
`SKIP LOCKED`，以避免多個指令更新同一筆資料列。
然而，接下來就需要一個不含 `SKIP LOCKED` 或
`LIMIT` 的最終 `UPDATE`，以確保沒有任何
符合條件的資料列被遺漏。

<a id="id-1.9.3.183.10"></a>

## 相容性

本指令符合 SQL 標準，但 `FROM` 與
`RETURNING` 子句是 PostgreSQL 的擴充功能，
與 `UPDATE` 搭配使用 `WITH` 的能力也是。

某些其他資料庫系統提供的 `FROM` 選項，是要求在
`FROM` 中再次列出目標資料表。PostgreSQL
對 `FROM` 的解讀並非如此。在移植使用這項擴充功能的
應用程式時請務必小心。

依照標準的規定，括號括住之目標欄位名稱清單所對應的來源值，
可以是任何能產生正確欄位數量的資料列值運算式。
PostgreSQL 只允許來源值為
[資料列建構子](../../the-sql-language/sql-syntax/sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)
或子 `SELECT`。在資料列建構子的情況下，
可以將個別欄位更新後的值指定為 `DEFAULT`，
但在子 `SELECT` 中則不行。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-update.html)（原文版本：18.6；核對日期：2026-09-28）
