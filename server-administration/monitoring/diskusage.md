<a id="DISKUSAGE"></a>

## 27.6. 監控磁碟用量 [#](#DISKUSAGE)

[27.6.1. 判斷磁碟用量](diskusage.md#DISK-USAGE)

[27.6.2. 磁碟已滿故障](diskusage.md#DISK-FULL)

本節討論如何監控
PostgreSQL 資料庫系統的磁碟用量。

<a id="DISK-USAGE"></a>

### 27.6.1. 判斷磁碟用量 [#](#DISK-USAGE)

<a id="id-1.6.14.11.3.2"></a>

每個資料表都有一個主要的堆積（heap）磁碟檔案，大部分資料都儲存在其中。
如果資料表有任何可能含有很寬之值的欄位，
該資料表可能還會關聯一個 TOAST 檔案，
用來儲存太寬而無法順利放進主資料表的值
（請參閱[第 66.2 節](../../internals/storage/storage-toast.md)）。若 TOAST 資料表存在，
它上面會有一個有效的索引。基礎資料表也可能有
與其關聯的索引。每個資料表與索引都儲存在
各自獨立的磁碟檔案中——若檔案會超過 1 GB，
則可能超過一個檔案。這些檔案的命名慣例說明於
[第 66.1 節](../../internals/storage/storage-file-layout.md)。

你可以透過三種方式監控磁碟空間：
使用[表 9.102](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-DBSIZE)所列的 SQL 函式、
使用 [oid2name](../../appendixes/contrib-prog/oid2name.md) 模組，或
以手動方式檢查系統目錄。
SQL 函式最容易使用，一般也建議使用它們。
本節其餘部分示範如何透過檢查
系統目錄來做到這件事。

在最近執行過 vacuum 或 analyze 的資料庫上使用 psql，
你可以發出查詢來查看任何資料表的磁碟用量：

```

SELECT pg_relation_filepath(oid), relpages FROM pg_class WHERE relname = 'customer';

 pg_relation_filepath | relpages
----------------------+----------
 base/16384/16806     |       60
(1 row)
```

每個頁面通常是 8 KB。（請記住，`relpages`
只會由 `VACUUM`、`ANALYZE` 以及
少數 DDL 命令（例如 `CREATE INDEX`）更新。）如果你想直接
檢查資料表的磁碟檔案，檔案路徑名稱就會派上用場。

若要顯示 TOAST 資料表所使用的空間，可以使用
如下的查詢：

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

你也可以輕鬆顯示索引的大小：

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

利用這些資訊，就能輕鬆找出你最大的資料表與索引：

```

SELECT relname, relpages
FROM pg_class
ORDER BY relpages DESC;

       relname        | relpages
----------------------+----------
 bigtable             |     3290
 customer             |     3144
```

<a id="DISK-FULL"></a>

### 27.6.2. 磁碟已滿故障 [#](#DISK-FULL)

資料庫管理員最重要的磁碟監控工作，
就是確保磁碟不會滿。資料磁碟寫滿
不會導致資料損毀，但可能會使有用的活動
無法進行。若存放 WAL 檔案的磁碟寫滿，資料庫
伺服器可能會發生 panic，並因此關閉。

如果你無法透過刪除其他東西來釋放磁碟上的額外空間，
可以利用資料表空間，將部分資料庫檔案移到其他檔案
系統上。關於這點的更多資訊，請參閱[第 22.6 節](../managing-databases/manage-ag-tablespaces.md)。

<a id="DISK-FULL-TIP"></a>

### 提示

有些檔案系統在快要滿的時候效能會很差，因此
不要等到磁碟完全滿了才採取行動。

如果你的系統支援依使用者設定的磁碟配額，那麼資料庫
自然會受到伺服器執行身分所屬使用者被設定的任何配額所限制。
超出配額會造成與磁碟空間完全用盡相同的不良影響。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/diskusage.html)（原文版本：18.6；核對日期：2026-10-10）
