<a id="PLTCL-TRIGGER"></a>

## 42.6. PL/Tcl 中的觸發程序函式 [#](#PLTCL-TRIGGER)

<a id="id-1.8.9.10.2"></a>

觸發程序函式可以用 PL/Tcl 撰寫。PostgreSQL 要求，要作為觸發程序被呼叫的函式，必須宣告為不帶引數且回傳型別為 `trigger` 的函式。

來自觸發程序管理器的資訊會透過下列變數傳入函式主體：

`$TG_name`
:   來自 `CREATE TRIGGER` 陳述式的觸發程序名稱。

`$TG_relid`
:   造成該觸發程序函式被呼叫的資料表之物件 ID。

`$TG_table_name`
:   造成該觸發程序函式被呼叫的資料表名稱。

`$TG_table_schema`
:   造成該觸發程序函式被呼叫的資料表所屬的綱要。

`$TG_relatts`
:   一個包含資料表欄位名稱的 Tcl list（串列），開頭多了一個空的 list 元素。因此用 Tcl 的 `lsearch` 指令在這個 list 中查找欄位名稱時，回傳的元素編號會從第一個欄位的 1 開始，與 PostgreSQL 中習慣的欄位編號方式相同。（已被刪除的欄位位置上也會出現空的 list 元素，以便其右側欄位的屬性編號仍然正確。）

`$TG_when`
:   字串 `BEFORE`、`AFTER` 或 `INSTEAD OF`，取決於觸發程序事件的型態。

`$TG_level`
:   字串 `ROW` 或 `STATEMENT`，取決於觸發程序事件的型態。

`$TG_op`
:   字串 `INSERT`、`UPDATE`、`DELETE` 或 `TRUNCATE`，取決於觸發程序事件的型態。

`$NEW`
:   一個關聯陣列，對 `INSERT` 或 `UPDATE` 動作而言含有新資料列的值，對 `DELETE` 而言則為空。這個陣列以欄位名稱作為索引。值為 NULL 的欄位不會出現在陣列中。在陳述式層級的觸發程序中不會設定這個變數。

`$OLD`
:   一個關聯陣列，對 `UPDATE` 或 `DELETE` 動作而言含有舊資料列的值，對 `INSERT` 而言則為空。這個陣列以欄位名稱作為索引。值為 NULL 的欄位不會出現在陣列中。在陳述式層級的觸發程序中不會設定這個變數。

`$args`
:   一個 Tcl list，內容是 `CREATE TRIGGER` 陳述式中給定的函式引數。這些引數在函式主體中也可以透過 `$1` ... `$n` 存取。

觸發程序函式的回傳值可以是字串 `OK` 或 `SKIP` 之一，或是一個欄位名稱／值配對的 list。如果回傳值是 `OK`，觸發該觸發程序的操作（`INSERT`／`UPDATE`／`DELETE`）會正常進行。`SKIP` 則告訴觸發程序管理器要靜默地略過此資料列的操作。如果回傳的是一個 list，它會告訴 PL/Tcl 要回傳一個修改過的資料列給觸發程序管理器；修改後資料列的內容由該 list 中的欄位名稱與值所指定。list 中未提及的欄位都會被設為 NULL。回傳修改過的資料列只對資料列層級的 `BEFORE` `INSERT` 或 `UPDATE` 觸發程序有意義，此時會插入修改後的資料列，而不是 `$NEW` 中所給定的那一筆；或者對資料列層級的 `INSTEAD OF` `INSERT` 或 `UPDATE` 觸發程序有意義，此時回傳的資料列會被用作 `INSERT RETURNING` 或 `UPDATE RETURNING` 子句的來源資料。在資料列層級的 `BEFORE` `DELETE` 或 `INSTEAD OF` `DELETE` 觸發程序中，回傳修改過的資料列與回傳 `OK` 有相同的效果，也就是操作會繼續進行。對於所有其他型態的觸發程序，觸發程序的回傳值都會被忽略。

### 提示

結果 list 可以用 Tcl 的 `array get` 指令，從修改後 tuple（值組）的陣列表示法產生出來。

以下是一個小小的範例觸發程序函式，它強制讓資料表中的某個整數值持續記錄該資料列被更新過的次數。對於新插入的資料列，該值會初始化為 0，然後在每次更新操作時遞增。

```

CREATE FUNCTION trigfunc_modcount() RETURNS trigger AS $$
    switch $TG_op {
        INSERT {
            set NEW($1) 0
        }
        UPDATE {
            set NEW($1) $OLD($1)
            incr NEW($1)
        }
        default {
            return OK
        }
    }
    return [array get NEW]
$$ LANGUAGE pltcl;

CREATE TABLE mytab (num integer, description text, modcnt integer);

CREATE TRIGGER trig_mytab_modcount BEFORE INSERT OR UPDATE ON mytab
    FOR EACH ROW EXECUTE FUNCTION trigfunc_modcount('modcnt');
```

請注意，觸發程序函式本身並不知道欄位名稱；那是由觸發程序的引數所提供的。這讓該觸發程序函式可以被不同的資料表重複使用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-trigger.html)（原文版本：18.6；核對日期：2026-09-12）
