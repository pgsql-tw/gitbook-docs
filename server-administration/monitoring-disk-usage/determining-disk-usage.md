# 29.1. 瞭解磁碟使用情形

每個資料表都有一個主要的 heap 磁碟檔案，其中儲存了大多數的資料。如果資料表中的任何欄位可能會有大量內容，則可能還會有一個與該資料表相關聯的 TOAST 欄位，該欄位用於儲存太大量而無法適當地容納在主資料表中的內容（請參閱[第 73.3 節](../../internals/database-physical-storage/toast.md)）。如果存在的話，TOAST 資料表上將有一個有效的索引。也可能會有與基本資料表關聯的索引。每個資料表和索引都會儲存在一個單獨的磁碟檔案中-如果檔案超過 1 GB，則可能有多個文檔案。這些檔案的命名規則的請參閱[第 73.1 節](../../internals/database-physical-storage/database-file-layout.md)。

您可以透過三種方式監控磁碟空間：使用 [Table 9.94](../../the-sql-language/functions-and-operators/system-administration.md#table-9-89-database-object-size-functions) 中所列出的 SQL 函數，使用 [oid2name](../../reference/client-applications/oid2name.md) 模組或對系統目錄進行手動檢查。SQL 函數最易於使用，通常建議使用。本節的其餘部分顯示如何透過檢查系統目錄來執行此操作。

在最近清理或分析的資料庫上使用 psql，可以發出查詢以查看任何資料表的磁碟使用情況：

```
SELECT pg_relation_filepath(oid), relpages FROM pg_class WHERE relname = 'customer';

 pg_relation_filepath | relpages
----------------------+----------
 base/16384/16806     |       60
(1 row)
```

每個頁面通常為 8 KB。（請記住，只有 VACUUM，ANALYZE 和一些 DDL 命令（如 CREATE INDEX）才能更新 relpages。）如果要直接檢查資料表的磁碟檔案，則需要使用檔案路徑名稱。

要顯示 TOAST 資料表所使用的空間，請使用如下的查詢：

```
SELECT relname, relpages
FROM pg_class,
     (SELECT reltoastrelid
      FROM pg_class
      WHERE relname = 'customer') AS ss
WHERE oid = ss.reltoastrelid OR
      oid = (SELECT indexrelid
             FROM pg_index
             WHERE indrelid = ss.reltoastrelid)
ORDER BY relname;

       relname        | relpages
----------------------+----------
 pg_toast_16806       |        0
 pg_toast_16806_index |        1
```

您也可以輕鬆顯示索引大小：

```
SELECT c2.relname, c2.relpages
FROM pg_class c, pg_class c2, pg_index i
WHERE c.relname = 'customer' AND
      c.oid = i.indrelid AND
      c2.oid = i.indexrelid
ORDER BY c2.relname;

      relname      | relpages
-------------------+----------
 customer_id_index |       26
```

使用以下語法可以很容易找到最大的資料表和索引：

```
SELECT relname, relpages
FROM pg_class
ORDER BY relpages DESC;

       relname        | relpages
----------------------+----------
 bigtable             |     3290
 customer             |     3144
```
