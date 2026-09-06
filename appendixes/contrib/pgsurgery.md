## F.34. `pg_surgery` — 對關聯資料執行低階修復 [#](#PGSURGERY)

[F.34.1. 函式](pgsurgery.md#PGSURGERY-FUNCS)

[F.34.2. 作者](pgsurgery.md#PGSURGERY-AUTHORS)

<a id="id-1.11.7.44.2"></a>

`pg_surgery` 模組提供多種函式，可修復受損的關聯。這些函式在設計上並不安全，使用它們可能損毀（或進一步損毀）資料庫。例如，這些函式很容易使資料表與其索引不一致、導致 `UNIQUE` 或 `FOREIGN KEY` 限制條件違規，甚至使讀取時會造成資料庫伺服器當機的 tuple 變得可見。應極為謹慎地使用它們，且只應作為最後手段。

<a id="PGSURGERY-FUNCS"></a>

### F.34.1. 函式 [#](#PGSURGERY-FUNCS)

`heap_force_kill(regclass, tid[]) returns void`
:   `heap_force_kill` 不檢查 tuple，便將「已使用」的行指標標記為「死亡」。此函式的用途是強制移除其他方式無法存取的 tuple。例如：

    ```

    test=> select * from t1 where ctid = '(0, 1)';
    ERROR:  could not access status of transaction 4007513275
    DETAIL:  Could not open file "pg_xact/0EED": No such file or directory.

    test=# select heap_force_kill('t1'::regclass, ARRAY['(0, 1)']::tid[]);
     heap_force_kill
    -----------------

    (1 row)

    test=# select * from t1 where ctid = '(0, 1)';
    (0 rows)
    ```

`heap_force_freeze(regclass, tid[]) returns void`
:   `heap_force_freeze` 不檢查 tuple 資料，便將 tuple 標記為凍結。此函式的用途是讓因可見性資訊損毀而無法存取的 tuple 可被存取，或讓因可見性資訊損毀而無法成功執行清理的資料表得以清理。例如：

    ```

    test=> vacuum t1;
    ERROR:  found xmin 507 from before relfrozenxid 515
    CONTEXT:  while scanning block 0 of relation "public.t1"

    test=# select ctid from t1 where xmin = 507;
     ctid
    -------
     (0,3)
    (1 row)

    test=# select heap_force_freeze('t1'::regclass, ARRAY['(0, 3)']::tid[]);
     heap_force_freeze
    -------------------

    (1 row)

    test=# select ctid from t1 where xmin = 2;
     ctid
    -------
     (0,3)
    (1 row)
    ```

<a id="PGSURGERY-AUTHORS"></a>

### F.34.2. 作者 [#](#PGSURGERY-AUTHORS)

Ashutosh Sharma `<ashu.coek88@gmail.com>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgsurgery.html)（原文版本：18.6；核對日期：2026-09-06）
