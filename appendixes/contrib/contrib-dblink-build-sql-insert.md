<a id="id-1.11.7.21.23.1"></a>

## dblink_build_sql_insert

dblink_build_sql_insert — 使用本機 tuple 建立 INSERT 陳述式，並以提供的替代值取代主鍵欄位值

## 語法

```

dblink_build_sql_insert(text relname,
                        int2vector primary_key_attnums,
                        integer num_primary_key_atts,
                        text[] src_pk_att_vals_array,
                        text[] tgt_pk_att_vals_array) returns text
```

<a id="id-1.11.7.21.23.5"></a>

## 說明

`dblink_build_sql_insert` 可用於將本機資料表選擇性複寫至遠端資料庫。它會依主鍵從本機資料表選取一列，接著建立複製該資料列的 SQL `INSERT` 指令，但以最後一個引數中的值取代主鍵值。（若要精確複製資料列，只要為最後兩個引數指定相同值。）

<a id="id-1.11.7.21.23.6"></a>

## 引數

*`relname`*
:   本機關聯名稱，例如 `foo` 或 `myschema.mytab`。若名稱混用大小寫或包含特殊字元，請加上雙引號，例如 `"FooBar"`；若未加引號，字串會摺疊為小寫。

*`primary_key_attnums`*
:   主鍵欄位的屬性編號（從 1 開始），例如 `1 2`。

*`num_primary_key_atts`*
:   主鍵欄位數量。

*`src_pk_att_vals_array`*
:   用來查詢本機 tuple 的主鍵欄位值。每個欄位都以文字形式表示。若沒有具有這些主鍵值的本機資料列，會引發錯誤。

*`tgt_pk_att_vals_array`*
:   置入產生之 `INSERT` 指令的主鍵欄位值。每個欄位都以文字形式表示。

<a id="id-1.11.7.21.23.7"></a>

## 傳回值

以文字形式傳回所要求的 SQL 陳述式。

<a id="id-1.11.7.21.23.8"></a>

## 注意事項

自 PostgreSQL 9.0 起，*`primary_key_attnums`* 中的屬性編號會解讀為邏輯欄位編號，對應至欄位在 `SELECT * FROM relname` 中的位置。先前版本將此編號解讀為實體欄位位置。若資料表生命週期中已刪除所指欄位左側的任何欄位，兩者會有所不同。

<a id="id-1.11.7.21.23.9"></a>

## 範例

```

SELECT dblink_build_sql_insert('foo', '1 2', 2, '{"1", "a"}', '{"1", "b''a"}');
             dblink_build_sql_insert
--------------------------------------------------
 INSERT INTO foo(f1,f2,f3) VALUES('1','b''a','1')
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-build-sql-insert.html)
