<a id="PGROWLOCKS"></a>

## F.31. pgrowlocks — 顯示資料表的資料列鎖定資訊 [#](#pgrowlocks) <a href="#pgrowlocks" id="pgrowlocks"></a>

[F.31.1. 概觀](pgrowlocks/pgrowlocks-overview.md#pgrowlocks-overview)

[F.31.2. 輸出範例](pgrowlocks.md#pgrowlocks-sample-output)

[F.31.3. 作者](pgrowlocks.md#pgrowlocks-author)

<a id="id-1.11.7.41.2"></a>

`pgrowlocks` 模組提供一個函式，用來顯示指定資料表的資料列鎖定資訊。

預設情況下，只有超級使用者、具有 `pg_stat_scan_tables` 角色權限的角色，以及對該資料表具有 `SELECT` 權限的使用者可以使用。

### F.31.1. 概觀 [#](#pgrowlocks-overview) <a href="#pgrowlocks-overview" id="pgrowlocks-overview"></a>

完整內容請見 [F.31.1. 概觀](pgrowlocks/pgrowlocks-overview.md#pgrowlocks-overview)。

<a id="PGROWLOCKS-SAMPLE-OUTPUT"></a>

### F.31.2. 輸出範例 [#](#pgrowlocks-sample-output) <a href="#pgrowlocks-sample-output" id="pgrowlocks-sample-output"></a>

```

=# SELECT * FROM pgrowlocks('t1');
 locked_row | locker | multi | xids  |     modes      |  pids
------------+--------+-------+-------+----------------+--------
 (0,1)      |    609 | f     | {609} | {"For Share"}  | {3161}
 (0,2)      |    609 | f     | {609} | {"For Share"}  | {3161}
 (0,3)      |    607 | f     | {607} | {"For Update"} | {3107}
 (0,4)      |    607 | f     | {607} | {"For Update"} | {3107}
(4 rows)
```

<a id="PGROWLOCKS-AUTHOR"></a>

### F.31.3. 作者 [#](#pgrowlocks-author) <a href="#pgrowlocks-author" id="pgrowlocks-author"></a>

Tatsuo Ishii

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgrowlocks.html)（原文版本：18.6；核對日期：2026-10-23）
