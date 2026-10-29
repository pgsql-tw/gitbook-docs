<a id="PGWALINSPECT"></a>

## F.37. pg_walinspect — 低階 WAL 檢視 [#](#pgwalinspect) <a href="#pgwalinspect" id="pgwalinspect"></a>

[F.37.1. 一般函式](pgwalinspect.md#pgwalinspect-funcs)

[F.37.2. 作者](pgwalinspect.md#pgwalinspect-author)

<a id="id-1.11.7.47.2"></a>

`pg_walinspect` 模組提供 SQL 函式，讓你以低階方式檢視執行中
PostgreSQL 資料庫叢集的預寫式日誌內容，可用於除錯、分析、報告或教學用途。它與
[pg_waldump](../../reference/reference-server/pgwaldump.md) 類似，但是透過 SQL 存取，而不是另一個獨立的公用程式。

此模組的所有函式都會使用伺服器目前的時間軸 ID 提供 WAL 資訊。

### 注意

呼叫 `pg_walinspect` 函式時，通常會使用一個 LSN 引數，指定某筆已知且感興趣的
WAL 紀錄*開始*的位置。然而，有些函式（例如
`pg_logical_emit_message`）傳回的是剛插入之紀錄*之後*的 LSN。

### 提示

所有顯示某個 LSN 範圍內紀錄資訊的 `pg_walinspect` 函式，都允許
*`end_lsn`* 引數位於伺服器目前 LSN 之後。使用「來自未來」的
*`end_lsn`* 不會引發錯誤。

將值 `FFFFFFFF/FFFFFFFF`（最大的有效
`pg_lsn` 值）作為 *`end_lsn`*
引數傳入可能較為方便。這等同於傳入與伺服器目前 LSN 相符的
*`end_lsn`* 引數。

預設情況下，只有超級使用者與 `pg_read_server_files` 角色的成員可以使用這些函式。超級使用者可以使用
`GRANT` 將存取權授與其他人。

<a id="PGWALINSPECT-FUNCS"></a>

### F.37.1. 一般函式 [#](#pgwalinspect-funcs) <a href="#pgwalinspect-funcs" id="pgwalinspect-funcs"></a>

<a id="PGWALINSPECT-FUNCS-PG-GET-WAL-RECORD-INFO"></a>

`pg_get_wal_record_info(in_lsn pg_lsn) returns record` [#](#PGWALINSPECT-FUNCS-PG-GET-WAL-RECORD-INFO)

取得位於 *`in_lsn`* 引數所指位置或其後之紀錄的 WAL 紀錄資訊。例如：

```

    postgres=# SELECT * FROM pg_get_wal_record_info('0/E419E28');
    -[ RECORD 1 ]----+-------------------------------------------------
    start_lsn        | 0/E419E28
    end_lsn          | 0/E419E68
    prev_lsn         | 0/E419D78
    xid              | 0
    resource_manager | Heap2
    record_type      | VACUUM
    record_length    | 58
    main_data_length | 2
    fpi_length       | 0
    description      | nunused: 5, unused: [1, 2, 3, 4, 5]
    block_ref        | blkref #0: rel 1663/16385/1249 fork main blk 364
```

若 *`in_lsn`* 不在某筆 WAL 紀錄的開頭，則改為顯示下一筆有效 WAL
紀錄的資訊。若沒有下一筆有效的 WAL 紀錄，此函式會引發錯誤。
<a id="PGWALINSPECT-FUNCS-PG-GET-WAL-RECORDS-INFO"></a>

`pg_get_wal_records_info(start_lsn pg_lsn, end_lsn pg_lsn) returns setof record` [#](#PGWALINSPECT-FUNCS-PG-GET-WAL-RECORDS-INFO)

取得 *`start_lsn`* 與 *`end_lsn`*
之間所有有效 WAL 紀錄的資訊。每筆 WAL 紀錄傳回一個資料列。例如：

```

    postgres=# SELECT * FROM pg_get_wal_records_info('0/1E913618', '0/1E913740') LIMIT 1;
    -[ RECORD 1 ]----+--------------------------------------------------------------
    start_lsn        | 0/1E913618
    end_lsn          | 0/1E913650
    prev_lsn         | 0/1E9135A0
    xid              | 0
    resource_manager | Standby
    record_type      | RUNNING_XACTS
    record_length    | 50
    main_data_length | 24
    fpi_length       | 0
    description      | nextXid 33775 latestCompletedXid 33774 oldestRunningXid 33775
    block_ref        |
```

若 *`start_lsn`* 無法使用，此函式會引發錯誤。
<a id="PGWALINSPECT-FUNCS-PG-GET-WAL-BLOCK-INFO"></a>

`pg_get_wal_block_info(start_lsn pg_lsn, end_lsn pg_lsn, show_data boolean DEFAULT true) returns setof record` [#](#PGWALINSPECT-FUNCS-PG-GET-WAL-BLOCK-INFO)
:   從 *`start_lsn`* 與
    *`end_lsn`* 之間所有具有一個或多個區塊參照的有效 WAL
    紀錄中，取得每個區塊參照的資訊。每筆 WAL 紀錄的每個區塊參照各傳回一個資料列。
    例如：

    ```

    postgres=# SELECT * FROM pg_get_wal_block_info('0/1230278', '0/12302B8');
    -[ RECORD 1 ]-----+-----------------------------------
    start_lsn         | 0/1230278
    end_lsn           | 0/12302B8
    prev_lsn          | 0/122FD40
    block_id          | 0
    reltablespace     | 1663
    reldatabase       | 1
    relfilenode       | 2658
    relforknumber     | 0
    relblocknumber    | 11
    xid               | 341
    resource_manager  | Btree
    record_type       | INSERT_LEAF
    record_length     | 64
    main_data_length  | 2
    block_data_length | 16
    block_fpi_length  | 0
    block_fpi_info    |
    description       | off: 46
    block_data        | \x00002a00070010402630000070696400
    block_fpi_data    |
    ```

    此範例涉及的 WAL 紀錄只包含一個區塊參照，但許多 WAL
    紀錄包含多個區塊參照。保證
    `pg_get_wal_block_info` 輸出的資料列中，
    *`start_lsn`* 與
    *`block_id`* 值的組合都是唯一的。

    此處顯示的大部分資訊，與給定相同引數時
    `pg_get_wal_records_info` 會顯示的輸出相符。然而，
    `pg_get_wal_block_info` 會將每筆 WAL
    紀錄的資訊展開，對每個區塊參照輸出一個資料列，因此某些細節是在區塊參照層級、而不是整筆紀錄層級追蹤。這種結構適用於追蹤個別區塊如何隨時間變化的查詢。請注意，沒有區塊參照的紀錄（例如
    `COMMIT` WAL 紀錄）不會傳回任何資料列，因此 `pg_get_wal_block_info`
    實際傳回的資料列可能比
    `pg_get_wal_records_info` *更少*。

    `reltablespace`、
    `reldatabase` 與
    `relfilenode` 參數分別參照
    [`pg_tablespace`](../../internals/catalogs/catalog-pg-tablespace.md).`oid`、
    [`pg_database`](../../internals/catalogs/catalog-pg-database.md).`oid` 與
    [`pg_class`](../../internals/catalogs/catalog-pg-class.md).`relfilenode`。
    `relforknumber`
    欄位是該區塊參照在關聯內的分支（fork）編號；詳細資訊請參閱 `common/relpath.h`。

    ### 提示

    `pg_filenode_relation` 函式（請參閱
    [表 9.103](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-DBLOCATION)）可以協助你判斷原本執行期間修改的是哪個關聯。

    用戶端可以避免具體化區塊資料的額外負擔，這可能使函式執行明顯加快。當
    *`show_data`* 設為 `false` 時，會省略 `block_data`
    與 `block_fpi_data` 值（也就是說，對所有傳回的資料列，
    `block_data` 與
    `block_fpi_data` 這兩個 `OUT`
    引數都是 `NULL`）。
    顯然，此最佳化只適用於並非真正需要區塊資料的查詢。

    若 *`start_lsn`* 無法使用，此函式會引發錯誤。
<a id="PGWALINSPECT-FUNCS-PG-GET-WAL-STATS"></a>

`pg_get_wal_stats(start_lsn pg_lsn, end_lsn pg_lsn, per_record boolean DEFAULT false) returns setof record` [#](#PGWALINSPECT-FUNCS-PG-GET-WAL-STATS)

取得 *`start_lsn`* 與
*`end_lsn`* 之間所有有效 WAL 紀錄的統計資訊。預設情況下，每種
*`resource_manager`* 類型傳回一個資料列。當
*`per_record`* 設為 `true` 時，
每種 *`record_type`* 傳回一個資料列。
例如：

```

    postgres=# SELECT * FROM pg_get_wal_stats('0/1E847D00', '0/1E84F500')
               WHERE count > 0 AND
                     "resource_manager/record_type" = 'Transaction'
               LIMIT 1;
    -[ RECORD 1 ]----------------+-------------------
    resource_manager/record_type | Transaction
    count                        | 2
    count_percentage             | 8
    record_size                  | 875
    record_size_percentage       | 41.23468426013195
    fpi_size                     | 0
    fpi_size_percentage          | 0
    combined_size                | 875
    combined_size_percentage     | 2.8634072910530795
```

若 *`start_lsn`* 無法使用，此函式會引發錯誤。

<a id="PGWALINSPECT-AUTHOR"></a>

### F.37.2. 作者 [#](#pgwalinspect-author) <a href="#pgwalinspect-author" id="pgwalinspect-author"></a>

Bharath Rupireddy `<bharath.rupireddyforpostgres@gmail.com>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgwalinspect.html)（原文版本：18.6；核對日期：2026-10-22）
