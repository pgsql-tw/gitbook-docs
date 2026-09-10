<a id="id-1.11.7.21.24.1"></a>

## dblink_build_sql_delete

dblink_build_sql_delete — 使用提供的主鍵欄位值建立 DELETE 陳述式

## 語法

```

dblink_build_sql_delete(text relname,
                        int2vector primary_key_attnums,
                        integer num_primary_key_atts,
                        text[] tgt_pk_att_vals_array) returns text
```

<a id="id-1.11.7.21.24.5"></a>

## 說明

`dblink_build_sql_delete` 可用於將本機資料表選擇性複寫至遠端資料庫。它會建立 SQL `DELETE` 指令，刪除具有指定主鍵值的資料列。

<a id="id-1.11.7.21.24.6"></a>

## 引數

*`relname`*
:   本機關聯名稱，例如 `foo` 或 `myschema.mytab`。若名稱混用大小寫或包含特殊字元，請加上雙引號，例如 `"FooBar"`；若未加引號，字串會摺疊為小寫。

*`primary_key_attnums`*
:   主鍵欄位的屬性編號（從 1 開始），例如 `1 2`。

*`num_primary_key_atts`*
:   主鍵欄位數量。

*`tgt_pk_att_vals_array`*
:   產生的 `DELETE` 指令中要使用的主鍵欄位值。每個欄位都以文字形式表示。

<a id="id-1.11.7.21.24.7"></a>

## 傳回值

以文字形式傳回所要求的 SQL 陳述式。

<a id="id-1.11.7.21.24.8"></a>

## 注意事項

自 PostgreSQL 9.0 起，*`primary_key_attnums`* 中的屬性編號會解讀為邏輯欄位編號，對應至欄位在 `SELECT * FROM relname` 中的位置。先前版本將此編號解讀為實體欄位位置。若資料表生命週期中已刪除所指欄位左側的任何欄位，兩者會有所不同。

<a id="id-1.11.7.21.24.9"></a>

## 範例

```

SELECT dblink_build_sql_delete('"MyFoo"', '1 2', 2, '{"1", "b"}');
           dblink_build_sql_delete
---------------------------------------------
 DELETE FROM "MyFoo" WHERE f1='1' AND f2='b'
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-build-sql-delete.html)
