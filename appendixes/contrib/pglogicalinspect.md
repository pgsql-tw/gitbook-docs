<a id="PGLOGICALINSPECT"></a>

## F.28. pg_logicalinspect — 邏輯解碼元件檢查 [#](#pglogicalinspect) <a href="#pglogicalinspect" id="pglogicalinspect"></a>

[F.28.1. 函式](pglogicalinspect.md#pglogicalinspect-funcs)

[F.28.2. 作者](pglogicalinspect.md#pglogicalinspect-author)

<a id="id-1.11.7.38.2"></a>

`pg_logicalinspect` 模組提供 SQL 函式，讓你可以檢查邏輯解碼元件的內容。它可以檢查執行中 PostgreSQL 資料庫叢集的序列化邏輯快照，這對除錯或教學用途很有幫助。

預設情況下，只有超級使用者與 `pg_read_server_files` 角色的成員可以使用這些函式。超級使用者可以使用 `GRANT` 將存取權授與其他人。

<a id="PGLOGICALINSPECT-FUNCS"></a>

### F.28.1. 函式 [#](#pglogicalinspect-funcs) <a href="#pglogicalinspect-funcs" id="pglogicalinspect-funcs"></a>

<a id="PGLOGICALINSPECT-FUNCS-PG-GET-LOGICAL-SNAPSHOT-META"></a>

`pg_get_logical_snapshot_meta(filename text) returns record` [#](#PGLOGICALINSPECT-FUNCS-PG-GET-LOGICAL-SNAPSHOT-META)
:   取得位於伺服器 `pg_logical/snapshots` 目錄中某個快照檔的邏輯快照中繼資料。
    *`filename`* 引數代表快照檔名。
    例如：

    ```

    postgres=# SELECT * FROM pg_ls_logicalsnapdir();
    -[ RECORD 1 ]+-----------------------
    name         | 0-40796E18.snap
    size         | 152
    modification | 2024-08-14 16:36:32+00

    postgres=# SELECT * FROM pg_get_logical_snapshot_meta('0-40796E18.snap');
    -[ RECORD 1 ]--------
    magic    | 1369563137
    checksum | 1028045905
    version  | 6

    postgres=# SELECT ss.name, meta.* FROM pg_ls_logicalsnapdir() AS ss,
    pg_get_logical_snapshot_meta(ss.name) AS meta;
    -[ RECORD 1 ]-------------
    name     | 0-40796E18.snap
    magic    | 1369563137
    checksum | 1028045905
    version  | 6
    ```

    若 *`filename`* 不符合任何快照檔，
    此函式會擲出錯誤。
<a id="PGLOGICALINSPECT-FUNCS-PG-GET-LOGICAL-SNAPSHOT-INFO"></a>

`pg_get_logical_snapshot_info(filename text) returns record` [#](#PGLOGICALINSPECT-FUNCS-PG-GET-LOGICAL-SNAPSHOT-INFO)
:   取得位於伺服器 `pg_logical/snapshots` 目錄中某個快照檔的邏輯快照資訊。
    *`filename`* 引數代表快照檔名。
    例如：

    ```

    postgres=# SELECT * FROM pg_ls_logicalsnapdir();
    -[ RECORD 1 ]+-----------------------
    name         | 0-40796E18.snap
    size         | 152
    modification | 2024-08-14 16:36:32+00

    postgres=# SELECT * FROM pg_get_logical_snapshot_info('0-40796E18.snap');
    -[ RECORD 1 ]------------+-----------
    state                    | consistent
    xmin                     | 751
    xmax                     | 751
    start_decoding_at        | 0/40796AF8
    two_phase_at             | 0/40796AF8
    initial_xmin_horizon     | 0
    building_full_snapshot   | f
    in_slot_creation         | f
    last_serialized_snapshot | 0/0
    next_phase_at            | 0
    committed_count          | 0
    committed_xip            |
    catchange_count          | 2
    catchange_xip            | {751,752}

    postgres=# SELECT ss.name, info.* FROM pg_ls_logicalsnapdir() AS ss,
    pg_get_logical_snapshot_info(ss.name) AS info;
    -[ RECORD 1 ]------------+----------------
    name                     | 0-40796E18.snap
    state                    | consistent
    xmin                     | 751
    xmax                     | 751
    start_decoding_at        | 0/40796AF8
    two_phase_at             | 0/40796AF8
    initial_xmin_horizon     | 0
    building_full_snapshot   | f
    in_slot_creation         | f
    last_serialized_snapshot | 0/0
    next_phase_at            | 0
    committed_count          | 0
    committed_xip            |
    catchange_count          | 2
    catchange_xip            | {751,752}
    ```

    若 *`filename`* 不符合任何快照檔，
    此函式會擲出錯誤。

<a id="PGLOGICALINSPECT-AUTHOR"></a>

### F.28.2. 作者 [#](#pglogicalinspect-author) <a href="#pglogicalinspect-author" id="pglogicalinspect-author"></a>

Bertrand Drouvot `<bertranddrouvot.pg@gmail.com>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pglogicalinspect.html)（原文版本：18.6；核對日期：2026-10-23）
