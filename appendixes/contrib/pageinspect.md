<a id="PAGEINSPECT"></a>

## F.23. pageinspect — 資料庫頁面的低階檢查 [#](#pageinspect) <a href="#pageinspect" id="pageinspect"></a>

[F.23.1. 一般函式](pageinspect.md#pageinspect-general-funcs)

[F.23.2. 堆積函式](pageinspect.md#pageinspect-heap-funcs)

[F.23.3. B-tree 函式](pageinspect.md#pageinspect-b-tree-funcs)

[F.23.4. BRIN 函式](pageinspect.md#pageinspect-brin-funcs)

[F.23.5. GIN 函式](pageinspect.md#pageinspect-gin-funcs)

[F.23.6. GiST 函式](pageinspect.md#pageinspect-gist-funcs)

[F.23.7. 雜湊函式](pageinspect.md#pageinspect-hash-funcs)

<a id="id-1.11.7.33.2"></a>

`pageinspect` 模組提供的函式可讓你在低階層面檢查資料庫頁面的內容，這對除錯很有用。所有這些函式都只能由超級使用者使用。

<a id="PAGEINSPECT-GENERAL-FUNCS"></a>

### F.23.1. 一般函式 [#](#pageinspect-general-funcs) <a href="#pageinspect-general-funcs" id="pageinspect-general-funcs"></a>

`get_raw_page(relname text, fork text, blkno bigint) returns bytea` <a id="id-1.11.7.33.4.2.1.1.2"></a>
:   `get_raw_page` 讀取指定名稱之關聯的指定區塊，並以 `bytea` 值傳回其副本。這樣便能取得該區塊在單一時間點上一致的副本。*`fork`* 應為：`'main'` 表示主資料分支（fork），`'fsm'` 表示[可用空間對應表](../../internals/storage/storage-fsm.md)，`'vm'` 表示[可見性對應表](../../internals/storage/storage-vm.md)，或 `'init'` 表示初始化分支。

`get_raw_page(relname text, blkno bigint) returns bytea`
:   `get_raw_page` 的簡寫版本，用於從主分支讀取。等同於 `get_raw_page(relname, 'main', blkno)`。

`page_header(page bytea) returns record` <a id="id-1.11.7.33.4.2.3.1.2"></a>

`page_header` 顯示所有 PostgreSQL 堆積頁面與索引頁面共有的欄位。

應傳入以 `get_raw_page` 取得的頁面映像作為引數。例如：

```

    test=# SELECT * FROM page_header(get_raw_page('pg_class', 0));
        lsn    | checksum | flags  | lower | upper | special | pagesize | version | prune_xid
    -----------+----------+--------+-------+-------+---------+----------+---------+-----------
     0/24A1B50 |        0 |      1 |   232 |   368 |    8192 |     8192 |       4 |         0
```

傳回的欄位對應於 `PageHeaderData` 結構中的欄位。詳細資訊請參閱 `src/include/storage/bufpage.h`。

`checksum` 欄位是儲存在頁面中的校驗和；若頁面因故損毀，此值可能不正確。若此執行個體停用了資料校驗和，則儲存的值沒有意義。

`page_checksum(page bytea, blkno bigint) returns smallint` <a id="id-1.11.7.33.4.2.4.1.2"></a>

`page_checksum` 計算頁面的校驗和，計算方式就如同該頁面位於給定的區塊。

應傳入以 `get_raw_page` 取得的頁面映像作為引數。例如：

```

    test=# SELECT page_checksum(get_raw_page('pg_class', 0), 0);
     page_checksum
    ---------------
             13443
```

請注意，校驗和取決於區塊編號，因此應傳入相符的區塊編號（除非是在進行特殊的除錯）。

以此函式計算出的校驗和，可以與 `page_header` 函式結果中的 `checksum` 欄位比較。若此執行個體啟用了資料校驗和，這兩個值應該相等。

`fsm_page_contents(page bytea) returns text` <a id="id-1.11.7.33.4.2.5.1.2"></a>

`fsm_page_contents` 顯示 FSM 頁面的內部節點結構。例如：

```

    test=# SELECT fsm_page_contents(get_raw_page('pg_class', 'fsm', 0));
```

輸出是一個多行字串，頁面內二元樹的每個節點各占一行。只會印出不為零的節點。所謂的「next」指標（指向頁面中下一個要傳回的槽位）也會一併印出。

關於 FSM 頁面結構的更多資訊，請參閱 `src/backend/storage/freespace/README`。

<a id="PAGEINSPECT-HEAP-FUNCS"></a>

### F.23.2. 堆積函式 [#](#pageinspect-heap-funcs) <a href="#pageinspect-heap-funcs" id="pageinspect-heap-funcs"></a>

`heap_page_items(page bytea) returns setof record` <a id="id-1.11.7.33.5.2.1.1.2"></a>

`heap_page_items` 顯示堆積頁面上的所有行指標（line pointer）。對於使用中的行指標，也會顯示元組（tuple）標頭以及元組的原始資料。所有元組都會顯示，不論在複製原始頁面的當下，這些元組對 MVCC 快照是否可見。

應傳入以 `get_raw_page` 取得的堆積頁面映像作為引數。例如：

```

    test=# SELECT * FROM heap_page_items(get_raw_page('pg_class', 0));
```

關於傳回欄位的說明，請參閱 `src/include/storage/itemid.h` 與 `src/include/access/htup_details.h`。

可以使用 `heap_tuple_infomask_flags` 函式，拆解堆積元組之 `t_infomask` 與 `t_infomask2` 的旗標位元。

`tuple_data_split(rel_oid oid, t_data bytea, t_infomask integer, t_infomask2 integer, t_bits text [, do_detoast bool]) returns bytea[]` <a id="id-1.11.7.33.5.2.2.1.2"></a>

`tuple_data_split` 以與後端內部相同的方式，將元組資料拆分為各個屬性。

```

    test=# SELECT tuple_data_split('pg_class'::regclass, t_data, t_infomask, t_infomask2, t_bits) FROM heap_page_items(get_raw_page('pg_class', 0));
```

呼叫此函式時，應使用與 `heap_page_items` 傳回屬性相同的引數。

若 *`do_detoast`* 為 `true`，屬性會視需要解除 TOAST（detoast）。預設值為 `false`。

`heap_page_item_attrs(page bytea, rel_oid regclass [, do_detoast bool]) returns setof record` <a id="id-1.11.7.33.5.2.3.1.2"></a>

`heap_page_item_attrs` 等同於 `heap_page_items`，差別在於它以屬性陣列的形式傳回元組原始資料，這些屬性可依 *`do_detoast`* 選擇是否解除 TOAST，該參數預設為 `false`。

應傳入以 `get_raw_page` 取得的堆積頁面映像作為引數。例如：

```

    test=# SELECT * FROM heap_page_item_attrs(get_raw_page('pg_class', 0), 'pg_class'::regclass);
```

`heap_tuple_infomask_flags(t_infomask integer, t_infomask2 integer) returns record` <a id="id-1.11.7.33.5.2.4.1.2"></a>

`heap_tuple_infomask_flags` 將 `heap_page_items` 傳回的 `t_infomask` 與 `t_infomask2` 解碼為一組人類可讀、由旗標名稱組成的陣列，其中一個欄位包含所有旗標，另一個欄位包含組合旗標。例如：

```

    test=# SELECT t_ctid, raw_flags, combined_flags
             FROM heap_page_items(get_raw_page('pg_class', 0)),
               LATERAL heap_tuple_infomask_flags(t_infomask, t_infomask2)
             WHERE t_infomask IS NOT NULL OR t_infomask2 IS NOT NULL;
```

呼叫此函式時，應使用與 `heap_page_items` 傳回屬性相同的引數。

組合旗標用於顯示會考量超過一個原始位元之值的原始碼層級巨集，例如 `HEAP_XMIN_FROZEN`。

關於傳回之旗標名稱的說明，請參閱 `src/include/access/htup_details.h`。

<a id="PAGEINSPECT-B-TREE-FUNCS"></a>

### F.23.3. B-tree 函式 [#](#pageinspect-b-tree-funcs) <a href="#pageinspect-b-tree-funcs" id="pageinspect-b-tree-funcs"></a>

`bt_metap(relname text) returns record` <a id="id-1.11.7.33.6.2.1.1.2"></a>
:   `bt_metap` 傳回 B-tree 索引中繼頁面（metapage）的相關資訊。例如：

    ```

    test=# SELECT * FROM bt_metap('pg_cast_oid_index');
    -[ RECORD 1 ]-------------+-------
    magic                     | 340322
    version                   | 4
    root                      | 1
    level                     | 0
    fastroot                  | 1
    fastlevel                 | 0
    last_cleanup_num_delpages | 0
    last_cleanup_num_tuples   | 230
    allequalimage             | f
    ```

`bt_page_stats(relname text, blkno bigint) returns record` <a id="id-1.11.7.33.6.2.2.1.2"></a>
:   `bt_page_stats` 傳回 B-tree 索引某個資料頁面的摘要資訊。例如：

    ```

    test=# SELECT * FROM bt_page_stats('pg_cast_oid_index', 1);
    -[ RECORD 1 ]-+-----
    blkno         | 1
    type          | l
    live_items    | 224
    dead_items    | 0
    avg_item_size | 16
    page_size     | 8192
    free_size     | 3668
    btpo_prev     | 0
    btpo_next     | 0
    btpo_level    | 0
    btpo_flags    | 3
    ```

`bt_multi_page_stats(relname text, blkno bigint, blk_count bigint) returns setof record` <a id="id-1.11.7.33.6.2.3.1.2"></a>
:   `bt_multi_page_stats` 傳回與 `bt_page_stats` 相同的資訊，但對象是從 *`blkno`* 開始、延伸 *`blk_count`* 個頁面之範圍內的每個頁面。若 *`blk_count`* 為負數，則會回報從 *`blkno`* 到索引結尾的所有頁面。例如：

    ```

    test=# SELECT * FROM bt_multi_page_stats('pg_proc_oid_index', 5, 2);
    -[ RECORD 1 ]-+-----
    blkno         | 5
    type          | l
    live_items    | 367
    dead_items    | 0
    avg_item_size | 16
    page_size     | 8192
    free_size     | 808
    btpo_prev     | 4
    btpo_next     | 6
    btpo_level    | 0
    btpo_flags    | 1
    -[ RECORD 2 ]-+-----
    blkno         | 6
    type          | l
    live_items    | 367
    dead_items    | 0
    avg_item_size | 16
    page_size     | 8192
    free_size     | 808
    btpo_prev     | 5
    btpo_next     | 7
    btpo_level    | 0
    btpo_flags    | 1
    ```

`bt_page_items(relname text, blkno bigint) returns setof record` <a id="id-1.11.7.33.6.2.4.1.2"></a>

`bt_page_items` 傳回 B-tree 索引頁面上所有項目的詳細資訊。例如：

```

    test=# SELECT itemoffset, ctid, itemlen, nulls, vars, data, dead, htid, tids[0:2] AS some_tids
            FROM bt_page_items('tenk2_hundred', 5);
     itemoffset |   ctid    | itemlen | nulls | vars |          data           | dead |  htid  |      some_tids
    ------------+-----------+---------+-------+------+-------------------------+------+--------+---------------------
              1 | (16,1)    |      16 | f     | f    | 30 00 00 00 00 00 00 00 |      |        |
              2 | (16,8292) |     616 | f     | f    | 24 00 00 00 00 00 00 00 | f    | (1,6)  | {"(1,6)","(10,22)"}
              3 | (16,8292) |     616 | f     | f    | 25 00 00 00 00 00 00 00 | f    | (1,18) | {"(1,18)","(4,22)"}
              4 | (16,8292) |     616 | f     | f    | 26 00 00 00 00 00 00 00 | f    | (4,18) | {"(4,18)","(6,17)"}
              5 | (16,8292) |     616 | f     | f    | 27 00 00 00 00 00 00 00 | f    | (1,2)  | {"(1,2)","(1,19)"}
              6 | (16,8292) |     616 | f     | f    | 28 00 00 00 00 00 00 00 | f    | (2,24) | {"(2,24)","(4,11)"}
              7 | (16,8292) |     616 | f     | f    | 29 00 00 00 00 00 00 00 | f    | (2,17) | {"(2,17)","(11,2)"}
              8 | (16,8292) |     616 | f     | f    | 2a 00 00 00 00 00 00 00 | f    | (0,25) | {"(0,25)","(3,20)"}
              9 | (16,8292) |     616 | f     | f    | 2b 00 00 00 00 00 00 00 | f    | (0,10) | {"(0,10)","(0,14)"}
             10 | (16,8292) |     616 | f     | f    | 2c 00 00 00 00 00 00 00 | f    | (1,3)  | {"(1,3)","(3,9)"}
             11 | (16,8292) |     616 | f     | f    | 2d 00 00 00 00 00 00 00 | f    | (6,28) | {"(6,28)","(11,1)"}
             12 | (16,8292) |     616 | f     | f    | 2e 00 00 00 00 00 00 00 | f    | (0,27) | {"(0,27)","(1,13)"}
             13 | (16,8292) |     616 | f     | f    | 2f 00 00 00 00 00 00 00 | f    | (4,17) | {"(4,17)","(4,21)"}
    (13 rows)
```

這是一個 B-tree 葉頁面。所有指向資料表的元組恰好都是 posting list 元組（它們各自總共儲存 100 個 6 位元組的 TID）。在 `itemoffset` 編號 1 處還有一個「高鍵」（high key）元組。在此範例中，`ctid` 用來儲存每個元組的編碼資訊，不過葉頁面元組通常會改為直接在 `ctid` 欄位中儲存堆積 TID。`tids` 是以 posting list 形式儲存的 TID 清單。

在內部頁面（此處未顯示）中，`ctid` 的區塊編號部分是「下行連結」（downlink），也就是索引本身中另一個頁面的區塊編號。`ctid` 的偏移量部分（第二個數字）儲存該元組的編碼資訊，例如實際存在的欄位數（後綴截斷可能已移除不需要的後綴欄位）。被截斷的欄位視為具有「負無限大」的值。

`htid` 顯示該元組的堆積 TID，不論底層的元組表示方式為何。此值可能與 `ctid` 相符，也可能是從 posting list 元組及內部頁面元組所使用的替代表示方式解碼而來。內部頁面中的元組通常已將實作層級的堆積 TID 欄位截斷移除，這會以 NULL 的 `htid` 值表示。

請注意，任何非最右側頁面（即 `btpo_next` 欄位值不為零的任何頁面）上的第一個項目是該頁面的「高鍵」，這表示其 `data` 作為頁面上所有項目的上界，而其 `ctid` 欄位不指向另一個區塊。此外，在內部頁面上，第一個真正的資料項目（第一個不是高鍵的項目）必定會將所有欄位都截斷移除，因此其 `data` 欄位中沒有實際的值。不過，這樣的項目在其 `ctid` 欄位中確實有有效的下行連結。

關於 B-tree 索引結構的更多細節，請參閱[第 65.1.4.1 節](../../internals/indextypes/btree.md#BTREE-STRUCTURE)。關於去重複與 posting list 的更多細節，請參閱[第 65.1.4.3 節](../../internals/indextypes/btree.md#BTREE-DEDUPLICATION)。

`bt_page_items(page bytea) returns setof record` <a id="id-1.11.7.33.6.2.5.1.2"></a>

也可以將頁面以 `bytea` 值的形式傳給 `bt_page_items`。應傳入以 `get_raw_page` 取得的頁面映像作為引數。因此，上一個範例也可以改寫成這樣：

```

    test=# SELECT itemoffset, ctid, itemlen, nulls, vars, data, dead, htid, tids[0:2] AS some_tids
            FROM bt_page_items(get_raw_page('tenk2_hundred', 5));
     itemoffset |   ctid    | itemlen | nulls | vars |          data           | dead |  htid  |      some_tids
    ------------+-----------+---------+-------+------+-------------------------+------+--------+---------------------
              1 | (16,1)    |      16 | f     | f    | 30 00 00 00 00 00 00 00 |      |        |
              2 | (16,8292) |     616 | f     | f    | 24 00 00 00 00 00 00 00 | f    | (1,6)  | {"(1,6)","(10,22)"}
              3 | (16,8292) |     616 | f     | f    | 25 00 00 00 00 00 00 00 | f    | (1,18) | {"(1,18)","(4,22)"}
              4 | (16,8292) |     616 | f     | f    | 26 00 00 00 00 00 00 00 | f    | (4,18) | {"(4,18)","(6,17)"}
              5 | (16,8292) |     616 | f     | f    | 27 00 00 00 00 00 00 00 | f    | (1,2)  | {"(1,2)","(1,19)"}
              6 | (16,8292) |     616 | f     | f    | 28 00 00 00 00 00 00 00 | f    | (2,24) | {"(2,24)","(4,11)"}
              7 | (16,8292) |     616 | f     | f    | 29 00 00 00 00 00 00 00 | f    | (2,17) | {"(2,17)","(11,2)"}
              8 | (16,8292) |     616 | f     | f    | 2a 00 00 00 00 00 00 00 | f    | (0,25) | {"(0,25)","(3,20)"}
              9 | (16,8292) |     616 | f     | f    | 2b 00 00 00 00 00 00 00 | f    | (0,10) | {"(0,10)","(0,14)"}
             10 | (16,8292) |     616 | f     | f    | 2c 00 00 00 00 00 00 00 | f    | (1,3)  | {"(1,3)","(3,9)"}
             11 | (16,8292) |     616 | f     | f    | 2d 00 00 00 00 00 00 00 | f    | (6,28) | {"(6,28)","(11,1)"}
             12 | (16,8292) |     616 | f     | f    | 2e 00 00 00 00 00 00 00 | f    | (0,27) | {"(0,27)","(1,13)"}
             13 | (16,8292) |     616 | f     | f    | 2f 00 00 00 00 00 00 00 | f    | (4,17) | {"(4,17)","(4,21)"}
    (13 rows)
```

其他所有細節都與上一個項目中的說明相同。

<a id="PAGEINSPECT-BRIN-FUNCS"></a>

### F.23.4. BRIN 函式 [#](#pageinspect-brin-funcs) <a href="#pageinspect-brin-funcs" id="pageinspect-brin-funcs"></a>

`brin_page_type(page bytea) returns text` <a id="id-1.11.7.33.7.2.1.1.2"></a>
:   `brin_page_type` 傳回給定 BRIN 索引頁面的頁面類型；若該頁面不是有效的 BRIN 頁面，則擲出錯誤。例如：

    ```

    test=# SELECT brin_page_type(get_raw_page('brinidx', 0));
     brin_page_type
    ----------------
     meta
    ```

`brin_metapage_info(page bytea) returns record` <a id="id-1.11.7.33.7.2.2.1.2"></a>
:   `brin_metapage_info` 傳回 BRIN 索引中繼頁面的各種資訊。例如：

    ```

    test=# SELECT * FROM brin_metapage_info(get_raw_page('brinidx', 0));
       magic    | version | pagesperrange | lastrevmappage
    ------------+---------+---------------+----------------
     0xA8109CFA |       1 |             4 |              2
    ```

`brin_revmap_data(page bytea) returns setof tid` <a id="id-1.11.7.33.7.2.3.1.2"></a>
:   `brin_revmap_data` 傳回 BRIN 索引範圍對應（range map）頁面中的元組識別碼清單。例如：

    ```

    test=# SELECT * FROM brin_revmap_data(get_raw_page('brinidx', 2)) LIMIT 5;
      pages
    ---------
     (6,137)
     (6,138)
     (6,139)
     (6,140)
     (6,141)
    ```

`brin_page_items(page bytea, index oid) returns setof record` <a id="id-1.11.7.33.7.2.4.1.2"></a>

`brin_page_items` 傳回儲存在 BRIN 資料頁面中的資料。例如：

```

    test=# SELECT * FROM brin_page_items(get_raw_page('brinidx', 5),
                                         'brinidx')
           ORDER BY blknum, attnum LIMIT 6;
     itemoffset | blknum | attnum | allnulls | hasnulls | placeholder | empty |    value
    ------------+--------+--------+----------+----------+-------------+-------+--------------
            137 |      0 |      1 | t        | f        | f           | f     |
            137 |      0 |      2 | f        | f        | f           | f     | {1 .. 88}
            138 |      4 |      1 | t        | f        | f           | f     |
            138 |      4 |      2 | f        | f        | f           | f     | {89 .. 176}
            139 |      8 |      1 | t        | f        | f           | f     |
            139 |      8 |      2 | f        | f        | f           | f     | {177 .. 264}
```

傳回的欄位對應於 `BrinMemTuple` 與 `BrinValues` 結構中的欄位。詳細資訊請參閱 `src/include/access/brin_tuple.h`。

<a id="PAGEINSPECT-GIN-FUNCS"></a>

### F.23.5. GIN 函式 [#](#pageinspect-gin-funcs) <a href="#pageinspect-gin-funcs" id="pageinspect-gin-funcs"></a>

`gin_metapage_info(page bytea) returns record` <a id="id-1.11.7.33.8.2.1.1.2"></a>
:   `gin_metapage_info` 傳回 GIN 索引中繼頁面的相關資訊。例如：

    ```

    test=# SELECT * FROM gin_metapage_info(get_raw_page('gin_index', 0));
    -[ RECORD 1 ]----+-----------
    pending_head     | 4294967295
    pending_tail     | 4294967295
    tail_free_size   | 0
    n_pending_pages  | 0
    n_pending_tuples | 0
    n_total_pages    | 7
    n_entry_pages    | 6
    n_data_pages     | 0
    n_entries        | 693
    version          | 2
    ```

`gin_page_opaque_info(page bytea) returns record` <a id="id-1.11.7.33.8.2.2.1.2"></a>
:   `gin_page_opaque_info` 傳回 GIN 索引不透明區域（opaque area）的相關資訊，像是頁面類型。例如：

    ```

    test=# SELECT * FROM gin_page_opaque_info(get_raw_page('gin_index', 2));
     rightlink | maxoff |         flags
    -----------+--------+------------------------
             5 |      0 | {data,leaf,compressed}
    (1 row)
    ```

`gin_leafpage_items(page bytea) returns setof record` <a id="id-1.11.7.33.8.2.3.1.2"></a>
:   `gin_leafpage_items` 傳回壓縮 GIN 葉頁面中所儲存資料的相關資訊。例如：

    ```

    test=# SELECT first_tid, nbytes, tids[0:5] AS some_tids
            FROM gin_leafpage_items(get_raw_page('gin_test_idx', 2));
     first_tid | nbytes |                        some_tids
    -----------+--------+----------------------------------------------------------
     (8,41)    |    244 | {"(8,41)","(8,43)","(8,44)","(8,45)","(8,46)"}
     (10,45)   |    248 | {"(10,45)","(10,46)","(10,47)","(10,48)","(10,49)"}
     (12,52)   |    248 | {"(12,52)","(12,53)","(12,54)","(12,55)","(12,56)"}
     (14,59)   |    320 | {"(14,59)","(14,60)","(14,61)","(14,62)","(14,63)"}
     (167,16)  |    376 | {"(167,16)","(167,17)","(167,18)","(167,19)","(167,20)"}
     (170,30)  |    376 | {"(170,30)","(170,31)","(170,32)","(170,33)","(170,34)"}
     (173,44)  |    197 | {"(173,44)","(173,45)","(173,46)","(173,47)","(173,48)"}
    (7 rows)
    ```

<a id="PAGEINSPECT-GIST-FUNCS"></a>

### F.23.6. GiST 函式 [#](#pageinspect-gist-funcs) <a href="#pageinspect-gist-funcs" id="pageinspect-gist-funcs"></a>

`gist_page_opaque_info(page bytea) returns record` <a id="id-1.11.7.33.9.2.1.1.2"></a>
:   `gist_page_opaque_info` 傳回 GiST 索引頁面不透明區域中的資訊，像是 NSN、右鏈結（rightlink）與頁面類型。例如：

    ```

    test=# SELECT * FROM gist_page_opaque_info(get_raw_page('test_gist_idx', 2));
     lsn | nsn | rightlink | flags
    -----+-----+-----------+--------
     0/1 | 0/0 |         1 | {leaf}
    (1 row)
    ```

`gist_page_items(page bytea, index_oid regclass) returns setof record` <a id="id-1.11.7.33.9.2.2.1.2"></a>
:   `gist_page_items` 傳回 GiST 索引頁面中所儲存資料的相關資訊。例如：

    ```

    test=# SELECT * FROM gist_page_items(get_raw_page('test_gist_idx', 0), 'test_gist_idx');
     itemoffset |   ctid    | itemlen | dead |             keys
    ------------+-----------+---------+------+-------------------------------
              1 | (1,65535) |      40 | f    | (p)=("(185,185),(1,1)")
              2 | (2,65535) |      40 | f    | (p)=("(370,370),(186,186)")
              3 | (3,65535) |      40 | f    | (p)=("(555,555),(371,371)")
              4 | (4,65535) |      40 | f    | (p)=("(740,740),(556,556)")
              5 | (5,65535) |      40 | f    | (p)=("(870,870),(741,741)")
              6 | (6,65535) |      40 | f    | (p)=("(1000,1000),(871,871)")
    (6 rows)
    ```

`gist_page_items_bytea(page bytea) returns setof record` <a id="id-1.11.7.33.9.2.3.1.2"></a>

與 `gist_page_items` 相同，但以原始 `bytea` 二進位資料傳回鍵值資料。由於它不會嘗試解碼鍵值，因此不需要知道涉及的是哪個索引。例如：

```

    test=# SELECT * FROM gist_page_items_bytea(get_raw_page('test_gist_idx', 0));
     itemoffset |   ctid    | itemlen | dead |                                      key_data
    ------------+-----------+---------+------+-----------------------------------------​-------------------------------------------
              1 | (1,65535) |      40 | f    | \x00000100ffff28000000000000c0644000000000​00c06440000000000000f03f000000000000f03f
              2 | (2,65535) |      40 | f    | \x00000200ffff28000000000000c0744000000000​00c074400000000000e064400000000000e06440
              3 | (3,65535) |      40 | f    | \x00000300ffff28000000000000207f4000000000​00207f400000000000d074400000000000d07440
              4 | (4,65535) |      40 | f    | \x00000400ffff28000000000000c0844000000000​00c084400000000000307f400000000000307f40
              5 | (5,65535) |      40 | f    | \x00000500ffff28000000000000f0894000000000​00f089400000000000c884400000000000c88440
              6 | (6,65535) |      40 | f    | \x00000600ffff28000000000000208f4000000000​00208f400000000000f889400000000000f88940
              7 | (7,65535) |      40 | f    | \x00000700ffff28000000000000408f4000000000​00408f400000000000288f400000000000288f40
    (7 rows)
```

譯註：此範例與上一個 gist_page_items 範例查詢的是同一個索引的同一個頁面（區塊 0），但上一個範例輸出 6 列、此處輸出 7 列，兩者並不一致，閱讀時請勿逐列對照。

<a id="PAGEINSPECT-HASH-FUNCS"></a>

### F.23.7. 雜湊函式 [#](#pageinspect-hash-funcs) <a href="#pageinspect-hash-funcs" id="pageinspect-hash-funcs"></a>

`hash_page_type(page bytea) returns text` <a id="id-1.11.7.33.10.2.1.1.2"></a>
:   `hash_page_type` 傳回給定 HASH 索引頁面的頁面類型。例如：

    ```

    test=# SELECT hash_page_type(get_raw_page('con_hash_index', 0));
     hash_page_type
    ----------------
     metapage
    ```

`hash_page_stats(page bytea) returns setof record` <a id="id-1.11.7.33.10.2.2.1.2"></a>

`hash_page_stats` 傳回 HASH 索引中桶頁面或溢位頁面的相關資訊。例如：

```

    test=# SELECT * FROM hash_page_stats(get_raw_page('con_hash_index', 1));
    -[ RECORD 1 ]---+-----------
    live_items      | 407
    dead_items      | 0
    page_size       | 8192
    free_size       | 8
    hasho_prevblkno | 4096
    hasho_nextblkno | 8474
    hasho_bucket    | 0
    hasho_flag      | 66
    hasho_page_id   | 65408
```

譯註：原文函式簽章寫作 returns setof record，但 pageinspect 擴充功能腳本是以 OUT 參數定義此函式，並未宣告 SETOF，因此實際上只傳回單一筆紀錄（上方範例輸出也只有一筆 RECORD）。

`hash_page_items(page bytea) returns setof record` <a id="id-1.11.7.33.10.2.3.1.2"></a>
:   `hash_page_items` 傳回 HASH 索引頁面之桶頁面或溢位頁面中所儲存資料的相關資訊。例如：

    ```

    test=# SELECT * FROM hash_page_items(get_raw_page('con_hash_index', 1)) LIMIT 5;
     itemoffset |   ctid    |    data
    ------------+-----------+------------
              1 | (899,77)  | 1053474816
              2 | (897,29)  | 1053474816
              3 | (894,207) | 1053474816
              4 | (892,159) | 1053474816
              5 | (890,111) | 1053474816
    ```

`hash_bitmap_info(index oid, blkno bigint) returns record` <a id="id-1.11.7.33.10.2.4.1.2"></a>
:   `hash_bitmap_info` 顯示 HASH 索引中，特定溢位頁面在點陣圖頁面中所對應位元的狀態。例如：

    ```

    test=# SELECT * FROM hash_bitmap_info('con_hash_index', 2052);
     bitmapblkno | bitmapbit | bitstatus
    -------------+-----------+-----------
              65 |         3 | t
    ```

`hash_metapage_info(page bytea) returns record` <a id="id-1.11.7.33.10.2.5.1.2"></a>
:   `hash_metapage_info` 傳回儲存在 HASH 索引中繼頁面中的資訊。例如：

    ```

    test=# SELECT magic, version, ntuples, ffactor, bsize, bmsize, bmshift,
    test-#     maxbucket, highmask, lowmask, ovflpoint, firstfree, nmaps, procid,
    test-#     regexp_replace(spares::text, '(,0)*}', '}') as spares,
    test-#     regexp_replace(mapp::text, '(,0)*}', '}') as mapp
    test-# FROM hash_metapage_info(get_raw_page('con_hash_index', 0));
    -[ RECORD 1 ]-------------------------------------------------​------------------------------
    magic     | 105121344
    version   | 4
    ntuples   | 500500
    ffactor   | 40
    bsize     | 8152
    bmsize    | 4096
    bmshift   | 15
    maxbucket | 12512
    highmask  | 16383
    lowmask   | 8191
    ovflpoint | 28
    firstfree | 1204
    nmaps     | 1
    procid    | 450
    spares    | {0,0,0,0,0,0,1,1,1,1,1,1,1,1,3,4,4,4,45,55,58,59,​508,567,628,704,1193,1202,1204}
    mapp      | {65}
    ```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pageinspect.html)（原文版本：18.6；核對日期：2026-10-23）
