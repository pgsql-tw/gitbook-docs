<a id="SQL-CLUSTER"></a><a id="id-1.9.3.51.1"></a>

## CLUSTER

CLUSTER — 依據索引將資料表叢集化

<a id="id-1.9.3.51.4"></a>

## 語法

```

CLUSTER [ ( option [, ...] ) ] [ table_name [ USING index_name ] ]

where option can be one of:

    VERBOSE [ boolean ]
```

<a id="id-1.9.3.51.5"></a>

## 說明

`CLUSTER` 會指示 PostgreSQL 依據 *`index_name`* 所指定的索引，將 *`table_name`* 所指定的資料表叢集化。該索引必須已經定義在 *`table_name`* 上。

資料表被叢集化時，會依據索引資訊在實體上重新排序。叢集化是一次性的操作：資料表之後被更新時，這些變更不會被叢集化。也就是說，系統不會嘗試依照索引順序來儲存新增或更新的資料列。（若有需要，可以定期再次執行此命令來重新叢集化。此外，將資料表的 `fillfactor` 儲存參數設為小於 100%，有助於在更新期間維持叢集順序，因為若同一頁面上有足夠空間，更新後的資料列會保留在該頁面上。）

資料表被叢集化時，PostgreSQL 會記住它是依據哪個索引叢集化的。`CLUSTER table_name` 這種形式會使用與先前相同的索引來重新叢集化資料表。你也可以使用 [`ALTER TABLE`](sql-altertable.md) 的 `CLUSTER` 或 `SET WITHOUT CLUSTER` 形式，設定未來叢集化操作所要使用的索引，或清除先前的任何設定。

未指定 *`table_name`* 的 `CLUSTER`，會重新叢集化目前資料庫中所有先前已叢集化、且呼叫的使用者具有權限的資料表。這種形式的 `CLUSTER` 不能在交易區塊內執行。

資料表正在叢集化時，會在其上取得 `ACCESS
EXCLUSIVE` 鎖定。這會阻止其他任何資料庫操作（包括讀取與寫入）作用於該資料表，直到 `CLUSTER` 完成為止。

<a id="id-1.9.3.51.6"></a>

## 參數

*`table_name`*
:   資料表的名稱（可能以綱要限定）。

*`index_name`*
:   索引的名稱。

`VERBOSE`
:   在每個資料表叢集化時，以 `INFO` 層級輸出進度報告。

*`boolean`*
:   指定所選選項應開啟或關閉。你可以寫 `TRUE`、`ON` 或 `1` 來啟用該選項，寫 `FALSE`、`OFF` 或 `0` 來停用它。*`boolean`* 值也可以省略，此時會假定為 `TRUE`。

<a id="id-1.9.3.51.7"></a>

## 注意事項

要將資料表叢集化，必須擁有該資料表的 `MAINTAIN` 權限。

若你是隨機存取資料表中的單一資料列，資料在資料表中的實際順序並不重要。然而，若你傾向於比其他資料更常存取某些資料，而且有一個索引會把這些資料歸在一起，那麼使用 `CLUSTER` 會讓你受益。若你要從資料表中查詢某個範圍的索引值，或查詢一個有多筆相符資料列的單一索引值，`CLUSTER` 會有幫助，因為一旦索引找出第一筆相符資料列所在的資料表頁面，其他所有相符的資料列很可能已經位於同一個資料表頁面上，因此可以節省磁碟存取並加快查詢速度。

`CLUSTER` 可以使用指定索引上的索引掃描，或（若該索引是 B-tree）先循序掃描再排序的方式，重新排序資料表。它會依據規劃器的成本參數與可用的統計資訊，嘗試選擇較快的方法。

`CLUSTER` 執行期間，[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 會暫時變更為 `pg_catalog,
pg_temp`。

使用索引掃描時，會建立一份資料表的暫存副本，其中依索引順序包含資料表的資料。資料表上每個索引的暫存副本也會一併建立。因此，你需要的磁碟可用空間至少等於資料表大小與各索引大小的總和。

使用循序掃描並排序時，還會另外建立一個暫存排序檔，因此暫存空間的峰值需求多達資料表大小的兩倍，再加上各索引的大小。這種方法通常比索引掃描方法快，但若無法容忍其磁碟空間需求，可以暫時將 [enable_sort](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-SORT) 設為 `off` 來停用這個選擇。

建議在叢集化之前，將 [maintenance_work_mem](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM) 設為合理的較大值（但不要超過你能分配給 `CLUSTER` 操作的 RAM 容量）。

由於規劃器會記錄資料表排序方式的統計資訊，建議對剛叢集化的資料表執行 [`ANALYZE`](sql-analyze.md)。否則，規劃器可能會選出不佳的查詢計畫。

由於 `CLUSTER` 會記住哪些索引已被叢集化，你可以在第一次手動將想要叢集化的資料表叢集化，然後設定一個定期執行不帶任何參數之 `CLUSTER` 的維護腳本，讓所需的資料表定期重新叢集化。

每個執行 `CLUSTER` 的後端都會在 `pg_stat_progress_cluster` 檢視表中回報其進度。詳情請參閱[第 27.4.2 節](../../server-administration/monitoring/progress-reporting.md#cluster-progress-reporting)。

將分割資料表叢集化時，會使用指定分割索引中對應的分割區，將其每個分割區叢集化。將分割資料表叢集化時，不可省略索引。對分割資料表執行的 `CLUSTER` 不能在交易區塊內執行。

<a id="id-1.9.3.51.8"></a>

## 範例

依據資料表 `employees` 的索引 `employees_ind` 將其叢集化：

```

CLUSTER employees USING employees_ind;
```

使用先前所用的相同索引將 `employees` 資料表叢集化：

```

CLUSTER employees;
```

將資料庫中所有先前已叢集化的資料表叢集化：

```

CLUSTER;
```

<a id="id-1.9.3.51.9"></a>

## 相容性

SQL 標準中沒有 `CLUSTER` 陳述式。

下列語法在 PostgreSQL 17 之前使用，目前仍受支援：

```

CLUSTER [ VERBOSE ] [ table_name [ USING index_name ] ]
```

下列語法在 PostgreSQL 8.3 之前使用，目前仍受支援：

```

CLUSTER index_name ON table_name
```

<a id="id-1.9.3.51.10"></a>

## 另請參閱

[clusterdb](../reference-client/app-clusterdb.md), [第 27.4.2 節](../../server-administration/monitoring/progress-reporting.md#cluster-progress-reporting)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-cluster.html)（原文版本：18.6；核對日期：2026-10-04）
