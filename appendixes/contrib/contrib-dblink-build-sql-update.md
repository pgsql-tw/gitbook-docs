<a id="id-1.11.7.21.25.1"></a>

## dblink_build_sql_update

dblink_build_sql_update — 使用本機 tuple 建立 `UPDATE` 陳述式，並以提供的替代值取代主鍵欄位值

## 語法

```

dblink_build_sql_update(text relname,
                        int2vector primary_key_attnums,
                        integer num_primary_key_atts,
                        text[] src_pk_att_vals_array,
                        text[] tgt_pk_att_vals_array) returns text
```

<a id="id-1.11.7.21.25.5"></a>

## 說明

`dblink_build_sql_update` 可用於將本機資料表選擇性複寫至遠端資料庫。它依據主鍵從本機資料表選取資料列，再建立一個複製該資料列的 SQL `UPDATE` 命令，但以最後一個引數的值取代主鍵值。（若要精確複製資料列，只需為最後兩個引數指定相同的值。）`UPDATE` 命令一律會指派資料列的所有欄位；它與 `dblink_build_sql_insert` 的主要差異在於，假設遠端資料表中已存在目標資料列。

<a id="id-1.11.7.21.25.6"></a>

## 引數

*`relname`*
:   本機關聯的名稱，例如 `foo` 或 `myschema.mytab`。若名稱混用大小寫或含有特殊字元，請加上雙引號，例如 `"FooBar"`；沒有引號時，字串會轉為小寫。

*`primary_key_attnums`*
:   主鍵欄位的屬性編號（從 1 開始），例如 `1 2`。

*`num_primary_key_atts`*
:   主鍵欄位的數量。

*`src_pk_att_vals_array`*
:   用於尋找本機 tuple 的主鍵欄位值。每個欄位均以文字形式表示。若沒有具備這些主鍵值的本機資料列，會發生錯誤。

*`tgt_pk_att_vals_array`*
:   要放入產生之 `UPDATE` 命令的主鍵欄位值。每個欄位均以文字形式表示。

<a id="id-1.11.7.21.25.7"></a>

## 回傳值

以文字形式回傳所要求的 SQL 陳述式。

<a id="id-1.11.7.21.25.8"></a>

## 注意事項

自 PostgreSQL 9.0 起，*`primary_key_attnums`* 中的屬性編號會解譯為邏輯欄位編號，亦即欄位在 `SELECT * FROM relname` 中的位置。較早版本則將這些編號解譯為實體欄位位置。若資料表存續期間曾刪除指定欄位左側的任何欄位，兩者會有所差異。

<a id="id-1.11.7.21.25.9"></a>

## 範例

```

SELECT dblink_build_sql_update('foo', '1 2', 2, '{"1", "a"}', '{"1", "b"}');
                   dblink_build_sql_update
-------------------------------------------------------------
 UPDATE foo SET f1='1',f2='b',f3='1' WHERE f1='1' AND f2='b'
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-build-sql-update.html)（原文版本：18.6；核對日期：2026-09-06）
